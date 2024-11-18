@echo off
SETLOCAL

echo batch2 starts

set BASE_NAME=%1
set DATA_DIR=%2
set MODEL_NAME=%3
set FILTER_RES=%4
set FILTER_TIME=%5
set SKYLINE_FILE=%6
rem set dataset=%7
set SKYLINE_FILE=%SKYLINE_FILE:"=%

set STARTTIME=%TIME%

set ROOT_DIR=%ROOT_ANALYSIS_DIR%\%BASE_NAME%
set SKYD_FILE="%ROOT_ANALYSIS_DIR%\%SKYLINE_FILE%d"

echo [%STARTTIME%] Running trial %MODEL_NAME%...
echo [%STARTTIME%] Running trial %MODEL_NAME%... >> %LOG%
rem GOTO REPORT

rem ECHO precursor analysis starts now 
rem Save to new location to allow parallel processing
%SKYLINE_RUNNER% --timestamp --dir="%ROOT_DIR%" --in="..\%SKYLINE_FILE%" --out="%MODEL_NAME%\SKYLITE_TGFA_characteristic_pattern_pos.sky" >> %LOG%

rem Do the analysis in the new location
rem %SKYLINE_RUNNER% --timestamp --dir="%ROOT_DIR%" --in="%MODEL_NAME%\SKYLITE_TGFA_characteristic_pattern_pos.sky" --import-transition-list=%ROOT_ANALYSIS_DIR%\SKYLITE_TGFA_TL_characteristic_pattern_pos.csv --save  --import-lockmass-positive=556.2771 --import-lockmass-tolerance=0.5 --import-all="%ROOT_ANALYSIS_DIR%\RAW_DATA_LCMSMS_TGFA\%dataset%" --import-naming-pattern="_([^_]*)$" --save --report-add="%ROOT_ANALYSIS_DIR%\OxLPD1_black_box\SKYLITE\skyline_report_vpw15.skyr" --report-conflict-resolution=overwrite --report-name=skyl_report_template_vpw15 --report-file="%ROOT_ANALYSIS_DIR%\skyl_report_vpw20_0.csv" --report-invariant --chromatogram-products --chromatogram-file="%ROOT_ANALYSIS_DIR%\skyl_xic_report_tgfa.tsv" >> %LOG%
%SKYLINE_RUNNER% --timestamp --dir="%ROOT_DIR%" --in="%MODEL_NAME%\SKYLITE_TGFA_characteristic_pattern_pos.sky" --import-transition-list=%ROOT_ANALYSIS_DIR%\SKYLITE_TGFA_TL_characteristic_pattern_pos.csv --save  --import-lockmass-positive=556.2771 --import-lockmass-tolerance=0.5 --import-all="%ROOT_ANALYSIS_DIR%\%DATA_DIR%" --import-naming-pattern="_([^_]*)$" --save --chromatogram-products --chromatogram-file="%ROOT_ANALYSIS_DIR%\Skyl_XIC_Rep_JPM_TG_FA_pos.tsv" >> %LOG%

rem run XIC analysis and write TGFA results in excel file:
rem (passing replicate name in argument to python)
rem "python.exe" "%~dp0\OxLPD1_black_box\SKYLITE\SKYLITE_8_TG_FA_XIC_analysis_pos.py" %MODEL_NAME%
"python.exe" "%~dp0\SKYLITE_8_TG_FA_XIC_analysis_pos.py" %MODEL_NAME%

rem PAUSE
if %ERRORLEVEL% NEQ 0 GOTO END

:REPORT

:END

set ENDTIME=%TIME%

rem Change formatting for the start and end times
for /F "tokens=1-4 delims=:.," %%a in ("%STARTTIME%") do (
   set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)
for /F "tokens=1-4 delims=:.," %%a in ("%ENDTIME%") do (
   set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
)

rem Calculate the elapsed time by subtracting values
set /A elapsed=end-start
rem we might have measured the time inbetween days
if %end% LSS %start% set /A elapsed=(24*60*60*100 - start) + end

    rem Format the results for output
set /A hh=elapsed/(60*60*100), rest=elapsed%%(60*60*100), mm=rest/(60*100), rest%%=60*100, ss=rest/100, cc=rest%%100
if %hh% lss 10 set hh=0%hh%
if %mm% lss 10 set mm=0%mm%
if %ss% lss 10 set ss=0%ss%
if %cc% lss 10 set cc=0%cc%

set DURATION=%hh%:%mm%:%ss%.%cc%

echo. >> %LOG%
echo [%ENDTIME%] Completed trial %MODEL_NAME%... >> %LOG%
echo [%ENDTIME%] =^> Elapsed time: %DURATION%
echo [%ENDTIME%] =^> Elapsed time: %DURATION% >> %LOG%
echo. >> %LOG%
echo. >> %LOG%

ENDLOCAL