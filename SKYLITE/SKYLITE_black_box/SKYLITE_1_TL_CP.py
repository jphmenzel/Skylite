# -*- coding: UTF-8 -*-

# Developer: Dr. Jan Philipp Menzel 
# Summary: Generates transition lists for detection of intact lipids by LC-MS, 
#  generates inclusion lists based on transitions that are generated (both pos and neg acquisitions)
## NOTES: First version created 22 May 2023

import math
import os
import openpyxl
import pandas as pd
import datetime
import openpyxl
from pathlib import Path
from openpyxl import Workbook
beforeall=datetime.datetime.now()

#isotope=['1H   ', '2H  ', '12C   ', '14N   ', '16O    ', '31P   ', '32S    ' '23Na     ', 'e     ', '132Xe', '   127I',      '13C']
imass=[1.007825, 2.0141, 12.00000, 14.00307, 15.99491, 30.973762, 31.97207, 22.98977, 0.000548585, 131.9041535, 126.904473, 13.003355]
atom=['H', 'D', 'C', 'N', 'O', 'P', 'S', 'Na', 'e', 'Xe', 'I']

mzh=imass[0]
mzd=imass[1]
mzc=imass[2]
mzn=imass[3]
mzo=imass[4]
mzp=imass[5]
mzna=imass[7]
mze=imass[8]
mzcth=imass[11]
############################################################################################################################################
##################################################    define lipid / FA species space						###########################
############################################################################################################################################
oxion=0			
identifier='NIST1950'
#maxrts=60 # set maximum RT for inclusion lists
maxrts=20 # set maximum RT for inclusion lists
collen=10	# set collision energy
gmode=1 # 0 	# Ceramides contain many odd chain saturated FA, use gmode=1 for plasma and other samples that can contain ceramides
# scufalist is list of likely unsaturated FA at sum compositional level				# EDIT TO GENERATE OTHER LIPIDS
if gmode==0:
	sfalist=[[16, 0], [18, 0]] # STANDARD TEST FA PROFILE
	scufalist=[[16, 1], [18, 1], [18, 2]]   
elif gmode==1:					# RECOMMENDED COMPREHENSIVE FA PROFILE
	sfalist=[[8, 0], [9, 0], [10, 0], [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], 
		  [21, 0], [22, 0], [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0], [30, 0]]                   # COMPREHENSIVE mammalian FA PROFILE
	scufalist=[[10, 1], [12, 1], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1], [21, 1], [22, 1], [24, 1], [26, 1], 
			[14, 2], [15, 2], [16, 2], [17, 2], [18, 2], [19, 2], [20, 2], [21, 2], [22, 2], [24, 2], 
			[14, 3], [16, 3], [17, 3], [18, 3], [19, 3], [20, 3], [21, 3], [22, 3], [23, 3], [24, 3], 
			[16, 4], [18, 4], [20, 4], [22, 4], [24, 4], [16, 5], [20, 5], [22, 5], [24, 5], [26, 5], [20, 6], [22, 6], [24, 6], [22, 7]] 		# COMPREHENSIVE mammalian FA PROFILE
elif gmode==2:
	sfalist=[[16, 0], [18, 0], [20, 0]] # ALTERNATIVE TEST FA PROFILE
	scufalist=[[16, 1], [18, 1], [18, 2], [20, 2], [18, 3], [20, 3], [20, 4], [22, 6]] 
elif gmode==3:
	sfalist=[[14, 0], [15, 0], [16, 0], [18, 0], [20, 0], [22, 0], [24, 0]] #, [26, 0]]   [19, 0],    [17, 0],              # NOT SO COMPREHENSIVE NIST FA PROFILE
	scufalist=[[14, 1], [16, 1], [17, 1], [18, 1], [20, 1], [16, 2], [18, 2], [20, 2], [18, 3], [20, 3], [20, 4], [22, 4], [20, 5], [22, 5], [22, 6]] #  [19, 1],  

sorting=1	# number of times the transition list is to be sorted (0 or 1 or 2; 0 for super large TL, 1 is default, 2 to test for sorting improvemnt in case of errors)
# [[18, 2], [20, 2], [18, 3], [20, 4], [22, 6]]  # alternative
# [[18, 2], [20, 4], [22, 6]]  # alternative
# [[18, 1], [18, 2], [16, 1]]  # alternative
charpshortcut=0											# MODIFY TO SELECT GENERATION OF FULL TRANSITION LIST OR PROCESSING OF TL TO CHARACTERISTIC PATTERN TL
if charpshortcut==0:
	scramble=1				# Including species with multiple unsaturated FA 
	if scramble==1:
		si=0
		while si<len(scufalist):
			sfalist.append(scufalist[si])
			si=si+1
	scramble=2				# Including species with multiple saturated FA 
	if scramble==2:
		si=0
		while si<len(sfalist):
			scufalist.append(sfalist[si])
			si=si+1		

	# PC: Phosphatidylcholine
	# OC: Ether PC
	# QC: Vinylether (Plasmalogen) or ether PC
	# PE: Phosphatidylethanolamine
	# OE: Ether PE
	# QE: Vinylether (Plasmalogen) or ether PE
	# PA: Phosphatidic acid
	# PI: Phosphatidylinositol
	# PG: Phosphatidylglycerol
	# PS: Phosphatidylserine
	# SM: Sphingomyeline
	# CR: Ceramide
	# HC: Hexosylceramide
	# DC: Dihexosylceramide
	# LC: Lysophosphtidylcholine, LPC
	# LE: Lysophosphtidylcholine, LPE
	# LA: Lysophosphtidylcholine, LPA
	# LI: Lysophosphtidylcholine, LPI
	# LG: Lysophosphtidylcholine, LPG
	# LS: Lysophosphtidylcholine, LPS
	# CE: Cholesterol ester
	# DG: Diacylglycerol
	# TG: Triacylglycerol

	# Fixed definitions: 
	#hglist=['PC', 'PE', 'PA', 'PI', 'PG', 'PS',
	#	'SM', 'CR', 'HC', 'DC',
	#	'LC', 'LE', 'LA', 'LI', 'LG', 'LS',
	#	'CE', 'TG', 'DG']		#
	#hgflist=[[8, 18, 1, 8, 1], [5, 12, 1, 8, 1], [3, 7, 0, 8, 1], [9, 17, 0, 13, 1], [6, 13, 0, 10, 1], [6, 12, 1, 10, 1],
	#	[5, 15, 2, 6, 1], [0, 3, 1, 3, 0], [6, 13, 1, 8, 0], [12, 23, 1, 13, 0],
	#	[8, 19, 1, 7, 1], [5, 13, 1, 7, 1], [3, 8, 0, 7, 1], [9, 18, 0, 12, 1], [6, 14, 0, 9, 1], [6, 13, 1, 9, 1],
	#	[27, 45, 0, 2, 0], [3, 5, 0, 6, 0], [3, 6, 0, 5, 0]]	# C, H, N, O, P 

	hglist=['SM', 'CR', 'HC', 'DC',
		'TG', 'DG']		#
	hgflist=[[5, 15, 2, 6, 1], [0, 3, 1, 3, 0], [6, 13, 1, 8, 0], [12, 23, 1, 13, 0],
		[3, 5, 0, 6, 0], [3, 6, 0, 5, 0]]	# C, H, N, O, P 
	#(headgroup atoms; with O atoms of both the ester bond, and the other O atom of acyl FA rests)
	oxlist=[]
	oxhlist=[]
	oxolist=[]
	ionlist=['H', 'NH4', 'Na']		# do not modify, exclusion according to lipid class below
	mzmax=1200 	#according to acquisition
	################ DATABASE ## Source: Internetchemie.info
	#isotope=["1H", "2H", "12C", "13C", "14N", "15N", "16O", "17O", "18O", "19F", "23Na", "28Si", "29Si", "30Si", "31P", "32S", "33S", "34S", "36S", "39K", "40K", "41K", "35Cl", "37Cl", "79Br", "81Br"]
	#mass=[1.00783, 2.01410 , 12.00000, 13.00335, 14.00307, 15.00011, 15.99491, 16.99913, 17.99916, 18.99840, 22.97977, 27.97693, 28.97649, 29.97377, 30.97376, 31.97207, 32.97146, 33.96787, 35.96708, 38.96371, 39.96400, 40.96183, 34.96885, 36,96590, 78.91834, 80.91629]
	#abundance=[99.9885, 0.0115, 98.93, 1.07, 99.636, 0.364, 99.7, 0.04, 0.2, 100, 100, 92.233, 4.685, 3.092, 100, 94.93, 0.76, 4.29, 0.02, 93.2581, 0.0117, 6.7302, 75.76, 24.24, 50.69, 49.31]
	################
	mfacombilist=scufalist

	#begin build bfalist with sum compositional FA description in case of two FA (one from sfalist, one from scufalist)
	bfalist=[]
	bfacombilist=[]
	sfi=0
	while sfi<len(sfalist):
		sci=0
		while sci<len(scufalist):
			checklist=[]
			checklist.append(int(sfalist[sfi][0])+int(scufalist[sci][0]))
			checklist.append(int(sfalist[sfi][1])+int(scufalist[sci][1]))
			if checklist in bfalist:
				ok=1
				searchbfa=0
				gos=1
				while gos==1:
					if bfalist[searchbfa]==checklist:
						gos=0
						indexbfa=searchbfa
					else:
						gos=gos
					searchbfa=searchbfa+1
				
				iclist=[]
				iclist.append(sfalist[sfi])
				iclist.append(scufalist[sci])
				# begin check for sn isomers
				# generate all sn isomers and test if present in current combination collection, if yes, skip, else, append
				jclist=[]
				jclist.append(scufalist[sci])
				jclist.append(sfalist[sfi])
				snisolist=[]
				snisolist.append(iclist)
				snisolist.append(jclist)
				# end check for sn isomers
				ca=1
				pr=0
				while pr<len(bfacombilist[indexbfa]):
					if bfacombilist[indexbfa][pr] in snisolist:
						ca=0
					pr=pr+1
				# end check for sn isomers
				if ca==1:
					bfacombilist[indexbfa].append(iclist)
			else:
				bfalist.append(checklist)
				ccombilist=[]
				ccombilist.append(sfalist[sfi])
				ccombilist.append(scufalist[sci])
				jclist=[]
				jclist.append(ccombilist)
				bfacombilist.append(jclist)
			sci=sci+1
		sfi=sfi+1

	#print(bfalist)
	#print(len(bfalist))
	##print(len(bfacombilist))
	#quit()
	# end build bfalist with sum compositional FA description in case of 2FA (one from sfalist, one from scufalist)

	# begin build tfalist with sum compositional FA description in case of 3 FA (2 from sfalist, one from scufalist)
	tfalist=[]
	combilist=[]	# combinations of FAs for sum composition
	sfi=0
	while sfi<len(sfalist):
		sfit=0
		while sfit<len(sfalist):
			sci=0
			while sci<len(scufalist):
				checklist=[]
				checklist.append(int(sfalist[sfi][0])+int(sfalist[sfit][0])+int(scufalist[sci][0]))		# Number of FA C atoms in sum composition
				checklist.append(int(sfalist[sfi][1])+int(sfalist[sfit][1])+int(scufalist[sci][1]))		# Number of DB in sum composition
				if checklist in tfalist:
					ok=1
					searchtfa=0
					gos=1
					while gos==1:
						if tfalist[searchtfa]==checklist:
							gos=0
							indextfa=searchtfa
						else:
							gos=gos
						searchtfa=searchtfa+1
					
					iclist=[]
					iclist.append(sfalist[sfi])
					iclist.append(sfalist[sfit])
					iclist.append(scufalist[sci])
					# begin check for sn isomers
					# generate all sn isomers and test if present in current combination collection, if yes, skip, else, append
					jclist=[]
					jclist.append(sfalist[sfit])
					jclist.append(sfalist[sfi])
					jclist.append(scufalist[sci])
					kclist=[]
					kclist.append(scufalist[sci])
					kclist.append(sfalist[sfi])
					kclist.append(sfalist[sfit])
					lclist=[]
					lclist.append(scufalist[sci])
					lclist.append(sfalist[sfit])
					lclist.append(sfalist[sfi])
					mclist=[]
					mclist.append(sfalist[sfi])
					mclist.append(scufalist[sci])
					mclist.append(sfalist[sfit])
					nclist=[]
					nclist.append(sfalist[sfit])
					nclist.append(scufalist[sci])
					nclist.append(sfalist[sfi])
					snisolist=[]
					snisolist.append(iclist)
					snisolist.append(jclist)
					snisolist.append(kclist)
					snisolist.append(lclist)
					snisolist.append(mclist)
					snisolist.append(nclist)
					# end check for sn isomers
					ca=1
					pr=0
					while pr<len(combilist[indextfa]):
						if combilist[indextfa][pr] in snisolist:
							ca=0
						pr=pr+1
					# end check for sn isomers
					if ca==1:
						combilist[indextfa].append(iclist)
				else:
					tfalist.append(checklist)
					ccombilist=[]
					ccombilist.append(sfalist[sfi])
					ccombilist.append(sfalist[sfit])
					ccombilist.append(scufalist[sci])
					jclist=[]
					jclist.append(ccombilist)
					combilist.append(jclist)
				sci=sci+1
			sfit=sfit+1
		sfi=sfi+1

	##print(len(tfalist))
	#print(combilist)
	#print(len(combilist))
	#quit()
	# end build tfalist with sum compositional FA description in case of 3 FA (2 from sfalist, one from scufalist)

	print('Building transition list...')

	# begin build transitionlist (pos and neg)
	moleculegrouplist=[]
	precursornamelist=[]
	precursorformulalist=[]
	precursoradductlist=[]
	precursormzlist=[]
	precursorchargelist=[]
	productnamelist=[]
	productformulalist=[]
	productadductlist=[]
	productmzlist=[]
	productchargelist=[]

	# transition list negative mode
	nmoleculegrouplist=[]
	nprecursornamelist=[]
	nprecursorformulalist=[]
	nprecursoradductlist=[]
	nprecursormzlist=[]
	nprecursorchargelist=[]
	nproductnamelist=[]
	nproductformulalist=[]
	nproductadductlist=[]
	nproductmzlist=[]
	nproductchargelist=[]

	hgi=0						# head group index
	while hgi<len(hglist):

		bfalipids=['PC', 'PE', 'PA', 'PI', 'PG', 'PS', 'SM', 'CR', 'HC', 'DC', 'DG']			# determine, whether FA variation list needs to adapt to lipid class with 1, 2 or 3 FA per lipid
		if hglist[hgi] in bfalipids:
			favarlist=bfalist
		mfalipids=['LC', 'LE', 'LA', 'LI', 'LG', 'LS', 'CE']
		#elif hglist[hgi]=='CE':
		if hglist[hgi] in mfalipids:
			favarlist=scufalist
		elif hglist[hgi]=='TG':
			favarlist=tfalist

		fvi=0					# fatty acid variation index
		while fvi<len(favarlist):
			ioni=0				# ionization index
			while ioni<len(ionlist):
				# begin limit ionization type depending on lipid class (normal, unoxidized lipids)
				if hglist[hgi]=='TG':
					if ioni==0:
						ioni=ioni+1		# exclude H
					#elif ioni==2:
					#	ioni=ioni+1		# exclude Na		# exclusion below for Na
				elif hglist[hgi]=='DG':
					if ioni==0:
						ioni=ioni+1		# exclude H
				elif hglist[hgi]=='PC':
					if ioni==1:
						ioni=ioni+1		# exclude NH4 		# exclusion below for Na
				elif hglist[hgi]=='SM':
					if ioni==1:
						ioni=ioni+1		# exclude NH4 		# exclusion below for Na
				elif hglist[hgi]=='PE':
					if ioni==1:
						ioni=ioni+1		# exclude NH4
				elif hglist[hgi] in bfalipids:
					if ioni==1:
						ioni=ioni+1		# exclude NH4
				elif hglist[hgi] in mfalipids:
					if hglist[hgi]=='CE':
						if ioni==0:
							ioni=ioni+1		# exclude H
					else:
						if ioni==1:
							ioni=ioni+1		# exclude NH4
				# end limit ionization type depending on lipid class

				###################################################################################################################################
				# begin build neg mode PC Formate adduct and fragments				##### BEGIN NEG MODE TL
				cfamode=2
				if hglist[hgi]=='DG':
					cfamode=3
				elif hglist[hgi] in bfalipids:
					cfamode=2
				elif hglist[hgi] in mfalipids:
					cfamode=1
				formate=0
				formatelist=['PC', 'LC', 'PA', 'SM', 'CR', 'HC', 'DC']
				if hglist[hgi] in formatelist:
					formate=1
				else:
					formate=0
				if cfamode==2:
					if ioni==0:
						# begin build precursor, iterate through bfacombilist
						comb=0 					#combination index
						while comb<len(bfacombilist[fvi]):
							# begin build unoxidized precursor and fragments of current combination
							nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'_'+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+')')
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
							nprecursorformulalist.append(cprecformula)
							if formate==1:
								nprecursoradductlist.append('[M+HCOO]1-')
								cionmz=mzh+mzc+(2*mzo)+mze # Formate anion
								nproductadductlist.append('[M+HCOO]1-')
							else:
								nprecursoradductlist.append('[M-H]1-')
								cionmz=mze-mzh #+mzc+(2*mzo)+mze # -H anion
								nproductadductlist.append('[M-H]1-')
							
							cprecmz=round(0+cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
							nprecursormzlist.append(cprecmz)
							nprecursorchargelist.append('-1')
							nproductchargelist.append('-1') #
							nproductnamelist.append('precursor')						
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)

							qcheck=0
							if qcheck==1:
								if 'PG_42:5' in nprecursornamelist[len(nprecursornamelist)-1]:
									print('Built PG_42:5')
								if 'PG_41:5' in nprecursornamelist[len(nprecursornamelist)-1]:
									print('Built PG_41:5')
							# build fragments of current combination
							nfr=0		# neg mode fragment index
							sfr=7
							if str(hglist[hgi])=='SM':
								nfr=4
							elif str(hglist[hgi])=='HC':
								sfr=9
							elif str(hglist[hgi])=='DC':
								sfr=10
							while nfr<sfr:
								# non variable part of fragments
								nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'_'+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+')')
								nprecursorformulalist.append(cprecformula)
								nprecursoradductlist.append('[M+HCOO]1-')
								nprecursormzlist.append(cprecmz)
								nprecursorchargelist.append('-1')
								nproductchargelist.append('-1') 
								nproductadductlist.append('[M-H]1-') #
								nfr=nfr+1

							if hglist[hgi]=='SM':
								# build non-variable part of SM
								nproductnamelist.append('HG(PC,168)')
								nproductnamelist.append('P(79)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1]))

								cprecformula='C4H12NO4P'
								cprecmz=round(float(mzc*4+mzh*12+mzn+mzo*4+mzp-mzh), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								cprecformula='HO3P'
								cprecmz=round(float(mzh+(mzo*3)+mzp-mzh), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1]))
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str(chfa)+'O2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0])+mzh*(chfa-1)+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	###

								# begin enter swapped transition for SM, if FA1 is not FA2
								if str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])==str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1]):
									ok=1
								else:
									nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
									nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')')
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
									nprecursorformulalist.append(cprecformula)
									if formate==1:
										nprecursoradductlist.append('[M+HCOO]1-')
										cionmz=mzh+mzc+(2*mzo)+mze # Formate anion
										nproductadductlist.append('[M+HCOO]1-')
									else:
										nprecursoradductlist.append('[M-H]1-')
										cionmz=mze-mzh #+mzc+(2*mzo)+mze # -H anion
										nproductadductlist.append('[M-H]1-')
									
									cprecmz=round(0+cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
									nprecursormzlist.append(cprecmz)
									nprecursorchargelist.append('-1')
									nproductchargelist.append('-1') #
									nproductnamelist.append('precursor')						
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)

									nfr=4
									while nfr<7:
										# non variable part of fragments
										nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
										nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')')
										nprecursorformulalist.append(cprecformula)
										nprecursoradductlist.append('[M+HCOO]1-')
										nprecursormzlist.append(cprecmz)
										nprecursorchargelist.append('-1')
										nproductchargelist.append('-1') 
										nproductadductlist.append('[M-H]1-') #
										nfr=nfr+1
									
									# build non-variable part of SM
									nproductnamelist.append('HG(PC,168)')
									nproductnamelist.append('P(79)')
									nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1]))

									cprecformula='C4H12NO4P'
									cprecmz=round(float(mzc*4+mzh*12+mzn+mzo*4+mzp-mzh), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									cprecformula='HO3P'
									cprecmz=round(float(mzh+(mzo*3)+mzp-mzh), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1]))
									cprecformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str(chfa)+'O2'
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0])+mzh*(chfa-1)+mzo*2), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
								# end enter swapped transition for SM, if FA1 is not FA2
							elif hglist[hgi]=='CR':
								#	BUILD CERAMIDE VARIABLE TRANSITIONS
								nproductnamelist.append(str(hglist[hgi])+'-(HCOO)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-H6NO)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-CH3O)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-C2H8NO)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3N)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+HN)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3NO)')

								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3])+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)

								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])+2)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str(chfa)+'O'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0])+mzh*(chfa-1)+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz) # LCB
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-1)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])+4)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-2)+'H'+str(chfa)+'O'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-2)+mzh*(chfa-1)+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB

								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0])+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
							elif hglist[hgi]=='HC':
								#	BUILD HEXOSYLCERAMIDE VARIABLE TRANSITIONS
								nproductnamelist.append(str(hglist[hgi])+'-(HCOO)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,162)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,180)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-H6NO)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-CH3O)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-C2H8NO)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3N)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+HN)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3NO)')

								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3])+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-10
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-5)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-5)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-12
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-6)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-6)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)

								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])+2)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str(chfa)+'O'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0])+mzh*(chfa-1)+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz) # LCB
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-1)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])+4)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-2)+'H'+str(chfa)+'O'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-2)+mzh*(chfa-1)+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB

								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0])+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA


							elif hglist[hgi]=='DC':
								#	BUILD DIHEXOSYLCERAMIDE VARIABLE TRANSITIONS
								nproductnamelist.append(str(hglist[hgi])+'-(HCOO)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,162)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,180)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,324)')
								nproductnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,342)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-CH3O)')
								nproductnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'(-C2H8NO)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3N)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+HN)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'(+C2H3NO)')

								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3])+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-10
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-5)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-5)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-12
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-6)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-6)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)

								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-20
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-10)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-10)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-22
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-11)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-11)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)

								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-1)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1])+4)
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0]-2)+'H'+str(chfa)+'O'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0]-2)+mzh*(chfa-1)+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### LCB

								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-1)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str(chfa)+'NO'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0])+mzh*(chfa-1)+mzn+mzo), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1])-3)
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0]+2)+'H'+str(chfa)+'NO2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0]+2)+mzh*(chfa-1)+mzn+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	### FA
							else:
								# use hglist[hgi] instead of PC (CHECK WITH EACH LIPIDCLASS IS THIS CORRECT ???)
								nproductnamelist.append(str(hglist[hgi])+'-(CH3+HCOO)')
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1]))
								nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1]))
								nproductnamelist.append(str(hglist[hgi])+'-FA '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])) #+'(+HO)-(CH3+HCOO)')
								nproductnamelist.append(str(hglist[hgi])+'-FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])) #+'(+HO)-(CH3+HCOO)')
								nproductnamelist.append(str(hglist[hgi])+'-FA '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'*') #+'(-H)-(CH3+HCOO)')
								nproductnamelist.append(str(hglist[hgi])+'-FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'*') #+'(-H)-(CH3+HCOO)')
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-2
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3])+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(bfacombilist[fvi][comb][0][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][0][1]))
								cprecformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str(chfa)+'O2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][0][0])+mzh*(chfa-1)+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(bfacombilist[fvi][comb][1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][1][1]))
								cprecformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str(chfa)+'O2'
								cprecmz=round(float(mzc*(bfacombilist[fvi][comb][1][0])+mzh*(chfa-1)+mzo*2), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	###
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][0][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][0][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][0][1])))-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][0][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][0][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][0][1])))-1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][1][1])))-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][1][1])))-1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)	###
								chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][0][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][0][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][0][1])))+2-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2+1)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][0][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][0][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][0][1])))+1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2+1)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][1][1])))+2-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2+1)+'P'+str(hgflist[hgi][4])
								cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][1][1])))+1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2+1)+mzp*(hgflist[hgi][4])), 4)
								nproductformulalist.append(cprecformula)
								nproductmzlist.append(cprecmz)
								# end build unoxidized precursor and fragments of current combination

							# begin build ether lipid(s), unoxidized, if PC or PE
							buildether=0
							if hglist[hgi]=='PC':
								buildether=1
							elif hglist[hgi]=='PE':
								buildether=2			
							if buildether==1:			# build PC ether lipid transitions 
								bemode=5	# determine which and how many ether lipid combinations need to be created for the current FA combination
								qt=2
								nc1=int(bfacombilist[fvi][comb][0][0])
								ndb1=int(bfacombilist[fvi][comb][0][1])
								nc2=int(bfacombilist[fvi][comb][1][0])
								ndb2=int(bfacombilist[fvi][comb][1][1])
								if ndb1==0:
									if ndb2==0:
										if nc1==nc2:
											bemode=1
											qt=1
										else:
											bemode=2
									else:
										bemode=3
								elif ndb2==0:
									bemode=3
								elif nc1==nc2:
									if ndb1==ndb2:
										bemode=5
										qt=1
									else:
										bemode=4
								else:
									bemode=4
								
								#if bemode==1:	# sat = sat, two same saturated FA, create PC-O (OC) ether link, 1 ether lipid
								#if bemode==2: # sat + sat, two different saturated FA, create PC-O (OC)  ether link, 2 ether lipids
								#if bemode==3: # sat + unsat, two different FA, create PC-O (OC) and PC-O/P (OC) ether and ether or vinylether link, 2 ether lipids
								#if bemode==4: # unsat + unsat, two different unsaturated FA, create PC-O/P (OC) ether or vinylether link link, 2 ether lipids
								#if bemode==5: # unsat = unsat, two same unsaturated FA, create PC-O/P (QC) ether or vinylether link link, 1 ether lipid

								qi=0
								while qi<qt:
									if bemode==2:
										etype='O'
									if bemode==4:
										etype='Q'
									if bemode==3:
										if ndb1==0:
											if qi==0:
												etype='O'
											else:
												etype='Q'
										else:
											if qi==0:
												etype='Q'
											else:
												etype='O'
									if bemode==5:
										etype='Q'
									elif bemode==1:
										etype='O'
									swfa0=0
									swfa1=1
									if qi==0:
										# don't swap FA 
										swfa0=0
										swfa1=1
									elif qi==1:
										# swap FA 
										swfa0=1
										swfa1=0
									nmoleculegrouplist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
									nprecursornamelist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1])+'_'+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+')')	
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa+2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
									nprecursorformulalist.append(cprecformula)
									if formate==1:
										nprecursoradductlist.append('[M+HCOO]1-')
										cionmz=mzh+mzc+(2*mzo)+mze # Formate anion
										nproductadductlist.append('[M+HCOO]1-')
									else:
										nprecursoradductlist.append('[M-H]1-')
										cionmz=mze-mzh #+mzc+(2*mzo)+mze # -H anion
										nproductadductlist.append('[M-H]1-')					
									cprecmz=round(0+cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]+2))+(mzn*hgflist[hgi][2])+(mzo*(hgflist[hgi][3]-1))+(mzp*hgflist[hgi][4])), 4)
									nprecursormzlist.append(cprecmz)
									nprecursorchargelist.append('-1')
									nproductchargelist.append('-1') #
									nproductnamelist.append('precursor')						
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									# build fragments of current combination
									nfr=0		# neg mode fragment index
									while nfr<7:
										# non variable part of fragments
										nmoleculegrouplist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
										nprecursornamelist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1])+'_'+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+')')
										nprecursorformulalist.append(cprecformula)
										nprecursoradductlist.append('[M+HCOO]1-')
										nprecursormzlist.append(cprecmz)
										nprecursorchargelist.append('-1')
										nproductchargelist.append('-1') 
										nproductadductlist.append('[M-H]1-') #
										nfr=nfr+1
									# variable part of fragments
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-(CH3+HCOO)')
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-(FA+FA+CH3+HCOO)')
									nproductnamelist.append('FA_'+etype+' '+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1]))
									nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1]))
									nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+'*')
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])) #+'(+HO)-(CH3+HCOO)')
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+'*') #+'(-H)-(CH3+HCOO)')

									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-2		# PC-(CH3+HCOO)
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1)+'H'+str(hgflist[hgi][1]+chfa+2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
									cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1)+mzh*(hgflist[hgi][1]+chfa-1+2)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-1)+mzp*(hgflist[hgi][4])), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									if str(hglist[hgi][1])=='C':					# PC specific PC-(FA+FA+CH3+HCOO)
										nproductformulalist.append('C7H16NO5P')
										nproductmzlist.append(224.0693)
									#elif str(hglist[hgi][1])=='E':
									#	nproductformulalist.append('C7H16NO5P')
									#	nproductmzlist.append(224.0693)
									chfa=(((int(bfacombilist[fvi][comb][swfa0][0]))*2)+2)-(2*int(bfacombilist[fvi][comb][swfa0][1]))	# ether or vinyl ether acyl fragment
									cprecformula='C'+str(bfacombilist[fvi][comb][swfa0][0])+'H'+str(chfa)+'O'
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa0][0])+mzh*(chfa-1)+mzo), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									chfa=(((int(bfacombilist[fvi][comb][swfa1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][swfa1][1]))	# FA fragment
									cprecformula='C'+str(bfacombilist[fvi][comb][swfa1][0])+'H'+str(chfa)+'O2'
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa1][0])+mzh*(chfa-1)+mzo*2), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									chfa=(((int(bfacombilist[fvi][comb][swfa1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][swfa1][1]))	# FA fragment -CO2
									cprecformula='C'+str(bfacombilist[fvi][comb][swfa1][0]-1)+'H'+str(chfa)
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa1][0]-1)+mzh*(chfa-1)), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1+2		# PC-FA fragment
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][swfa1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2-1)+'P'+str(hgflist[hgi][4])
									cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][swfa1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))-1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2-1)+mzp*(hgflist[hgi][4])), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1+2		# PC-FA* fragment
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][swfa1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))+2-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2-1+1)+'P'+str(hgflist[hgi][4])
									cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-bfacombilist[fvi][comb][swfa1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))+1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2-1+1)+mzp*(hgflist[hgi][4])), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									#print('ether lipid built.')
									qi=qi+1
								# finished building PC ether lipid transitions
							if buildether==2:	#set to 2 to activate building of PE ether lipids		# changed back to OE and QE as data does not distinguish ether lipid and vinyl ether lipid for PEs
								bemode=5	# determine which and how many ether lipid combinations need to be created for the current FA combination
								qt=4
								nc1=int(bfacombilist[fvi][comb][0][0])
								ndb1=int(bfacombilist[fvi][comb][0][1])
								nc2=int(bfacombilist[fvi][comb][1][0])
								ndb2=int(bfacombilist[fvi][comb][1][1])
								if ndb1==0:
									if ndb2==0:
										if nc1==nc2:
											bemode=1
											qt=1
										else:
											bemode=2
											qt=2
									else:
										bemode=3	# sat + unsat
										qt=2 #3
								elif ndb2==0:
									bemode=3	# unsat + sat
									qt=2 #3
								elif nc1==nc2:
									if ndb1==ndb2:
										bemode=5
										qt=1 #2
									else:
										bemode=4
										qt=2 #4
								else:
									bemode=4
									qt=2 #4
								
								#if bemode==1:	# sat = sat, two same saturated FA, create PE-O (OE) ether link, 1 ether lipid
								#if bemode==2: # sat + sat, two different saturated FA, create PE-O (OE)  ether link, 2 ether lipids
								#if bemode==3: # sat + unsat, two different FA, create PE-O (OE) and PE-O/P (OE)  ether and ether or vinylether link, 3 ether lipids
								#if bemode==4: # unsat + unsat, two different unsaturated FA, create PE-O and PE-P (OE and VE)  ether or vinylether link link, 4 ether lipids
								#if bemode==5: # unsat = unsat, two same unsaturated FA, create PE-O and PE-P (OE and VE)  ether or vinylether link link, 2 ether lipids
								
								qi=0
								while qi<qt:
									swfa0=0		# default don't swap FA
									swfa1=1
									if bemode==1:
										etype='O'
									if bemode==2:
										etype='O'
										if qi==1:
											swfa0=1 # swap FA 
											swfa1=0
									if bemode==3:
										if ndb1==0:
											if qi==0:
												etype='O'
											elif qi==1:
												etype='Q'
												swfa0=1  # swap FA 
												swfa1=0
											elif qi==2:
												etype='Q'						
												swfa0=1  # swap FA 
												swfa1=0
										else:
											if qi==0:
												etype='O'
											elif qi==1:
												etype='Q'
											elif qi==2:
												etype='Q'
												swfa0=1 # swap FA 
												swfa1=0
									if bemode==4:
										if qi==0:
											etype='Q'
										elif qi==1:
											etype='Q'
											swfa0=1 # swap FA 
											swfa1=0
										elif qi==2:
											etype='Q'
										elif qi==3:
											etype='Q'
											swfa0=1 # swap FA 
											swfa1=0
									if bemode==5:
										if qi==0:
											etype='Q'
										elif qi==1:
											etype='Q'

									nmoleculegrouplist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
									nprecursornamelist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1])+'_'+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+')')	
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa+2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
									nprecursorformulalist.append(cprecformula)
									if formate==1:
										nprecursoradductlist.append('[M+HCOO]1-')
										cionmz=mzh+mzc+(2*mzo)+mze # Formate anion
										nproductadductlist.append('[M+HCOO]1-')
									else:
										nprecursoradductlist.append('[M-H]1-')
										cionmz=mze-mzh #+mzc+(2*mzo)+mze # -H anion
										nproductadductlist.append('[M-H]1-')					
									cprecmz=round(0+cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]+2))+(mzn*hgflist[hgi][2])+(mzo*(hgflist[hgi][3]-1))+(mzp*hgflist[hgi][4])), 4)
									nprecursormzlist.append(cprecmz)
									nprecursorchargelist.append('-1')
									nproductchargelist.append('-1') #
									nproductnamelist.append('precursor')						
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									# build fragments of current combination
									nfr=0		# neg mode fragment index
									while nfr<6:
										# non variable part of fragments
										nmoleculegrouplist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
										nprecursornamelist.append(etype+str(hglist[hgi][1])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1])+'_'+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+')')
										nprecursorformulalist.append(cprecformula)
										nprecursoradductlist.append('[M+HCOO]1-')
										nprecursormzlist.append(cprecmz)
										nprecursorchargelist.append('-1')
										nproductchargelist.append('-1') 
										nproductadductlist.append('[M-H]1-') #
										nfr=nfr+1
									# variable part of fragments
									
									# begin ether type dependent fragments
									if etype=='O':
										nproductnamelist.append('GP(153)')
										nproductformulalist.append('C3H7O5P')
										nproductmzlist.append(152.9958)
										nproductnamelist.append('GP(135)')
										nproductformulalist.append('C3H5O4P')
										nproductmzlist.append(134.9853)
									elif etype=='Q':
										nproductnamelist.append('HG (PE, 196)')
										nproductformulalist.append('C5H12NO5P')
										nproductmzlist.append(196.0380)
										nproductnamelist.append('FA_'+etype+' '+str(bfacombilist[fvi][comb][swfa0][0])+':'+str(bfacombilist[fvi][comb][swfa0][1]))
										chfa=(((int(bfacombilist[fvi][comb][swfa0][0]))*2)+2)-(2*int(bfacombilist[fvi][comb][swfa0][1]))	# ether or vinyl ether acyl fragment
										cprecformula='C'+str(bfacombilist[fvi][comb][swfa0][0])+'H'+str(chfa)+'O'
										cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa0][0])+mzh*(chfa-1)+mzo), 4)
										nproductformulalist.append(cprecformula)
										nproductmzlist.append(cprecmz)
									# end ether type dependent fragments

									nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1]))
									nproductnamelist.append('FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+'*')
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])) #+'(+HO)-(CH3+HCOO)')
									nproductnamelist.append(etype+str(hglist[hgi][1])+'-FA '+str(bfacombilist[fvi][comb][swfa1][0])+':'+str(bfacombilist[fvi][comb][swfa1][1])+'*') #+'(-H)-(CH3+HCOO)')

									chfa=(((int(bfacombilist[fvi][comb][swfa1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][swfa1][1]))	# FA fragment
									cprecformula='C'+str(bfacombilist[fvi][comb][swfa1][0])+'H'+str(chfa)+'O2'
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa1][0])+mzh*(chfa-1)+mzo*2), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									chfa=(((int(bfacombilist[fvi][comb][swfa1][0])-2)*2)+4)-(2*int(bfacombilist[fvi][comb][swfa1][1]))	# FA fragment -CO2
									cprecformula='C'+str(bfacombilist[fvi][comb][swfa1][0]-1)+'H'+str(chfa)
									cprecmz=round(float(mzc*(bfacombilist[fvi][comb][swfa1][0]-1)+mzh*(chfa-1)), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1+2		# PC-FA fragment
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][swfa1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2-1)+'P'+str(hgflist[hgi][4])
									cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][swfa1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))-1-2)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2-1)+mzp*(hgflist[hgi][4])), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)
									chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1+2		# PC-FA* fragment
									cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][swfa1][0])+'H'+str(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))+2-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2-1+1)+'P'+str(hgflist[hgi][4])
									cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][swfa1][0])+mzh*(hgflist[hgi][1]+chfa-(((bfacombilist[fvi][comb][swfa1][0]-2)*2)+2-(2*(bfacombilist[fvi][comb][swfa1][1])))+1-2)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2-1+1)+mzp*(hgflist[hgi][4])), 4)
									nproductformulalist.append(cprecformula)
									nproductmzlist.append(cprecmz)	###
									#print('PE ether lipid built.')
									qi=qi+1
								# finished building PE ether lipid transitions

							# end build ether lipid(s), unoxidized, if PC or PE
							comb=comb+1
				if cfamode==1:
					if ioni==0:
						# begin build precursor, iterate through mfacombilist 
						comb=0 					#combination index
						while comb<1: #len(mfacombilist[fvi]):
							# begin build unoxidized precursor and fragments of current combination
							nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
							nprecursorformulalist.append(cprecformula)
							if formate==1:
								nprecursoradductlist.append('[M+HCOO]1-')
								cionmz=mzh+mzc+(2*mzo)+mze # Formate anion
								nproductadductlist.append('[M+HCOO]1-')
							else:
								nprecursoradductlist.append('[M-H]1-')
								cionmz=mze-mzh #+mzc+(2*mzo)+mze # -H anion
								nproductadductlist.append('[M-H]1-')
							
							cprecmz=round(0+cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
							nprecursormzlist.append(cprecmz)
							nprecursorchargelist.append('-1')
							nproductchargelist.append('-1') #
							nproductnamelist.append('precursor')						
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							# build fragments of current combination
							nfr=0		# neg mode fragment index
							while nfr<7:
								# non variable part of fragments
								nmoleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								nprecursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								nprecursorformulalist.append(cprecformula)
								nprecursoradductlist.append('[M+HCOO]1-')
								nprecursormzlist.append(cprecmz)
								nprecursorchargelist.append('-1')
								nproductchargelist.append('-1') 
								nproductadductlist.append('[M-H]1-') #
								nfr=nfr+1
							nproductnamelist.append(str(hglist[hgi])+'-(CH3+HCOO)')
							nproductnamelist.append('FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1]))
							nproductnamelist.append('FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1]))
							nproductnamelist.append(str(hglist[hgi])+'-FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1])) #+'(+HO)-(CH3+HCOO)')
							nproductnamelist.append(str(hglist[hgi])+'-FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1])) #+'(+HO)-(CH3+HCOO)')
							nproductnamelist.append(str(hglist[hgi])+'-FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1])+'*') #+'(-H)-(CH3+HCOO)')
							nproductnamelist.append(str(hglist[hgi])+'-FA '+str(mfacombilist[fvi][0])+':'+str(mfacombilist[fvi][1])+'*') #+'(-H)-(CH3+HCOO)')
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1-2
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1)+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
							cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1)+mzh*(hgflist[hgi][1]+chfa-1)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3])+mzp*(hgflist[hgi][4])), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							chfa=(((int(mfacombilist[fvi][0])-2)*2)+4)-(2*int(mfacombilist[fvi][1]))
							cprecformula='C'+str(mfacombilist[fvi][0])+'H'+str(chfa)+'O2'
							cprecmz=round(float(mzc*(mfacombilist[fvi][0])+mzh*(chfa-1)+mzo*2), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							chfa=(((int(mfacombilist[fvi][0])-2)*2)+4)-(2*int(mfacombilist[fvi][1]))
							cprecformula='C'+str(mfacombilist[fvi][0])+'H'+str(chfa)+'O2'
							cprecmz=round(float(mzc*(mfacombilist[fvi][0])+mzh*(chfa-1)+mzo*2), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)	###
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
							cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))-1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2)+mzp*(hgflist[hgi][4])), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
							cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))-1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2)+mzp*(hgflist[hgi][4])), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)	###
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))+2-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2+1)+'P'+str(hgflist[hgi][4])
							cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))+1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2+1)+mzp*(hgflist[hgi][4])), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))+2-4)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2+1)+'P'+str(hgflist[hgi][4])
							cprecmz=round(float(mzc*(hgflist[hgi][0]+favarlist[fvi][0]-1-mfacombilist[fvi][0])+mzh*(hgflist[hgi][1]+chfa-(((mfacombilist[fvi][0]-2)*2)+2-(2*(mfacombilist[fvi][1])))+1-4)+mzn*(hgflist[hgi][2])+mzo*(hgflist[hgi][3]-2+1)+mzp*(hgflist[hgi][4])), 4)
							nproductformulalist.append(cprecformula)
							nproductmzlist.append(cprecmz)
							# end build unoxidized precursor and fragments of current combination
							comb=comb+1
				# end build neg mode PC Formate adduct and fragments		##### END NEG MODE TL
				########################################################################################################################### END NEG MODE TL
				###########################################################################################################################

				###########################################################################################################################
				########################################################################################################################### BEGIN POS MODE TL
				#  begin add unoxidized lipid, positive mode		#
				# begin add precursor of unoxidized lipid
				comb=0
				if hglist[hgi] in bfalipids:
					combcut=len(bfacombilist[fvi])
				elif hglist[hgi]=='TG':
					combcut=1 #len(combilist[fvi])
				while comb<combcut:
					qch=0
					if qch==1:
						print(comb)
						#print(bfacombilist)
						print(fvi)
						print(hglist[hgi])
						#print(bfalist)

					if hglist[hgi] in bfalipids:
						comb=comb
					else:
						comb=combcut+1
					#begin build transitions (use comb only for lipids with two FA; TG uses comx later)
					moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
					precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])) # individual FA information added below (depending on TG or bis FA lipid)
					if hglist[hgi]=='CE':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))
					elif hglist[hgi]=='DG':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					elif hglist[hgi]=='SM':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					elif hglist[hgi]=='CR':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					elif hglist[hgi]=='HC':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					elif hglist[hgi]=='DC':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					elif hglist[hgi]=='TG':
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-2
						precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1])+'_'+str(combilist[fvi][0][1][0])+':'+str(combilist[fvi][0][1][1])+'_'+str(combilist[fvi][0][2][0])+':'+str(combilist[fvi][0][2][1])+')'
					else:
						if str(hglist[hgi][0])=='L':
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))	# correct number of H for Lyso species in pos mode
						else:
							chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1

					if hglist[hgi] in bfalipids:
						precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'_'+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+')'
					

					cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
					precursorformulalist.append(cprecformula)
					precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
					if ionlist[ioni]=='H':
						cionmz=mzh-mze
					elif ionlist[ioni]=='NH4':
						cionmz=(mzh*4)+mzn-mze
					elif ionlist[ioni]=='Na':
						cionmz=mzna-mze
					cprecmz=round(cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
					ccprecmz=cprecmz-cionmz
					precursormzlist.append(cprecmz)
					precursorchargelist.append('1')
					productnamelist.append('precursor')
					productformulalist.append(cprecformula)
					productadductlist.append('[M+'+ionlist[ioni]+']1+')
					productmzlist.append(cprecmz)
					productchargelist.append('1')
					# end add precursor of unoxidized lipid

					# begin add HG and other fragments specific for lipid class
					infr=0
					if hglist[hgi]=='SM':		# 2 product fragments for Sphingomyelins	
						inft=2
					elif hglist[hgi]=='CR':		# 4 product fragments for Ceramides	
						inft=4
					elif hglist[hgi]=='HC':		# 7 product fragments for Hexosylceramides	
						inft=7
					elif hglist[hgi]=='DC':		# 7 product fragments for Dihexosylceramides
						inft=7
					elif hglist[hgi]=='DG':		# 3 product fragments for Diacylglycerols
						inft=3
					else:
						inft=1
					while infr<inft:
						moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
						precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
						if hglist[hgi] in bfalipids:
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+'_'+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+')'
						precursorformulalist.append(cprecformula)
						precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
						precursormzlist.append(cprecmz)
						precursorchargelist.append('1')
						productchargelist.append('1')
						infr=infr+1
					if hglist[hgi]=='PC':	# variable part for products
						productnamelist.append('HG(PC,184.0733)')
						productformulalist.append('C5H14NO4P')
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(184.0733),4))
					elif hglist[hgi]=='PE':		# -141.0191 (-HG(PE)), -C2H8NO4P
						productnamelist.append('PE-HG(PE-141.0191)')
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-2)+'H'+str(hgflist[hgi][1]+chfa-8)+'N'+str(hgflist[hgi][2]-1)+'O'+str(hgflist[hgi][3]-4)+'P'+str(hgflist[hgi][4]-1)
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(ccprecmz-141.0191+mzh-mze),4))
					elif hglist[hgi]=='CE':		# -FA
						productnamelist.append('CE-FA,-(OH)')
						productformulalist.append('C27H44')
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(369.3516),4))
					elif hglist[hgi]=='SM':	
						productnamelist.append('HG(PC,184)')					# 
						productformulalist.append('C5H14NO4P')
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(184.0733),4))
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1]))					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
					elif hglist[hgi]=='CR':
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)+1-(bfacombilist[fvi][comb][0][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)+2-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][0][0])-1))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						# begin add flipped lipid (swapped FAs)
						#begin add precursor
						moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
						precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])) # individual FA information added below (depending on TG or bis FA lipid)
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
						if hglist[hgi] in bfalipids:
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
						precursorformulalist.append(cprecformula)
						precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
						if ionlist[ioni]=='H':
							cionmz=mzh-mze
						elif ionlist[ioni]=='NH4':
							cionmz=(mzh*4)+mzn-mze
						elif ionlist[ioni]=='Na':
							cionmz=mzna-mze
						cprecmz=round(cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
						ccprecmz=cprecmz-cionmz
						precursormzlist.append(cprecmz)
						precursorchargelist.append('1')
						productnamelist.append('precursor')
						productformulalist.append(cprecformula)
						productadductlist.append('[M+'+ionlist[ioni]+']1+')
						productmzlist.append(cprecmz)
						productchargelist.append('1')
						# end add precursor
						infr=0
						while infr<inft:
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							if hglist[hgi] in bfalipids:
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')
							infr=infr+1
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)+1-(bfacombilist[fvi][comb][1][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)+2-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0]-1)+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][1][0])-1))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						# end add flipped lipid (swapped FAs)
						# adjust product fragments 
					elif hglist[hgi]=='HC':
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)+1-(bfacombilist[fvi][comb][0][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)+2-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][0][0])-1))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,180)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-12)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-6)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-11))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-6))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,198)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-14)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-7)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-13))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-7))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,162)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-10)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-5)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-9))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-5))), 4)
						productmzlist.append(cprodmz)
						# begin add flipped lipid (swapped FAs)
						#begin add precursor
						moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
						precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])) # individual FA information added below (depending on TG or bis FA lipid)
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
						if hglist[hgi] in bfalipids:
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
						precursorformulalist.append(cprecformula)
						precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
						if ionlist[ioni]=='H':
							cionmz=mzh-mze
						elif ionlist[ioni]=='NH4':
							cionmz=(mzh*4)+mzn-mze
						elif ionlist[ioni]=='Na':
							cionmz=mzna-mze
						cprecmz=round(cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
						ccprecmz=cprecmz-cionmz
						precursormzlist.append(cprecmz)
						precursorchargelist.append('1')
						productnamelist.append('precursor')
						productformulalist.append(cprecformula)
						productadductlist.append('[M+'+ionlist[ioni]+']1+')
						productmzlist.append(cprecmz)
						productchargelist.append('1')
						# end add precursor
						infr=0
						while infr<inft:
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							if hglist[hgi] in bfalipids:
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')
							infr=infr+1
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)+1-(bfacombilist[fvi][comb][1][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)+2-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0]-1)+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][1][0])-1))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,180)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-12)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-6)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-11))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-6))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,198)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-14)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-7)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-13))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-7))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('HC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,162)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-6)+'H'+str(hgflist[hgi][1]+chfa-10)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-5)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-6)+(mzh*(hgflist[hgi][1]+chfa-9))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-5))), 4)
						productmzlist.append(cprodmz)
						# end add flipped lipid (swapped FAs)
						# adjust product fragments 
					elif hglist[hgi]=='DC':
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)+1-(bfacombilist[fvi][comb][0][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)+2-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0])+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][0][0]))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][0][0]-1)+'H'+str((bfacombilist[fvi][comb][0][0]*2)-1-(bfacombilist[fvi][comb][0][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][0][0])-1))+(mzh*((bfacombilist[fvi][comb][0][0]*2)-(bfacombilist[fvi][comb][0][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,342)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-22)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-11)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-21))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-11))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,360)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-24)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-12)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-23))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-12))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,324)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-20)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-10)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-19))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-10))), 4)
						productmzlist.append(cprodmz)
						# begin add flipped lipid (swapped FAs)
						#begin add precursor
						moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
						precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])) # individual FA information added below (depending on TG or bis FA lipid)
						chfa=(((int(favarlist[fvi][0])-2)*2)+3)-(2*int(favarlist[fvi][1]))-1
						if hglist[hgi] in bfalipids:
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3])+'P'+str(hgflist[hgi][4])
						precursorformulalist.append(cprecformula)
						precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
						if ionlist[ioni]=='H':
							cionmz=mzh-mze
						elif ionlist[ioni]=='NH4':
							cionmz=(mzh*4)+mzn-mze
						elif ionlist[ioni]=='Na':
							cionmz=mzna-mze
						cprecmz=round(cionmz+float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]))+(mzh*(chfa+hgflist[hgi][1]))+(mzn*hgflist[hgi][2])+(mzo*hgflist[hgi][3])+(mzp*hgflist[hgi][4])), 4)
						ccprecmz=cprecmz-cionmz
						precursormzlist.append(cprecmz)
						precursorchargelist.append('1')
						productnamelist.append('precursor')
						productformulalist.append(cprecformula)
						productadductlist.append('[M+'+ionlist[ioni]+']1+')
						productmzlist.append(cprecmz)
						productchargelist.append('1')
						# end add precursor
						infr=0
						while infr<inft:
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							if hglist[hgi] in bfalipids:
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+'_'+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1])+')'
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')
							infr=infr+1
						productnamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+' -(H2O,18)')	# MODIFY
						cprecformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cprecformula)
						productadductlist.append('[M+H]1+')
						cprodmz=cprecmz-(2*mzh+mzo)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-HO)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)+1-(bfacombilist[fvi][comb][1][1]*2))+'NO'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)+2-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)+mzo), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-H3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0])+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(bfacombilist[fvi][comb][1][0]))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('LCB '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1])+';2(-CH3O2)')					# 
						cpeformula='C'+str(bfacombilist[fvi][comb][1][0]-1)+'H'+str((bfacombilist[fvi][comb][1][0]*2)-1-(bfacombilist[fvi][comb][1][1]*2))+'N'
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*((bfacombilist[fvi][comb][1][0])-1))+(mzh*((bfacombilist[fvi][comb][1][0]*2)-(bfacombilist[fvi][comb][1][1]*2)))+(mzn)), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,342)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-22)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-11)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-21))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-11))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,360)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-24)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-12)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-23))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-12))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DC_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-HG(Hex,324)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-12)+'H'+str(hgflist[hgi][1]+chfa-20)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-10)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-12)+(mzh*(hgflist[hgi][1]+chfa-19))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-10))), 4)
						productmzlist.append(cprodmz)
						# begin add flipped lipid (swapped FAs)
						# adjust product fragments
					elif hglist[hgi]=='DG':
						productnamelist.append('DG_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-(H2O+NH3,35)')					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0])+'H'+str(hgflist[hgi][1]+chfa-2)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-1)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0])+(mzh*(hgflist[hgi][1]+chfa-1))+(mzn*hgflist[hgi][2])+mzo*(hgflist[hgi][3]-1))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DG_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-FA '+str(bfacombilist[fvi][comb][0][0])+':'+str(bfacombilist[fvi][comb][0][1]))					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][0][0])+'H'+str(hgflist[hgi][1]+chfa-(2*int(bfacombilist[fvi][comb][0][0])-(2*int(bfacombilist[fvi][comb][0][1]))))+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][0][0])+(mzh*(hgflist[hgi][1]+chfa+1-(2*int(bfacombilist[fvi][comb][0][0])-(2*int(bfacombilist[fvi][comb][0][1])))))+(mzn*(hgflist[hgi][2]))+mzo*(hgflist[hgi][3]-2))), 4)
						productmzlist.append(cprodmz)
						productnamelist.append('DG_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'-FA '+str(bfacombilist[fvi][comb][1][0])+':'+str(bfacombilist[fvi][comb][1][1]))					# 
						cpeformula='C'+str(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][1][0])+'H'+str(hgflist[hgi][1]+chfa-(2*int(bfacombilist[fvi][comb][1][0])-(2*int(bfacombilist[fvi][comb][1][1]))))+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
						productformulalist.append(cpeformula)
						productadductlist.append('[M+H]1+')
						cprodmz=round(float((mzc*(hgflist[hgi][0]+favarlist[fvi][0]-bfacombilist[fvi][comb][1][0])+(mzh*(hgflist[hgi][1]+chfa+1-(2*int(bfacombilist[fvi][comb][1][0])-(2*int(bfacombilist[fvi][comb][1][1])))))+(mzn*(hgflist[hgi][2]))+mzo*(hgflist[hgi][3]-2))), 4)
						productmzlist.append(cprodmz)

					elif hglist[hgi] in bfalipids:							# 
						productnamelist.append('HG(DUMMY)')					# 
						productformulalist.append('C5H14NO4P')
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(184.0733),4))
					elif hglist[hgi] in mfalipids:							# 
						productnamelist.append('HG(DUMMY)')					# 
						productformulalist.append('C5H14NO4P')
						productadductlist.append('[M+H]1+')
						productmzlist.append(round(float(184.0733),4))
					elif hglist[hgi]=='TG':		# add first combination in combilist, later add other combinations accordingly with precursor line
						precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1])+'_'+str(combilist[fvi][0][1][0])+':'+str(combilist[fvi][0][1][1])+'_'+str(combilist[fvi][0][2][0])+':'+str(combilist[fvi][0][2][1])+')'
						productnamelist.append('FA '+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1]))		# add first line (FA#1)
						productformulalist.append('C'+str(combilist[fvi][0][0][0])+'H'+str((combilist[fvi][0][0][0]-2)*2+4-(2*combilist[fvi][0][0][1])-2)+'O') # add first line (FA#1)
						productadductlist.append('[M+H]1+') # add first line (FA#1)
						productmzlist.append(round(float((mzh-mze+mzc*float(combilist[fvi][0][0][0]))+(mzh*float((combilist[fvi][0][0][0]-2)*2+4-(2*combilist[fvi][0][0][1])-2))+(mzo)),4)) # add first line (FA#1)
						ffa=1	# index for finding FA in first combination
						while ffa<3:
							#add other FA fragments for first combination
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1])+'_'+str(combilist[fvi][0][1][0])+':'+str(combilist[fvi][0][1][1])+'_'+str(combilist[fvi][0][2][0])+':'+str(combilist[fvi][0][2][1])+')'
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')	#
							productnamelist.append('FA '+str(combilist[fvi][0][ffa][0])+':'+str(combilist[fvi][0][ffa][1]))		# add first combination (FA#2,3)
							productformulalist.append('C'+str(combilist[fvi][0][ffa][0])+'H'+str((combilist[fvi][0][ffa][0]-2)*2+4-(2*combilist[fvi][0][ffa][1])-2)+'O') # add first combination (FA#2,3)
							productadductlist.append('[M+H]1+') # add first line (FA#2,3)
							productmzlist.append(round(float((mzh-mze+mzc*float(combilist[fvi][0][ffa][0]))+(mzh*float((combilist[fvi][0][ffa][0]-2)*2+4-(2*combilist[fvi][0][ffa][1])-2))+(mzo)),4)) # add first combination (FA#2,3)
							ffa=ffa+1
						gfa=0
						while gfa<3:
							#add fragments from FA removal from first combination
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1])+'_'+str(combilist[fvi][0][1][0])+':'+str(combilist[fvi][0][1][1])+'_'+str(combilist[fvi][0][2][0])+':'+str(combilist[fvi][0][2][1])+')'
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')	#
							productnamelist.append('TG-FA '+str(combilist[fvi][0][gfa][0])+':'+str(combilist[fvi][0][gfa][1]))		# add first combination (-FA#1,2,3)
							cfnc=str(hgflist[hgi][0]+favarlist[fvi][0]-int(combilist[fvi][0][gfa][0]))
							cfnh=str(hgflist[hgi][1]+chfa-int(((combilist[fvi][0][gfa][0]-2)*2)+3-combilist[fvi][0][gfa][1]*2))
							cprodformula='C'+str(cfnc)+'H'+str(cfnh)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
							productformulalist.append(cprodformula) # add first combination (-FA#1,2,3) ##
							productadductlist.append('[M+H]1+') # add first combination (-FA#1,2,3)
							productmzlist.append(round(float((mzc*float(cfnc))+(mzh*float(cfnh))+(4*mzo)),4)) # add first combination (-FA#1,2,3)
							gfa=gfa+1
						if ioni==2:
							# add [TG-FA +Na]+ fragments
							nfa=0
							while nfa<3:
								#add fragments from FA removal from first combination
								moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][0][0][0])+':'+str(combilist[fvi][0][0][1])+'_'+str(combilist[fvi][0][1][0])+':'+str(combilist[fvi][0][1][1])+'_'+str(combilist[fvi][0][2][0])+':'+str(combilist[fvi][0][2][1])+')'
								precursorformulalist.append(cprecformula)
								precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
								precursormzlist.append(cprecmz)
								precursorchargelist.append('1')
								productchargelist.append('1')	#
								productnamelist.append('TG(Na)-FA '+str(combilist[fvi][0][nfa][0])+':'+str(combilist[fvi][0][nfa][1]))		# add first combination (-FA#1,2,3)
								cfnc=str(hgflist[hgi][0]+favarlist[fvi][0]-int(combilist[fvi][0][nfa][0]))
								cfnh=str(hgflist[hgi][1]+chfa-int(((combilist[fvi][0][nfa][0]-2)*2)+3-combilist[fvi][0][nfa][1]*2)-1)
								cprodformula='C'+str(cfnc)+'H'+str(cfnh)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
								productformulalist.append(cprodformula) # add first combination (-FA#1,2,3) ##
								productadductlist.append('[M+Na]1+') # add first combination (-FA#1,2,3)
								productmzlist.append(round(float((mzc*float(cfnc))+(mzh*(float(cfnh)-0))+(4*mzo)+mzna),4)) # add first combination (-FA#1,2,3)
								nfa=nfa+1

						# Other combinations according to combilist (incl. precursor line each)
						comx=1 #00
						while comx<len(combilist[fvi]):
							#print('########')
							#print(comx)
							#print(combilist[fvi])
							#print(len(combilist[fvi]))
							#print('____________')
							#precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')'
							# add precursor of this combination
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')')
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')
							#
							productnamelist.append('precursor')
							productformulalist.append(cprecformula)
							productadductlist.append('[M+'+ionlist[ioni]+']1+')
							productmzlist.append(cprecmz)
							#add first FA (fragments)
							moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
							precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')')
							precursorformulalist.append(cprecformula)
							precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
							precursormzlist.append(cprecmz)
							precursorchargelist.append('1')
							productchargelist.append('1')

							productnamelist.append('FA '+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1]))		# add first line (FA#1)
							productformulalist.append('C'+str(combilist[fvi][comx][0][0])+'H'+str((combilist[fvi][comx][0][0]-2)*2+4-(2*combilist[fvi][comx][0][1])-2)+'O') # add first line (FA#1)
							productadductlist.append('[M+H]1+') # add first line (FA#1)
							productmzlist.append(round(float((mzh-mze+mzc*float(combilist[fvi][comx][0][0]))+(mzh*float((combilist[fvi][comx][0][0]-2)*2+4-(2*combilist[fvi][comx][0][1])-2))+(mzo)),4)) # add first line (FA#1)
							ffa=1	# index for finding FA in first combination
							while ffa<3:
								#add other FA fragments for first combination
								moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')'
								precursorformulalist.append(cprecformula)
								precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
								precursormzlist.append(cprecmz)
								precursorchargelist.append('1')
								productchargelist.append('1')	#
								productnamelist.append('FA '+str(combilist[fvi][comx][ffa][0])+':'+str(combilist[fvi][comx][ffa][1]))		# add first combination (FA#2,3)
								productformulalist.append('C'+str(combilist[fvi][comx][ffa][0])+'H'+str((combilist[fvi][comx][ffa][0]-2)*2+4-(2*combilist[fvi][comx][ffa][1])-2)+'O') # add first combination (FA#2,3)
								productadductlist.append('[M+H]1+') # add first line (FA#2,3)
								productmzlist.append(round(float((mzh-mze+mzc*float(combilist[fvi][comx][ffa][0]))+(mzh*float((combilist[fvi][comx][ffa][0]-2)*2+4-(2*combilist[fvi][comx][ffa][1])-2))+(mzo)),4)) # add first combination (FA#2,3)
								ffa=ffa+1
							gfa=0
							while gfa<3:
								#add fragments from FA removal from first combination
								moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
								precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')'
								precursorformulalist.append(cprecformula)
								precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
								precursormzlist.append(cprecmz)
								precursorchargelist.append('1')
								productchargelist.append('1')	#
								productnamelist.append('TG-FA '+str(combilist[fvi][comx][gfa][0])+':'+str(combilist[fvi][comx][gfa][1]))		# add first combination (-FA#1,2,3)
								cfnc=str(hgflist[hgi][0]+favarlist[fvi][0]-int(combilist[fvi][comx][gfa][0]))
								cfnh=str(hgflist[hgi][1]+chfa-int(((combilist[fvi][comx][gfa][0]-2)*2)+3-combilist[fvi][comx][gfa][1]*2))
								cprodformula='C'+str(cfnc)+'H'+str(cfnh)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
								productformulalist.append(cprodformula) # add first combination (-FA#1,2,3) ##
								productadductlist.append('[M+H]1+') # add first combination (-FA#1,2,3)
								productmzlist.append(round(float((mzc*float(cfnc))+(mzh*float(cfnh))+(4*mzo)),4)) # add first combination (-FA#1,2,3)
								gfa=gfa+1
							if ioni==2:
								# add [TG-FA +Na]+ fragments
								nfa=0
								while nfa<3:
									moleculegrouplist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
									precursornamelist.append(str(hglist[hgi])+'_'+str(favarlist[fvi][0])+':'+str(favarlist[fvi][1]))
									precursornamelist[len(precursornamelist)-1]=str(precursornamelist[len(precursornamelist)-1])+'_('+str(combilist[fvi][comx][0][0])+':'+str(combilist[fvi][comx][0][1])+'_'+str(combilist[fvi][comx][1][0])+':'+str(combilist[fvi][comx][1][1])+'_'+str(combilist[fvi][comx][2][0])+':'+str(combilist[fvi][comx][2][1])+')'
									precursorformulalist.append(cprecformula)
									precursoradductlist.append('[M+'+ionlist[ioni]+']1+')
									precursormzlist.append(cprecmz)
									precursorchargelist.append('1')
									productchargelist.append('1')	#
									productnamelist.append('TG(Na)-FA '+str(combilist[fvi][comx][nfa][0])+':'+str(combilist[fvi][comx][nfa][1]))		# add first combination (-FA#1,2,3)
									cfnc=str(hgflist[hgi][0]+favarlist[fvi][0]-int(combilist[fvi][comx][nfa][0]))
									cfnh=str(hgflist[hgi][1]+chfa-int(((combilist[fvi][comx][nfa][0]-2)*2)+3-combilist[fvi][comx][nfa][1]*2)-1)
									cprodformula='C'+str(cfnc)+'H'+str(cfnh)+'N'+str(hgflist[hgi][2])+'O'+str(hgflist[hgi][3]-2)+'P'+str(hgflist[hgi][4])
									productformulalist.append(cprodformula) # add first combination (-FA#1,2,3) ##
									productadductlist.append('[M+Na]1+') # add first combination (-FA#1,2,3)
									productmzlist.append(round(float((mzc*float(cfnc))+(mzh*float(cfnh))+(4*mzo)+mzna),4)) # add first combination (-FA#1,2,3)
									nfa=nfa+1
							#print('Added 1 combination.')
							comx=comx+1

					# end add HG and other fragments specific for lipid class
					# end add unoxidized lipid
					comb=comb+1
				ioni=ioni+1
				if hglist[hgi]=='TG':
					if ioni==2:
						ioni=ioni+1		# exclude Na
				if hglist[hgi] in bfalipids:
					#if hglist[hgi]=='PC':
					if ioni==1:
						ioni=ioni+1		# exclude NH4 		
					if ioni==2:
						ioni=ioni+1		# exclude Na			# exclusion here for Na
				if hglist[hgi] in mfalipids:
					if hglist[hgi]=='CE':
						ok=1
					else:
						if ioni==1:
							ioni=ioni+1		# exclude NH4 		
						if ioni==2:
							ioni=ioni+1		# exclude Na			# exclusion here for Na
			fvi=fvi+1
		hgi=hgi+1

	writelist=[]
	writelist.append(moleculegrouplist)
	writelist.append(precursornamelist)
	writelist.append(precursorformulalist)
	writelist.append(precursoradductlist)
	writelist.append(precursormzlist)
	writelist.append(precursorchargelist)
	writelist.append(productnamelist)
	writelist.append(productformulalist)
	writelist.append(productadductlist)
	writelist.append(productmzlist)
	writelist.append(productchargelist)

	nwritelist=[]
	nwritelist.append(nmoleculegrouplist)
	nwritelist.append(nprecursornamelist)
	nwritelist.append(nprecursorformulalist)
	nwritelist.append(nprecursoradductlist)
	nwritelist.append(nprecursormzlist)
	nwritelist.append(nprecursorchargelist)
	nwritelist.append(nproductnamelist)
	nwritelist.append(nproductformulalist)
	nwritelist.append(nproductadductlist)
	nwritelist.append(nproductmzlist)
	nwritelist.append(nproductchargelist)

	# end build transition lists
	print('Initial transition lists are built, sorting and saving now...')

	checktl=0
	if checktl==1:
		# begin save transitionlist neg to csv file
		after=datetime.datetime.now()
		after=str(after)
		today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'
		toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
		ntransitionresultsdf=pd.DataFrame(nwritelist).transpose() #print('Transposed')
		ntransitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
		ntransitionresultsdf.to_csv(str(today)+'TL_JPM_OxLPD1_2_neg_CHECK_'+str(identifier)+'.csv', index=False)
		nrows=len(nmoleculegrouplist)
		print('Transition list (neg) is saved as %sTL_JPM_OxLPD1_2_CHECK_neg_%s.csv (%d rows)' % (today, identifier, nrows))
		# end save transitionlist neg to csv file	###########################################################

	# begin scan transition list pos and neg for entries with mz>1200 (or mzmax) and delete these
	ws=0
	while ws<len(writelist[0]):
		if float(writelist[4][ws])>mzmax:
			cs=0
			while cs<len(writelist):
				#print(writelist[cs][ws])
				del writelist[cs][ws]
				cs=cs+1
			ws=ws-1
		ws=ws+1
	ws=0
	while ws<len(nwritelist[0]):
		if float(nwritelist[4][ws])>mzmax:
			cs=0
			while cs<len(nwritelist):
				del nwritelist[cs][ws]
				cs=cs+1
			ws=ws-1
		ws=ws+1
	# end scan transition list pos and neg for entries with mz>1200 (or mzmax) and delete these

	#print('checkpoint')

	# begin sort neg transition lists by class (to separate PC from OC and QC, and PE from OE and VE)
	ti=0
	while ti<len(nwritelist[0])-1:
		if str(nwritelist[0][ti][0])+str(nwritelist[0][ti][1])==str(nwritelist[0][ti+1][0])+str(nwritelist[0][ti+1][1]):
			ti=ti+1
		else:
			eob=ti
			ti=ti+1
			while ti<len(nwritelist[0])-1:
				if str(nwritelist[0][ti][0])+str(nwritelist[0][ti][1])==str(nwritelist[0][ti+1][0])+str(nwritelist[0][ti+1][1]):
					ti=ti+1
				else:
					if str(nwritelist[0][eob][0])+str(nwritelist[0][eob][1])==str(nwritelist[0][ti+1][0])+str(nwritelist[0][ti+1][1]):
						solb=ti+1
						ti=ti+1
						while ti<len(nwritelist[0])-1:
							if str(nwritelist[0][ti][0])+str(nwritelist[0][ti][1])==str(nwritelist[0][ti+1][0])+str(nwritelist[0][ti+1][1]):
								ti=ti+1
							else:
								eolb=ti
								# found loose block and place to insert
								# insert line by line starting with last line in block
								mcount=0
								mi=eolb
								while mi>(solb-1):
									col=0
									while col<len(nwritelist):
										nwritelist[col].insert((eob+1),nwritelist[col][mi])
										del nwritelist[col][mi+1]
										col=col+1
									solb=solb+1
									mcount=mcount+1
								ti=len(nwritelist[0])
					else:
						ti=ti+1
			ti=eob+1 #mcount+1

	#  end sort neg transition lists by class (to separate PC from OC and QC, and PE from OE and VE)

	# begin sort transition lists
	sorti=0
	while sorti<sorting:
		# begin sort transition list pos
		r=0
		while r<len(writelist[0]):		# go through rows of excel file 
			e=writelist[0][r] # MoleculeGroup		# begin determine which row to start (r) and to end (s)
			s=r+1
			st=0
			while st<1:
				if s>(len(writelist[0])-1):
					ne='stop_loop'
				else:
					ne=writelist[0][s] # MoleculeGroup
				if ne==e:
					s=s+1
					st=0
				else:
					s=s-1
					st=1		# end determine s
			t=r
			# check, if this entry needs to be included earlier or should be appended
			#print(writelist[0][r])
			q=0
			while q<len(writelist[0]):
				if str(writelist[0][q][0])+str(writelist[0][q][1])==str(writelist[0][r][0])+str(writelist[0][r][1]):	# compare lipid class
					if str(writelist[6][q])=='precursor':
						if q<r:
							#print('comparing...')
							#compare FA r to FA q
							#print(writelist[0][r])
							far=int(10*int(writelist[0][r][3])+int(writelist[0][r][4]))
							faq=int(10*int(writelist[0][q][3])+int(writelist[0][q][4]))
							if far<faq:		# compare number of C in FAs
								# insert r before q, delete r, terminate q search loop, go on to next r (s+1)
								#print('moving...')

								#print(writelist[0][r])
								cpc=0
								while cpc<len(writelist):
									cpr=t
									cq=q
									while cpr<(s+1):
										writelist[cpc].insert(cq,writelist[cpc][cpr])			#insert cpc cpr before q
										del(writelist[cpc][cpr+1])								#delete cpc cpr
										#print('loop')
										cq=cq+1
										cpr=cpr+1
									cpc=cpc+1
								q=len(writelist[0])
							elif int(10*int(writelist[0][r][3])+int(writelist[0][r][4]))==int(10*int(writelist[0][q][3])+int(writelist[0][q][4])):
								if len(writelist[0][q])==7:
									if len(writelist[0][r])==7:
										dbr=int(writelist[0][r][6])
										dbq=int(writelist[0][q][6])
									else:
										dbr=int(10*int(writelist[0][r][6])+int(writelist[0][r][7]))
										dbq=int(writelist[0][q][6])
								else:
									if len(writelist[0][r])==7:
										dbr=int(writelist[0][r][6])
										dbq=int(10*int(writelist[0][q][6])+int(writelist[0][q][7]))
									else:
										dbr=int(10*int(writelist[0][r][6])+int(writelist[0][r][7]))
										dbq=int(10*int(writelist[0][q][6])+int(writelist[0][q][7]))
								if dbr<(dbq+1):
									# insert r before q, delete r, terminate q search loop, go on to next r (s+1)
									#print('moving....')
									cpc=0
									while cpc<len(writelist):
										cpr=t
										cq=q
										while cpr<(s+1):
											writelist[cpc].insert(cq,writelist[cpc][cpr])			#insert cpc cpr before q
											del(writelist[cpc][cpr+1])								#delete cpc cpr
											cq=cq+1
											cpr=cpr+1
										cpc=cpc+1
									q=len(writelist[0])
								else:
									ok=1
							else:
								ok=1
						else:
							q=len(writelist[0])
					else:
						ok=1
				else:
					ok=1
				q=q+1
			r=s+1
		# end sort transition list pos
		# begin sort transition list neg
		r=0
		while r<len(nwritelist[0]):		# go through rows of excel file 
			e=nwritelist[0][r] # Precursorname		# begin determine which row to start (r) and to end (s)
			s=r+1
			st=0
			while st<1:
				if s>(len(nwritelist[0])-1):
					ne='stop_loop'
				else:
					ne=nwritelist[0][s] # Precursorname
				if ne==e:
					s=s+1
					st=0
				else:
					s=s-1
					st=1		# end determine s
			t=r
			# check, if this entry needs to be included earlier or should be appended
			#print(nwritelist[0][r])
			q=0
			while q<len(nwritelist[0]):
				if str(nwritelist[0][q][0])+str(nwritelist[0][q][1])==str(nwritelist[0][r][0])+str(nwritelist[0][r][1]):
					if str(nwritelist[6][q])=='precursor':
						if q<r:
							#compare FA r to FA q
							if int(10*int(nwritelist[0][r][3])+int(nwritelist[0][r][4]))<int(10*int(nwritelist[0][q][3])+int(nwritelist[0][q][4])):
								# insert r before q, delete r, terminate q search loop, go on to next r (s+1)
								cpc=0
								while cpc<len(nwritelist):
									cpr=t
									cq=q
									while cpr<(s+1):
										nwritelist[cpc].insert(cq,nwritelist[cpc][cpr])			#insert cpc cpr before q
										del(nwritelist[cpc][cpr+1])								#delete cpc cpr
										cq=cq+1
										cpr=cpr+1
									cpc=cpc+1
								q=len(nwritelist[0])
							elif int(10*int(nwritelist[0][r][3])+int(nwritelist[0][r][4]))==int(10*int(nwritelist[0][q][3])+int(nwritelist[0][q][4])):

								if len(nwritelist[0][q])==7:
									if len(nwritelist[0][r])==7:
										dbr=int(nwritelist[0][r][6])
										dbq=int(nwritelist[0][q][6])
									else:
										dbr=int(10*int(nwritelist[0][r][6])+int(nwritelist[0][r][7]))
										dbq=int(nwritelist[0][q][6])
								else:
									if len(nwritelist[0][r])==7:
										dbr=int(nwritelist[0][r][6])
										dbq=int(10*int(nwritelist[0][q][6])+int(nwritelist[0][q][7]))
									else:
										dbr=int(10*int(nwritelist[0][r][6])+int(nwritelist[0][r][7]))
										dbq=int(10*int(nwritelist[0][q][6])+int(nwritelist[0][q][7]))

								if dbr<(dbq+1):
									# insert r before q, delete r, terminate q search loop, go on to next r (s+1)
									cpc=0
									while cpc<len(nwritelist):
										cpr=t
										cq=q
										while cpr<(s+1):
											nwritelist[cpc].insert(cq,nwritelist[cpc][cpr])			#insert cpc cpr before q
											del(nwritelist[cpc][cpr+1])								#delete cpc cpr
											cq=cq+1
											cpr=cpr+1
										cpc=cpc+1
									q=len(nwritelist[0])
								else:
									ok=1
							else:
								ok=1
						else:
							q=len(nwritelist[0])
					else:
						ok=1
				else:
					ok=1
				q=q+1
			r=s+1
		# end sort transition list neg
		sorti=sorti+1
	# end sort transition lists

	# begin add [M+1] and [M+2] isotopes for precursor		
	### this module is not required - once TL and data loaded, make one (any) transition settings change in Skyline to provoke recalculation of target tree
	### reloading transition settings is not sufficient
	# end add [M+1] and [M+2] isotopes for precursor

	# begin saving files
	after=datetime.datetime.now()
	after=str(after)
	today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'

	# begin save transitionlist pos to csv file
	toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
	transitionresultsdf=pd.DataFrame(writelist).transpose() #print('Transposed')
	transitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
	transitionresultsdf.to_csv(str(today)+'TL_JPM_OxLPD1_1_pos_'+str(identifier)+'.csv', index=False)
	nrows=len(moleculegrouplist)
	print('Transition list (pos) is saved as %sTL_JPM_OxLPD1_1_pos_%s.csv (%d rows)' % (today, identifier, nrows))
	# end save transitionlist pos to csv file	###########################################################

	# begin save transitionlist neg to csv file
	toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
	ntransitionresultsdf=pd.DataFrame(nwritelist).transpose() #print('Transposed')
	ntransitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
	ntransitionresultsdf.to_csv(str(today)+'TL_JPM_OxLPD1_2_neg_'+str(identifier)+'.csv', index=False)
	nrows=len(nmoleculegrouplist)
	print('Transition list (neg) is saved as %sTL_JPM_OxLPD1_2_neg_%s.csv (%d rows)' % (today, identifier, nrows))
	# end save transitionlist neg to csv file	###########################################################

	# begin build inclusion list, pos mode
	inclcomplist=[]
	inclmzlist=[]
	incltstartlist=[]
	incltstoplist=[]
	inclintthrlist=[]
	inclhcdcelist=[]
	wi=0
	while wi<len(writelist[0]):
		if writelist[6][wi]=='precursor':
			if writelist[4][wi] in inclmzlist:
				ok=1
			else:
				minusfa=0
				if str(writelist[1][wi][0])+str(writelist[1][wi][1])=='TG':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='SM':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='CR':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='HC':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='DC':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PC':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PE':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PA':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PG':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PI':
					minusfa=1
				elif str(writelist[1][wi][0])+str(writelist[1][wi][1])=='PS':
					minusfa=1
				if minusfa==1:
					god=1
					while god==1:
						if str(writelist[1][wi][len(writelist[1][wi])-1])=='(':
							god=0
							writelist[1][wi]=writelist[1][wi][:-1]
						else:
							god=god
						writelist[1][wi]=writelist[1][wi][:-1]	# remove last element of string (removing specific FA information, so that only sum composition info remains)
				inclcomplist.append(str(writelist[1][wi])+'_'+str(writelist[3][wi]))
				inclmzlist.append(writelist[4][wi])
				incltstartlist.append(0.5)
				maxrt=round(float(maxrts),1)
				incltstoplist.append(maxrt)
				inclintthrlist.append(0)
				inclhcdcelist.append(collen)
				# if phospholipid, add line for ether lipid(s)
				ethercancel=0		# old addition of ether lipid targets into inclusion list, not required anymore
				if ethercancel==0:
					if str(writelist[1][wi][0])=='P':
						inclcomplist.append(str(writelist[1][wi])+'e_'+str(writelist[3][wi]))
						inclmzlist.append((writelist[4][wi])-mzo+(2*mzh))
						incltstartlist.append(0.5)
						maxrt=round(float(maxrts),1)
						incltstoplist.append(maxrt)
						inclintthrlist.append(0)
						inclhcdcelist.append(collen)

		wi=wi+1
	inclusionlist=[]
	inclusionlist.append(inclcomplist)
	inclusionlist.append(inclmzlist)
	inclusionlist.append(incltstartlist)
	inclusionlist.append(incltstoplist)
	inclusionlist.append(inclintthrlist)
	inclusionlist.append(inclhcdcelist)
	# end build inclusion list					# writelist is now modified to not include specific info on FAs, only sum composition !

	# begin save inclusion list to csv file
	toprowi=['Compound', 'm/z', 't start (min)', 't stop (min)', 'Intensity Threshold', 'HCD Collision Energies (%)']
	inclusionresultsdf=pd.DataFrame(inclusionlist).transpose() #print('Transposed')
	inclusionresultsdf.columns=[toprowi[0],toprowi[1],toprowi[2],toprowi[3],toprowi[4],toprowi[5]] #print('Transposed and DataFrame created')
	inclusionresultsdf.to_csv(str(today)+'IncL_JPM_OxLPD1_pos_'+str(identifier)+'.csv', index=False)
	irows=len(inclcomplist)
	print('Inclusion list (pos) is saved as %sIncL_JPM_OxLPD1_pos_%s.csv (%d rows)' % (today, identifier, irows))
	# end save inclusion list to csv file, pos mode


	# begin build inclusion list, neg mode
	inclcomplist=[]
	inclmzlist=[]
	incltstartlist=[]
	incltstoplist=[]
	inclintthrlist=[]
	inclhcdcelist=[]
	wi=0
	while wi<len(nwritelist[0]):
		if nwritelist[6][wi]=='precursor':
			if nwritelist[4][wi] in inclmzlist:
				ok=1
				#print(nwritelist[0][wi])
			else:
				minusfa=0
				wlip=1
				if str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PC':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='OC':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='QC':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PE':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='OE':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='QE':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PA':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PG':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PI':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='PS':
					minusfa=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='SM':		# wlip=0 means sphingolipids are not included in inclusion list, as MS2 information non-specific for FA
					minusfa=1
					wlip=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='CR':
					minusfa=1
					wlip=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='HC':
					minusfa=1
					wlip=1
				elif str(nwritelist[1][wi][0])+str(nwritelist[1][wi][1])=='DC':
					minusfa=1
					wlip=1
				if minusfa==1:
					god=1
					while god==1:
						if str(nwritelist[1][wi][len(nwritelist[1][wi])-1])=='(':
							god=0
							nwritelist[1][wi]=nwritelist[1][wi][:-1]
						else:
							god=god
						nwritelist[1][wi]=nwritelist[1][wi][:-1]	# remove last element of string (removing specific FA information, so that only sum composition info remains)
				if wlip==1:
					inclcomplist.append(str(nwritelist[1][wi])+'_'+str(nwritelist[3][wi]))
					inclmzlist.append(nwritelist[4][wi])
					incltstartlist.append(0.5)
					incltstoplist.append(maxrt)
					inclintthrlist.append(0)
					inclhcdcelist.append(collen)
				# if phospholipid, add line for ether lipid(s)
				ethercancel=1		# old addition of ether lipid targets into inclusion list, not required anymore
				if ethercancel==0:
					if str(nwritelist[1][wi][0])=='P':
						inclcomplist.append(str(nwritelist[1][wi])+'e_'+str(nwritelist[3][wi]))
						inclmzlist.append((nwritelist[4][wi])-mzo+(2*mzh))
						incltstartlist.append(0.5)
						incltstoplist.append(maxrt)
						inclintthrlist.append(0)
						inclhcdcelist.append(collen)

		wi=wi+1
	ninclusionlist=[]
	ninclusionlist.append(inclcomplist)
	ninclusionlist.append(inclmzlist)
	ninclusionlist.append(incltstartlist)
	ninclusionlist.append(incltstoplist)
	ninclusionlist.append(inclintthrlist)
	ninclusionlist.append(inclhcdcelist)
	# end build inclusion list					# writelist is now modified to not include specific info on FAs, only sum composition !

	# begin save inclusion list to csv file
	toprowi=['Compound', 'm/z', 't start (min)', 't stop (min)', 'Intensity Threshold', 'HCD Collision Energies (%)']
	ninclusionresultsdf=pd.DataFrame(ninclusionlist).transpose() #print('Transposed')
	ninclusionresultsdf.columns=[toprowi[0],toprowi[1],toprowi[2],toprowi[3],toprowi[4],toprowi[5]] #print('Transposed and DataFrame created')
	ninclusionresultsdf.to_csv(str(today)+'IncL_JPM_OxLPD1_neg_'+str(identifier)+'.csv', index=False)
	irows=len(inclcomplist)
	print('Inclusion list (neg) is saved as %sIncL_JPM_OxLPD1_neg_%s.csv (%d rows)' % (today, identifier, irows))
	afterall=datetime.datetime.now()
	dt=afterall-beforeall
	print('Calculation time is %s.' % dt)
	# end save inclusion list to csv file, neg mode

if charpshortcut==1:
	#read csv file
	ntrdf=pd.read_csv('2024_06_18_TL_JPM_OxLPD1_1_pos_NIST1950.csv', low_memory=False)
	toprown=[ntrdf.columns.values.tolist()]
	toprown=toprown[0]
	ntrdf=ntrdf.transpose()
	writelist=ntrdf.values.tolist()
	#print(writelist[1][6])
	# begin consolidate transition list for analysis of TG with characteristic pattern
	# use data in list writelist (pos) and nwritelist (neg) to built TL with all relevant FA fragments for each sum composition
	# for each sum composition create only one precursor to minimize computational demand
	# begin consolidate pos mode TL
	# go through writelist, for each sum composition grab only unique ms2 fragments to add to characteristic pattern
	charp=[[], [], [], [], [], [], [], [], [], [], []]	# new writelist with consolidated TL pos
	def charpadd(k, charp):
		#add current line to charp list
		cli=0
		while cli<len(writelist):
			addx=writelist[cli][k]
			if cli==1:
				addx=writelist[cli-1][k]
			charp[cli].append(addx)
			cli=cli+1
		return(charp)
	k=0
	while k<len(writelist[0]):
		if 'TG' in str(writelist[0][k]):
			#print(writelist[0][k])
			#print(charp)
			if writelist[0][k] in charp[0]:
				if writelist[6][k]=='precursor':
					ok=1
				else:
					if 'TG-FA' in str(writelist[6][k]):
						curcharp=[]	#make inventory of already added ms2 fragments for this sum composition
						j=0
						while j<len(charp[0]):
							if writelist[0][k]==charp[0][j]:
								if charp[6][j] in curcharp:
									ok=1
								else:
									curcharp.append(charp[6][j])
							j=j+1
						if writelist[6][k] in curcharp:
							ok=1
						else:	
							charp=charpadd(k, charp) # call function to add current line for new ms2 fragment
					else:
						ok=1	# delete / ignore fragments that are not TG-FA fragments for efficiency
			else:
				# call function to add current line for new precursor (new sum composition)
				charp=charpadd(k, charp)
		k=k+1
	after=datetime.datetime.now()
	after=str(after)
	today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'
	# begin save transitionlist pos to csv file
	toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
	transitionresultsdf=pd.DataFrame(charp).transpose() #print('Transposed')
	transitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
	transitionresultsdf.to_csv(str(today)+'TL_JPM_characteristic_pattern_pos_'+str(identifier)+'.csv', index=False)
	nrows=len(charp[0])
	print('Transition list (pos) is saved as %sTL_JPM_characteristic_pattern_pos_%s.csv (%d rows)' % (today, identifier, nrows))
	# end save transitionlist pos to csv file	###########################################################
	# end consolidate transition list for analysis with characteristic pattern


