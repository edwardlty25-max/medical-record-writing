#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""病历正文规范自检（确定性机检）。

用法：
    python scripts/validate_note.py note.md
    python scripts/validate_note.py note.md --kind progress
    python scripts/validate_note.py note.md --kind first-progress --admit "2026-09-16 08:00"
    python scripts/validate_note.py 手术记录.txt --kind procedure
    python scripts/validate_note.py 术前讨论.txt --kind preop-discussion
    python scripts/validate_note.py note.md --json
    Get-Content note.md -Raw | python scripts/validate_note.py -

退出码：0 = 通过（可含 WARN）；1 = 存在 ERROR；2 = 用法或读取错误。

本脚本只做**可机检**的格式与规范项，不判断医学内容对错，不替代医师与医院质控。
规则来源：references/rules.md（《河北省病历书写规范细则（2013年版）》+ 2023 补充要点）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
_ORDER = {ERROR: 0, WARN: 1, INFO: 2}

# ---------------------------------------------------------------- 规则表

# kind: (中文名, 时限分钟, 是否需签名, 是否需生命体征)
KINDS = {
    "admission":             ("入院记录", 1440, True, True),
    "admission-readmission": ("再次/多次入院记录", 1440, True, True),
    "first-progress":        ("首次病程记录", 480, True, True),
    "progress":              ("日常病程记录", None, True, False),
    "rounds-critical":       ("新入院危重患者上级查房记录", 1440, False, False),
    "rounds-attending":      ("主治医师首次查房记录", 2880, False, False),
    "rounds-director":       ("科主任/副高以上首次查房记录", 4320, False, False),
    "handover":              ("交接班记录", 1440, True, False),
    "rescue":                ("抢救记录（6 小时内补记）", 360, True, False),
    "consultation":          ("会诊记录", 1440, True, False),
    "discharge":             ("出院记录", 1440, True, False),
    "death":                 ("死亡记录", 1440, True, False),
    "death-discussion":      ("死亡病例讨论记录", 10080, True, False),
    "transfer":              ("转科记录", 1440, True, False),
}

UNIT_FORBIDDEN = {"公分": "cm", "公寸": "dm", "公尺": "m", "公升": "L",
                  "立升": "L", "市斤": "kg", "公斤": "kg"}
UNIT_DISCOURAGED = {"毫升": "mL", "厘米": "cm", "毫米": "mm"}

BRAND_NAMES = {
    "拜新同": "硝苯地平控释片", "络活喜": "氨氯地平", "波依定": "非洛地平",
    "代文": "缬沙坦", "安博维": "厄贝沙坦", "蒙诺": "福辛普利",
    "倍他乐克": "美托洛尔", "心律平": "普罗帕酮", "欣康": "单硝酸异山梨酯",
    "洛赛克": "奥美拉唑", "波立维": "氯吡格雷", "泰嘉": "氯吡格雷",
    "拜阿司匹灵": "阿司匹林", "拜阿斯匹灵": "阿司匹林",
    "立普妥": "阿托伐他汀", "可定": "瑞舒伐他汀", "舒降之": "辛伐他汀",
    "优甲乐": "左甲状腺素钠", "格华止": "二甲双胍", "拜糖平": "阿卡波糖",
    "诺和灵": "人胰岛素", "速尿": "呋塞米", "安体舒通": "螺内酯",
    "芬必得": "布洛芬", "扶他林": "双氯芬酸", "达克宁": "咪康唑",
}

ABBREVIATIONS = {
    "CABG": "冠状动脉旁路移植术", "COPD": "慢性阻塞性肺疾病",
    "ACS": "急性冠脉综合征", "T2DM": "2型糖尿病", "CKD": "慢性肾脏病",
    "NSAIDs": "非甾体抗炎药", "DKA": "糖尿病酮症酸中毒",
    "ARDS": "急性呼吸窘迫综合征", "SLE": "系统性红斑狼疮",
    "ITP": "免疫性血小板减少症",
}

DIAGNOSIS_WORDS = (
    "高血压", "糖尿病", "冠心病", "脑梗死", "脑出血", "心肌梗死", "心梗",
    "肺炎", "肿瘤", "癌", "综合征", "结石", "白血病", "贫血", "肝硬化",
    "骨折", "甲状腺功能亢进", "甲状腺功能减退", "肾功能不全", "感染",
)

ABSOLUTE_WORDS = ("一定", "完全排除", "明确无误", "肯定为", "100%", "绝对")
VAGUE_NEGATIVES = ("无异常", "(-)", "（-）", "(－)", "（－）")
DIAGNOSIS_TYPES = ("初步诊断", "修正诊断", "补充诊断", "出院诊断", "入院诊断",
                   "目前诊断", "死亡诊断", "最后诊断", "术前诊断", "术中诊断",
                   "术后诊断")

DATE_KINDS = ("progress", "first-progress", "admission", "admission-readmission",
              "rounds-critical", "rounds-attending", "rounds-director",
              "discharge", "death", "transfer", "handover", "rescue", "consultation")

# ---- 出院记录专用规则（对应 references/discharge-summary.md） ----
DISCHARGE_SECTIONS = ("入院情况", "入院诊断", "诊疗经过", "出院诊断", "出院情况", "出院医嘱")
ORDER_CATEGORIES = ("药物治疗", "复诊安排", "生活方式", "注意事项")
SKELETON_LABELS = ("【诊断依据】", "【住院检查】", "【诊断演变】", "【问题导向处理】",
                   "【会诊整合】", "【治疗小结】", "【出院前评估】", "【转归】")
CLOSURE_WORDS = ("复查", "复诊", "随诊", "随访")
UNSOLVED_MARKERS = ("拒绝", "待查", "未明确", "未完善")
CONSULT_TONE = ("贵科", "我科")

# ---- 易漏要素（对应各模板的“易漏要素”清单） ----
ALLERGY_KINDS = ("admission", "admission-readmission", "first-progress", "discharge")
BLOOD_PRODUCT_RE = re.compile(
    r"(?:输注|输)\s*(?:[ABO]{1,2}型)?\s*(?:悬浮红细胞|红细胞|血浆|血小板|全血|冷沉淀|白蛋白)")
BLOOD_REACTION_RE = re.compile(r"输血反应|输注反应|不良反应|无反应|未见反应")
PLACEHOLDER_RE = re.compile(r"_{2,}|＿{2,}")
TEMPLATE_HINT_RE = re.compile(
    r"（[^）]{0,40}(?:≤\s*\d+\s*字|不超过\s*\d+\s*字|如[:：]|选填|择一|可不填|括号内说明)[^）]{0,20}）")
DT_RE = re.compile(
    r"(\d{4})\s*[-/年]\s*(\d{1,2})\s*[-/月]\s*(\d{1,2})\s*日?(?:\s+|T)(\d{1,2})\s*[:：]\s*(\d{2})")
CLOCK_RE = re.compile(r"(?<![\d:])(\d{1,2})\s*[:：]\s*(\d{2})(?![\d:])")
TIME12_RE = re.compile(r"(上午|下午|晚上|凌晨|中午)\s*\d{1,2}")
HOUR_RE = re.compile(r"(?<![\d.（(])(\d{1,2})\s*[点时]")
TEMP_RE = re.compile(r"(?:体温|(?<![A-Za-z0-9])T)\s*[:：]?\s*\d{2}(?:\.\d)?")
BP_RE = re.compile(r"(?:血压|(?<![A-Za-z])BP)\s*[:：]?\s*\d{2,3}\s*/\s*\d{2,3}")

# ---- 围手术期 / 手术记录专用规则（对应 references/procedure-record.md） ----







CONSENT_OPINION_RE = re.compile(
    r"(签署意见|签字为证|家属签字|患者签字|已签字|同意手术|同意操作|同意置入|"
    r"(?:患者|家属|家属表示|患者表示|其)[^。；\n]{0,12}同意|自愿(?:接受|要求))")

PREOP_SUMMARY_RE = re.compile(r"术前小结|术前病程记录|术前记录")
PREOP_INDICATION_RE = re.compile(r"(手术指征|指征|必要性)")
PREOP_PREP_RE = re.compile(r"(术前准备|术前检查|禁食|备血|皮肤准备|抗凝|停药|桥接|碘过敏)")
PREOP_RISK_RE = re.compile(r"(手术风险|风险评估|出血|感染|麻醉风险|防范|并发症)")
CONSENT_OPINION_ONLY_RE = re.compile(r"(签署意见|同意手术|同意操作|签字为证|家属签字|患者签字)")



PREOP_WORKUP_RE = re.compile(
    r"(术前检查|术前评估|术前准备|入院后.{0,12}(?:检查|化验|复查)|完善.{0,10}(?:检查|化验)|"
    r"凝血功能|凝血四项|感染筛查|超声心动图|心脏超声|胸部 CT|胸部CT|胸部摄片|肺功能)")
EXAM_MARKER_RE = re.compile(
    r"(心电图|超声心动图|心脏超声|肌钙蛋白|高敏肌钙蛋白|心肌损伤标志物|肌酸激酶|血肌酐|肌酐|"
    r"eGFR|电解质|血钾|血常规|凝血|肝功能|血脂|CTA|磁共振|CT|造影|"
    r"射血分数|LVEF|动态心电图)")
PERIOP_MARKER_RE = re.compile(
    r"(术后|术前|手术记录|手术经过|术中|手术当日|手术治疗|有创操作)")
MED_RECONCILE_NOTE_RE = re.compile(r"(核对|以医嘱|医嘱为准|请确认|存疑|待医生确认|一致)")

# ---- 围手术期 / 病程相关常量 ----
POSTOP_PROGRESS_RE = re.compile(r"(术后病程|术后第 ?[一二三四五六七八九十\d]+ ?[天日]|术后当日|术后第一天)")
POSTOP_EXAM_RE = re.compile(r"(切口|伤口|引流|敷料|渗血|渗液|红肿|末梢|局部)")
POSTOP_REVIEW_RE = re.compile(r"(心肌损伤|肌钙蛋白|BNP|肾功能|肌酐|电解质|血常规|凝血|心电图)")
DIAGNOSIS_CHANGE_RE = re.compile(r"(修正诊断|补充诊断|诊断修正|诊断变更|更改诊断)")
DIAGNOSIS_BASIS_RE = re.compile(
    r"(依据(?!诊断)|根据|检查示|检查提示|复查|证实|结果示|报告示|"
    r"CT|磁共振|MRI|超声|心电图|肌钙蛋白|阳性|阴性|升高|下降|提示|考虑)")
DIAGNOSIS_FILLER_RE = re.compile(r"(考虑|诊断|明确|病情需要|结合临床表现|进一步明确)")
REFUSAL_RE = re.compile(r"(拒绝|不同意|自动出院|自行离院)")
REFUSAL_INFORM_RE = re.compile(r"(告知|已告知|交代|交待|说明|知情)")
REFUSAL_ALTERNATIVE_RE = re.compile(r"(替代|替代方案|改为|继续目前|随访|复查|观察)")
CONSULT_LEAD_RE = re.compile(
    r"((?:[\u4e00-\u9fff]{2,8}科)[^。；\n]{0,12}(?:会诊|随诊|建议))")
CONSULT_ADOPT_RE = re.compile(
    r"(采纳|已执行|执行|已加用|已予|已给|按会诊意见|暂不执行|未采纳|同意会诊|"
    r"暂不加用|暂不加|暂予|暂按|已调整|已改|遵会诊|结合会诊|依会诊|"
    r"患者拒绝|家属拒绝|已告知|未执行|经[^。；\n]{0,10}会诊后)")
STATINS = ("阿托伐他汀", "瑞舒伐他汀", "辛伐他汀", "普伐他汀", "氟伐他汀", "匹伐他汀", "洛伐他汀")
DRUG_DOSE_PAIRS = (
    ("阿托伐他汀", ("10mg", "20mg", "40mg", "80mg", "10 mg", "20 mg", "40 mg", "80 mg")),
    ("瑞舒伐他汀", ("5mg", "10mg", "20mg", "5 mg", "10 mg", "20 mg")),
    ("阿司匹林", ("75mg", "100mg", "75 mg", "100 mg")),
    ("替格瑞洛", ("90mg", "60mg", "90 mg", "60 mg", "180mg", "180 mg")),
    ("氯吡格雷", ("75mg", "75 mg", "300mg", "300 mg")),
    ("美托洛尔", ("25mg", "47.5mg", "50mg", "95mg", "25 mg", "47.5 mg", "50 mg")),
    ("氨氯地平", ("2.5mg", "5mg", "10mg", "2.5 mg", "5 mg", "10 mg")),
    ("呋塞米", ("20mg", "40mg", "20 mg", "40 mg")),
    ("螺内酯", ("20mg", "25mg", "20 mg", "25 mg")),
)
MED_RECONCILE_NOTE_RE = re.compile(r"(核对|以医嘱|医嘱为准|请确认|存疑|待医生确认|一致)")
VESSEL_NAMES = ()
UNTREATED_BASIS = ()

FINDINGS: list[dict] = []


def add(level: str, code: str, line: int, message: str) -> None:
    FINDINGS.append({"level": level, "code": code, "line": line, "message": message})


def line_no(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def each(text: str, pattern: re.Pattern):
    for m in pattern.finditer(text):
        yield m, line_no(text, m.start())


# ---------------------------------------------------------------- 检查项

def check_length(text: str) -> None:
    if not text.strip():
        add(ERROR, "empty", 1, "内容为空")
    elif len(re.sub(r"\s", "", text)) < 40:
        add(ERROR, "too_short", 1, "内容过短（<40 字），疑似未成稿")


def check_placeholders(text: str) -> None:
    for m, ln in each(text, PLACEHOLDER_RE):
        add(ERROR, "placeholder", ln, f"模板占位符未填写：{m.group(0)}")
    for m, ln in each(text, TEMPLATE_HINT_RE):
        add(WARN, "template_hint", ln, f"疑似模板说明文字进入正文：{m.group(0)[:30]}")
    for token in ("【待补充】", "【待补充确认】", "【待医生确认】"):
        idx = text.find(token)
        while idx != -1:
            add(WARN, "pending_field", line_no(text, idx),
                f"正文含 {token}，请确认是否已核实或需医生补充")
            idx = text.find(token, idx + 1)


def extract_chief_complaint(text: str):
    lines = text.splitlines()
    for i, raw in enumerate(lines):
        s = raw.strip()
        if re.match(r"^[【\[（(]?\s*主诉\s*[】\]）)]?\s*[:：]", s):
            body = re.split(r"[:：]", s, maxsplit=1)[1].strip()
            if body:
                return body, i + 1
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j].strip():
                    return lines[j].strip(), j + 1
    return None, 0


def check_chief_complaint(text: str) -> None:
    body, ln = extract_chief_complaint(text)
    if not body:
        return
    compact = re.sub(r"[\s，。、；：,.;:！？!?“”\"'（）()]", "", body)
    n = len(compact)
    if n > 30:
        add(ERROR, "cc_length", ln, f"主诉 {n} 字，明显超过 20 字（规范：一般不超过 20 字）")
    elif n > 20:
        add(WARN, "cc_length", ln, f"主诉 {n} 字，超过 20 字，建议精简")
    for w in DIAGNOSIS_WORDS:
        if w in body:
            add(WARN, "cc_diagnosis", ln,
                f"主诉疑似含诊断/检查结果「{w}」；主诉应为症状或体征 + 部位 + 持续时间")
            break
    if "阳性" in body or "阴性" in body:
        add(WARN, "cc_result", ln, "主诉疑似含检查结果，建议移入现病史或辅助检查")


def check_time(text: str, kind) -> None:
    for m, ln in each(text, TIME12_RE):
        add(ERROR, "time_12h", ln, f"未使用 24 小时制：{m.group(0)}")
    for m, ln in each(text, HOUR_RE):
        if int(m.group(1)) > 24:
            add(ERROR, "time_hour", ln, f"小时数异常：{m.group(0)}")
        seg = text[m.end(): m.end() + 4]
        if not re.match(r"\s*(分|整|\d{1,2}\s*分|[:：]\d{2})", seg):
            add(WARN, "time_minute", ln, f"时间未精确到分：{m.group(0)}")
    for m, ln in each(text, CLOCK_RE):
        if int(m.group(1)) > 24 or int(m.group(2)) > 59:
            add(ERROR, "time_invalid", ln, f"时间格式异常：{m.group(0)}")
    if kind in DATE_KINDS and not re.search(r"\d{4}\s*[-/年]", text):
        add(WARN, "date_missing", 1, "未见完整日期（年-月-日）；病历文书应写明日期与时间")


def check_units(text: str) -> None:
    for bad, good in UNIT_FORBIDDEN.items():
        for _m, ln in each(text, re.compile(re.escape(bad))):
            add(ERROR, "unit_forbidden", ln, f"计量单位「{bad}」不规范，应写 {good}")
    for w, good in UNIT_DISCOURAGED.items():
        for _m, ln in each(text, re.compile(re.escape(w))):
            add(WARN, "unit_discouraged", ln, f"「{w}」建议改用法定符号 {good}")
    for m, ln in each(text, TEMP_RE):
        if not re.match(r"\s*(℃|°C|度)", text[m.end(): m.end() + 3]):
            add(WARN, "unit_missing", ln, f"体温疑似缺单位（℃）：{m.group(0)}")
    for m, ln in each(text, BP_RE):
        seg = text[m.end(): m.end() + 8]
        if "mmHg" not in seg and "毫米汞柱" not in seg:
            add(WARN, "unit_missing", ln, f"血压疑似缺单位（mmHg）：{m.group(0)}")


def check_wording(text: str) -> None:
    for w in ABSOLUTE_WORDS:
        for _m, ln in each(text, re.compile(re.escape(w))):
            add(WARN, "absolute_wording", ln,
                f"含绝对化表述「{w}」；除非医生已确认，建议改为「目前考虑/现有资料支持」")
    for w in VAGUE_NEGATIVES:
        for _m, ln in each(text, re.compile(re.escape(w))):
            add(WARN, "vague_negative", ln, f"「{w}」过于笼统，阴性体征须逐系统具体描述")
    for w, generic in BRAND_NAMES.items():
        for _m, ln in each(text, re.compile(re.escape(w))):
            add(WARN, "brand_name", ln, f"疑似商品名「{w}」，病历须用通用名（如 {generic}）")
    for abbr, full in ABBREVIATIONS.items():
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(abbr) + r"(?![A-Za-z0-9])")
        for _m, ln in each(text, pat):
            if full not in text:
                add(WARN, "abbreviation", ln, f"缩写 {abbr} 首次出现应写全称：{full}（{abbr}）")


def check_diagnosis(text: str) -> None:
    if re.search(r"(初步诊断|诊断)\s*[:：]", text) and not any(t in text for t in DIAGNOSIS_TYPES):
        add(WARN, "diagnosis_type", 1,
            "诊断未注明分类（初步/修正/补充/出院）；入院记录须写「初步诊断」")


def check_signature(text: str, need_sig: bool) -> None:
    if "签名" not in text:
        if need_sig:
            add(WARN, "signature_missing", 1, "未见「医师签名」行，须由医师本人签署全名")
        return
    for m, ln in each(text, re.compile(r"签名\s*[:：]?\s*([^\n]*)")):
        tail = m.group(1).strip()
        cleaned = re.sub(r"[\s_\-—－]", "", tail)
        cleaned = cleaned.replace("（全名）", "").replace("(全名)", "")
        if cleaned == "":
            add(WARN, "signature_empty", ln, "签名处为空或仍为占位符，须签署全名")
        elif len(cleaned) < 2:
            add(WARN, "signature_short", ln, f"签名疑似不完整：{tail[:20]}")


def check_vitals(text: str, need_vitals: bool) -> None:
    if not need_vitals:
        return
    missing = []
    if not re.search(r"(?:体温|(?<![A-Za-z0-9])T)\s*[:：]?\s*\d", text):
        missing.append("T")
    if not re.search(r"(?:脉搏|心率|(?<![A-Za-z])P)\s*[:：]?\s*\d", text):
        missing.append("P")
    if not re.search(r"(?:呼吸|(?<![A-Za-z])R)\s*[:：]?\s*\d", text):
        missing.append("R")
    if not re.search(r"(?:血压|(?<![A-Za-z])BP)\s*[:：]?\s*\d", text):
        missing.append("BP")
    if missing:
        add(WARN, "vitals_missing", 1, "生命体征不完整，缺：" + "、".join(missing))


def check_discharge(text: str, kind) -> None:
    """出院记录专用检查（对应 references/discharge-summary.md 的模板要求）。"""
    if kind != "discharge":
        return
    missing = [s for s in DISCHARGE_SECTIONS if s not in text]
    if missing:
        add(ERROR, "discharge_sections_missing", 1,
            "出院记录缺少必备段落：" + "、".join(missing))
    for label in SKELETON_LABELS:
        pos = text.find(label)
        if pos != -1:
            add(ERROR, "skeleton_label_leak", line_no(text, pos),
                f"正文残留思考骨架标签 {label}；成文形态必须删除全部【】标签")
    idx = text.find("出院医嘱")
    if idx == -1:
        return
    orders = text[idx:]
    lack = [c for c in ORDER_CATEGORIES if c not in orders]
    if lack:
        add(WARN, "orders_categories_missing", line_no(text, idx),
            "出院医嘱缺少类别：" + "、".join(lack))
    if not any(w in orders for w in CLOSURE_WORDS):
        add(WARN, "no_recheck_plan", line_no(text, idx),
            "出院医嘱未见复查/复诊/随诊安排")
    body = text[:idx]
    if any(m in body for m in UNSOLVED_MARKERS) and not any(
            w in orders for w in ("建议", "完善", "复查", "复诊", "随诊")):
        add(WARN, "no_unsolved_closure", 1,
            "诊疗经过存在未完成事项（拒绝/待查等），但复诊安排未给出对应出口")
    for word in CONSULT_TONE:
        pos = text.find(word)
        if pos != -1:
            add(WARN, "consult_note_copied", line_no(text, pos),
                f"疑似照录会诊原文（「{word}」）；应转写为本院叙述：会诊科室 + 意见 + 本科采纳情况")


def check_perioperative(text: str, kind) -> None:
    """围手术期前后呼应（病程 / 出院记录）。"""
    if kind not in ("progress", "rounds-attending", "rounds-critical", "rounds-director", "discharge"):
        return
    if not PERIOP_MARKER_RE.search(text):
        return
    if PREOP_SUMMARY_RE.search(text) and not POSTOP_PROGRESS_RE.search(text):
        return    # 术前小结/术前病程：本就不该含术后病程
    is_postop_record = bool(POSTOP_PROGRESS_RE.search(text))
    if not is_postop_record and re.search(r"术[后前][^\n]{0,20}(?:手术|操作|治疗)经过[^\n]{0,10}详见手术记录", text):
        is_postop_record = True
    if not is_postop_record and re.search(r"今[日天][^\n]{0,40}行[^\n]{0,20}(?:手术|操作|治疗|术)", text):
        is_postop_record = True
    if not is_postop_record:
        add(WARN, "postop_progress_missing", 1,
            "正文涉及手术，但未见术后病程记录（术后当日须有首次术后病程，此后连续记录）")
    if not POSTOP_EXAM_RE.search(text):
        add(WARN, "postop_exam_missing", 1,
            "术后记录未见切口或引流等局部观察要素（渗血、渗液、红肿、局部循环与感觉）")
    if not POSTOP_REVIEW_RE.search(text):
        add(WARN, "postop_recheck_missing", 1,
            "术后记录未见复查项目（心肌损伤标志物/肾功能与电解质/血常规/凝血/心电图等）")
    if kind == "discharge" and not any(k in text for k in ("切口", "伤口", "愈合", "引流")):
        add(WARN, "perioperative_no_outcome", 1,
            "有手术/介入，但出院记录未见切口或局部愈合情况的出院前评估")
    if kind != "discharge":
        return
    # 检查位置预留：出院记录要有承载术前检查与术后复查的位置
    _seg = lambda a, b: (text[text.find(a): text.find(b)] if (a in text and b in text and text.find(a) < text.find(b)) else "")
    seg_adm = _seg("入院情况", "入院诊断")
    seg_course = _seg("诊疗经过", "出院诊断")
    seg_status = _seg("出院情况", "出院医嘱")
    if not seg_course:
        return
    if not EXAM_MARKER_RE.search(seg_adm) and not (
            PREOP_WORKUP_RE.search(seg_course[:len(seg_course) // 2])
            or re.search(r"术前[^。；\n]{0,30}", seg_course)):
        add(WARN, "preop_exam_location_missing", 1,
            "入院情况与诊疗经过前半段均未见术前检查/术前评估内容；"
            "支持手术指征的术前检查应写在此处，不能只说「具备手术指征」")
    if EXAM_MARKER_RE.search(seg_status):
        add(WARN, "exam_in_discharge_status", 1,
            "出院情况段出现检查结果；该段只写症状、生命体征、查体、功能状态与待办检查，"
            "检查结果应移至诊疗经过（术后复查或出院前复查）")


def check_diagnosis_revision(text: str) -> None:
    """修正/补充诊断五要素（诊断名称 + 依据 + 时间 + 对治疗的影响 + 签名）。"""
    m = DIAGNOSIS_CHANGE_RE.search(text)
    if not m:
        return
    # 只看诊断变更所在那一段（前后各有限字符），避免被全文其他内容掩盖
    seg = text[max(0, m.start() - 120): m.end() + 400]
    if not DIAGNOSIS_BASIS_RE.search(seg):
        add(WARN, "diagnosis_revision_no_basis", line_no(text, m.start()),
            "出现修正/补充诊断，但该段未见具体依据（检查项目、数值与时间）；诊断变更必须留痕")
    seg_compact = re.sub(r"\s", "", seg)
    if not DT_RE.search(seg) and not re.search(r"\d{1,2}月\d{1,2}日", seg_compact):
        add(WARN, "diagnosis_revision_no_time", line_no(text, m.start()),
            "修正/补充诊断未见日期/时间；须注明依据的发现时间与记录日期")


def check_refusal(text: str) -> None:
    """患者拒绝检查/治疗的六要素留痕。"""
    for m, ln in each(text, REFUSAL_RE):
        seg = text[max(0, m.start() - 220): m.end() + 220]
        missing = []
        if not REFUSAL_INFORM_RE.search(seg):
            missing.append("已告知的风险")
        if not REFUSAL_ALTERNATIVE_RE.search(seg):
            missing.append("替代方案或随访安排")
        if missing:
            add(WARN, "refusal_unstated", ln,
                "记录到患者拒绝，但同一段未见：" + "、".join(missing)
                + "；拒绝须写清「告知了什么 + 拒绝什么 + 后果 + 替代方案 + 随访出口」")


def check_consult_closing(text: str) -> None:
    """会诊意见须有本科采纳情况。"""
    if not CONSULT_LEAD_RE.search(text):
        return
    if not CONSULT_ADOPT_RE.search(text):
        add(WARN, "consult_no_adoption", 1,
            "提到他科会诊/建议，但未见本科采纳情况；应写「会诊科室 + 意见 + 本科采纳/不采纳及理由」")


def check_med_reconciliation(text: str) -> None:
    """同一药物出现两种写法或两个剂量（跨全文比对），提示逐条核对。"""
    present = [s for s in STATINS if s in text]
    if len(present) > 1 and not MED_RECONCILE_NOTE_RE.search(text):
        add(WARN, "med_reconciliation_risk", 1,
            "全文出现两种他汀类（" + "、".join(present) + "）；须以医嘱执行记录为准统一写法，"
            "或并列呈现请医生确认（不得自行取舍）")
    for generic, doses in DRUG_DOSE_PAIRS:
        if generic not in text:
            continue
        hits = {d for d in doses if d in text}
        if len(hits) > 1 and not MED_RECONCILE_NOTE_RE.search(text):
            add(WARN, "med_reconciliation_risk", 1,
                f"{generic} 出现多个剂量（" + "、".join(sorted(hits)) + "）；须核对医嘱后统一")



def check_rounds_increment(text: str, kind) -> None:
    """上级查房记录：分析要有增量、指示要有落实。"""
    if kind not in ("rounds-attending", "rounds-critical", "rounds-director"):
        return
    if not re.search(r"(考虑|结合|提示|支持|复查|检查示|分析|认为)", text):
        add(WARN, "rounds_no_analysis", 1,
            "上级查房记录未见分析依据（依据→判断→决策）；不得只复述病情与「继续观察」")
    if not re.search(r"(建议|指示|同意|调整|加用|停用|改为|计划|择期|继续(?!观察|目前))", text):
        add(WARN, "rounds_no_decision", 1,
            "上级查房记录未见明确的诊疗决策或下一步安排")
    if "查房意见" in text and not re.search(r"(已执行|已按|已加用|已调整|已予|当日执行|落实情况)", text):
        add(WARN, "rounds_no_followthrough", 1,
            "提到「查房意见」但未见落实记录；应在当日或次日病程写明「已按查房意见执行××」")


def check_required_elements(text: str, kind) -> None:
    """易漏要素：过敏史、输血反应。"""
    if kind in ALLERGY_KINDS and "过敏" not in text:
        add(WARN, "allergy_history_missing", 1,
            "未见过敏史记录；既往史/入院情况须明确药物与食物过敏史（无则写「无」）")
    if BLOOD_PRODUCT_RE.search(text) and not BLOOD_REACTION_RE.search(text):
        add(WARN, "transfusion_reaction_unstated", 1,
            "记录了输血/输注血制品，但未见有无输血反应的描述")


def parse_first_dt(text: str):
    m = DT_RE.search(text)
    if not m:
        return None
    try:
        y, mo, d, h, mi = (int(x) for x in m.groups())
        return datetime(y, mo, d, h, mi)
    except ValueError:
        return None


def check_deadline(text: str, kind, admit_raw, record_raw) -> None:
    if not admit_raw:
        return
    admit = parse_first_dt(admit_raw)
    if admit is None:
        add(WARN, "deadline_input", 1, f"--admit 无法解析为时间：{admit_raw}")
        return
    record = parse_first_dt(record_raw) if record_raw else parse_first_dt(text)
    if record is None:
        add(WARN, "deadline_input", 1,
            "未能从正文解析记录时间（需形如 2026-09-16 09:20），本次未做时限勾稽")
        return
    limit = KINDS.get(kind or "", ("", None, False, False))[1]
    if limit is None:
        return
    delta = (record - admit).total_seconds() / 60
    if delta < 0:
        add(WARN, "deadline_order", 1, "记录时间早于起始时间，请核对")
    elif delta > limit:
        add(ERROR, "deadline", 1,
            f"时限超标：距起始时间 {delta / 60:.1f} 小时，超过 {limit / 60:g} 小时上限（单项否决项）")
    else:
        add(INFO, "deadline", 1, f"时限勾稽通过：{delta / 60:.1f} 小时 ≤ {limit / 60:g} 小时")


# ---------------------------------------------------------------- 入口

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="病历正文规范自检（确定性机检）")
    ap.add_argument("path", help="病历正文文件；用 - 从标准输入读取")
    ap.add_argument("--kind", choices=sorted(KINDS), help="文书类型（用于时限/签名/生命体征检查）")
    ap.add_argument("--admit", help="起始时间（如入院时间），用于时限勾稽")
    ap.add_argument("--record", help="记录时间；缺省时从正文自动解析")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = ap.parse_args(argv)

    try:
        if args.path == "-":
            raw = sys.stdin.buffer.read()
        else:
            with open(args.path, "rb") as fh:
                raw = fh.read()
    except OSError as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 2
    text = raw.decode("utf-8-sig", errors="replace")

    name = KINDS.get(args.kind or "", ("（未指定文书类型）", None, False, False))
    need_sig, need_vitals = name[2], name[3]
    name = name[0]

    check_length(text)
    check_placeholders(text)
    check_chief_complaint(text)
    check_time(text, args.kind)
    check_units(text)
    check_wording(text)
    check_diagnosis(text)
    check_signature(text, need_sig)
    check_vitals(text, need_vitals)
    check_discharge(text, args.kind)
    check_perioperative(text, args.kind)
    check_diagnosis_revision(text)
    check_rounds_increment(text, args.kind)
    check_refusal(text)
    check_consult_closing(text)
    check_med_reconciliation(text)
    check_required_elements(text, args.kind)
    check_deadline(text, args.kind, args.admit, args.record)

    FINDINGS.sort(key=lambda f: (_ORDER.get(f["level"], 9), f["line"]))
    errors = [f for f in FINDINGS if f["level"] == ERROR]
    warns = [f for f in FINDINGS if f["level"] == WARN]

    if args.json:
        print(json.dumps({"kind": args.kind, "kind_name": name,
                          "errors": len(errors), "warnings": len(warns),
                          "findings": FINDINGS}, ensure_ascii=False, indent=2))
    else:
        print(f"文书类型：{name}")
        if not FINDINGS:
            print("自检通过：未发现规范性错误（0 ERROR / 0 WARN）")
        else:
            for f in FINDINGS:
                print(f"[{f['level']:<5}] L{f['line']:<4} {f['message']}")
            verdict = "未通过，请修正 ERROR 后重跑" if errors else "通过（有需确认项）"
            print(f"\n合计：{len(errors)} ERROR / {len(warns)} WARN —— {verdict}")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
