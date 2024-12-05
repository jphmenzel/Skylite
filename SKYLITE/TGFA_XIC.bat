@ECHO OFF
rem ECHO ------- SKYLITE MULTI TGFA ANALYSIS -------
rem ECHO This batch file controls the SKYLITE triglyceride fatty acid analysis workflow using LC-MS/MS data. 
rem ECHO The workflow was created by Dr. Jan Philipp Menzel,
rem ECHO Inselspital, Bern University Hospital, 2023 / 2024.
rem ECHO Before running the workflow, make sure that:
rem ECHO  1 There is enough diskspace available, recommended is at least 10 GB free space.
rem ECHO  2 The maximum retention time in the Transition Settings in the Skyline file template.sky is set according to the analysis.
rem ECHO  3 The dataset to be analysed and python programs are in the appropriate directories.

rem To install this file on a computer, make sure the folder structure is maintained as indicated herein.
rem Tip: Use the find and replace function in Notepad++ to make the changes in all batch files at once.
rem ECHO For instructions and further information see the publication: _.

set replicatex=%1
rem ECHO %replicatex%
set replicate=%replicatex:~0,-1%
set dataset=RAW_DATA_%replicate%TGFA
ECHO The current replicate / sample is:
ECHO %replicate%
rem ECHO %dataset%

SETLOCAL
set ROOT_ANALYSIS_DIR=%~dp0
set SKYLINE_RUNNER="%ROOT_ANALYSIS_DIR%\SKYLITE_black_box\SkylineRunner.exe"
set BAT_Script_TGFA_XIC_run="%ROOT_ANALYSIS_DIR%\SKYLITE_black_box\TGFA_XIC_run.bat"
set LOG="%ROOT_ANALYSIS_DIR%\SKYLITE_black_box\workflow_log_files\Import.log"
FOR /F %%A IN ('WMIC OS GET LocalDateTime ^| FINDSTR \.') DO @SET DT=%%A
set LOG_ROLLOVER="%ROOT_ANALYSIS_DIR%\SKYLITE_black_box\workflow_log_files\Import_%DT:~0,8%_%DT:~8,6%.log"

if exist %LOG% move %LOG% %LOG_ROLLOVER%

rem echo Test

rem run precheck precursor only Skyline analysis, export chromatograms, convert tsv file to csv files
rem call %BAT_Script_TGFA_XIC_run%  SKYLITE_multi_results RAW_DATA_LCMSMS_TGFA\%dataset% %replicate% 100000 12 "template.sky" dataset
call %BAT_Script_TGFA_XIC_run% SKYLITE_multi_results All_raw_data_LCMSMS_TGFA\%dataset% %replicatex% 100000 12 "template.sky"

rem echo meow

if %ERRORLEVEL% NEQ 0 GOTO END
GOTO END
:END 

rem begin make new folder and Move results files excel and csv to folder in OzFAD1_results location of current run
md SKYLITE_multi_results\%replicate%\transition_lists_and_report_files
rem copy %~dp0\OzFAD1_workflow_parameters.xlsx %~dp0\OzFAD1_results\%identifier%\transition_lists_and_report_csv_files
move %~dp0\Skyl_XIC_Rep_JPM_TG_FA_pos.tsv %~dp0\SKYLITE_multi_results\%replicate%\transition_lists_and_report_files

move %~dp0\skyl_xic_report_1_intensities_pos.csv %~dp0\SKYLITE_multi_results\%replicate%\transition_lists_and_report_files
move %~dp0\skyl_xic_report_1_intensities_CORRECTED_pos.csv %~dp0\SKYLITE_multi_results\%replicate%\transition_lists_and_report_files
move %~dp0\skyl_xic_report_1_intensities_FPS_pos.tsv %~dp0\SKYLITE_multi_results\%replicate%\transition_lists_and_report_files
move %~dp0\skyl_xic_report_1_times_pos.csv %~dp0\SKYLITE_multi_results\%replicate%\transition_lists_and_report_files
rem end make new folder and Move results files excel and csv to folder in OzFAD1_results location of current run

echo The calculation is completed.
rem :END
ENDLOCAL
rem PAUSE
