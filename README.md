# Skylite
Skyline-based lipid isomer retention time evaluation

This repository contains python and batch code for the Skylite workflow. Please see the associated publication for reference:
#

To run Skylite, a version of Skyline, including Skyline Runner is required, as well as a version of python.
Recommended: Anaconda & Visual Studio Code

A step-by-step guide to running this workflow is shown below.
The following updates have been made since the first release:

#



Step-by-step guide:
The below step-by-step protocol applies to negative mode data, but analogously to the analysis of positive mode data, except for noted differences.
1)	Generate Skyline transition list using the script ‘SKYLITE_1_TL.py’, LipidCreator and the Skyline transition list for the deuterated Ultimate SPLASH lipid standard (‘SKYLITE_Ultimate_SPLASH.csv’, see git-hub).
2)	Calculate inclusion lists for tandem mass spectrometric acquisition using the script ‘SKYLITE_2_TL_to_IL.py’.
3)	Prepare samples according to lipid extraction method described herein and run LC-MS/MS acquisition with the respective inclusion lists. Generally, include at least one retention time reference sample in each LC-MS sequence. Ideally, a NIST 1950 SRM lipid extract is used, alternatively, another human plasma, an A549 cancer cell line extract or a fetal bovine serum lipid extract should be used as retention time reference.
4)	Run SKYLITE_discovery.py with a representative or a PBQC dataset (both negative and positive mode acquisitions).
5)	Manually curate the resulting Skyline files to exclude lipids that are not observed with sufficient evidence in the MS/MS spectra. Adjust integration limits to include all potential isomers of the same sum composition and for each adjustment apply integration to all replicates. Export the report using the Skyline report template ‘SKYLITE_report_template’ and save report as ‘Skyline_report_curated_for_SKYLITE_3_neg.csv’.
6)	Adjust replicate naming pattern in script ‘SKYLITE_3_quantification_FA_sum_neg.py’ and run script using previous report from the negative mode analysis as input file. Only part of the filename needs to be included in the naming pattern, for example with a file named ‘2024_03_10_JPM_DML_neg_FB14_i1.raw’, where each replicate is identified as FB1, FB2, …FB21, the naming pattern list in the python script should be [‘FB1_’, ‘FB2_’, …’FB21_’] to allow a unique assignment of the filenames.
7)	Save previous Skyline file under changed filename and duplicate entries in Skyline for which there are chromatographically resolved isomers present and adjust integration limits to each MS/MS extracted ion chromatogram peak and for each adjustment apply integration to all replicates. Export the report using the Skyline report template ‘SKYLITE_report_template’ and save report as ‘Skyline_Report_isomers_for_SKYLITE_4_neg.csv’.
8)	Run script ‘SKYLITE_4_quantification_FA_isomers_neg.py’ and ‘SKYLITE_6_quantification_ FA_isomers_pos.py’ using the previous reports as input files, respectively.
9)	Calculate statistics as relevant and use NIST 1950 SRM and, if applicable, fetal bovine serum or an A549 cancer cell extract, as retention time reference to assign lipid isomers. For further confidence in the assignment, perform a hydrolysis and subsequent AMPP derivatization with a sample of interest and NIST 1950 SRM to compare retention times.
10)	Follow instructions in section 2.9 to determine reconstructed fatty acid profiles from triglyceride tandem MS data as well as the above sum composition analysis of triglycerides.



