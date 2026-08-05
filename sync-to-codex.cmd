@echo off
REM 将本 skill（Claude 权威副本）同步到 Codex 副本（Windows 双击运行）
set SRC=%USERPROFILE%\.claude\skills\medical-record-writing
set DST=%USERPROFILE%\.codex\skills\medical-record-writing
mkdir "%DST%" 2>nul
copy /Y "%SRC%\SKILL.md" "%DST%\SKILL.md" >nul
xcopy /E /Y /Q "%SRC%\references" "%DST%\references" >nul
copy /Y "%SRC%\README.md" "%DST%\README.md" >nul
echo [OK] 已同步 Claude -> Codex: %DST%
pause
