# -*- coding: UTF-8 -*-

# Jan Philipp Menzel
# Reads TG list of relevant sum compositions and TL_characteristic_pattern_23k file to generate TG-FA transition list with suitable TGs

import math
import openpyxl
import pandas as pd
import datetime
import openpyxl
from openpyxl import Workbook
import subprocess
import statistics
import csv
import sys
maxInt=sys.maxsize
beforeall=datetime.datetime.now()
################ DATABASE ## Source: Internetchemie.info
#isotope=["1H", "2H", "12C", "13C", "14N", "15N", "16O", "17O", "18O", "19F", "23Na", "28Si", "29Si", "30Si", "31P", "32S", "33S", "34S", "36S", "39K", "40K", "41K", "35Cl", "37Cl", "79Br", "81Br"]
#mass=[1.00783, 2.01410 , 12.00000, 13.00335, 14.00307, 15.00011, 15.99491, 16.99913, 17.99916, 18.99840, 22.97977, 27.97693, 28.97649, 29.97377, 30.97376, 31.97207, 32.97146, 33.96787, 35.96708, 38.96371, 39.96400, 40.96183, 34.96885, 36,96590, 78.91834, 80.91629]
#abundance=[99.9885, 0.0115, 98.93, 1.07, 99.636, 0.364, 99.7, 0.04, 0.2, 100, 100, 92.233, 4.685, 3.092, 100, 94.93, 0.76, 4.29, 0.02, 93.2581, 0.0117, 6.7302, 75.76, 24.24, 50.69, 49.31]
isotope=['1H   ', '2H  ', '12C   ', '14N   ', '16O    ', '31P   ', '32S    ' '23Na     ', 'e     ', '132Xe', '   127I']
imass=[1.007825, 2.0141, 12.00000, 14.00307, 15.99491, 30.973762, 31.97207, 22.98977, 0.000548585, 131.9041535, 126.904473]
################
checkup=0
print('--------------------------------------------------------------------------------------------------------')
print(' S K Y L I T E  7 ')
print('This program calculates a transition list for TG-FA profile analysis based on a generic input transition list and a TG sum composition profile for one specific sample.')
print('The required input file for this program is SKYLITE_TL_characteristic_pattern_TG_23k.csv and TG_sum_composition_for_TGFA_input.xlsx')
print('Adjust the latter file to contain the TG sum compositions as required for this sample or sample type.')
print('Please refer to the associated publication / preprint and the github page for information.')
print('Calculation start at %s' % beforeall)
print('--------------------------------------------------------------------------------------------------------')

# begin read sum compositions from excel file
wb=openpyxl.load_workbook('TG_sum_composition_for_TGFA_input.xlsx')
ws=wb['TG']
r=2
sclist=[]
scnlist=[]
gok=1
while gok==1:
	csc=ws.cell(row=r, column=1).value
	if csc is None:
		gok=0
	elif str(csc)=='':
		gok=0
	else:
		sclist.append(str(csc))
		cscnlist=[]
		cscnlist.append(int(str(csc[3])+str(csc[4])))
		if len(csc)==7:
			cscnlist.append(int(str(csc[6])))
		elif len(csc)==8:
			cscnlist.append(int(str(csc[6])+str(csc[7])))
		scnlist.append(cscnlist)
	r=r+1
# end read sum compositions from excel file

# begin read Skyline generic transitin list of TG characteristic pattern
trdf=pd.read_csv('SKYLITE_TL_characteristic_pattern_TG_23k.csv', low_memory=False)
toprow=[trdf.columns.values.tolist()]
toprow=toprow[0]
trdf=trdf.transpose()
tlgen=trdf.values.tolist()
# end read  Skyline generic transitin list of TG characteristic pattern

print(sclist)			# full sum compositions ['TG_50:2', '...']
#print(scnlist)			# usable sum compositions [[xx, y], [xx, yy]...]
#print(tlgen[3][5])		# tlgen[column][row] starting at index 0 each
#print(tlgen[4][2])
tlout=[]
i=0
while i<11:
	tlout.append([])
	i=i+1
#print(tlout)
k=0
while k<len(tlgen[0]):
	if str(tlgen[1][k]) in sclist:
		#print(tlgen[1][k])
		i=0
		while i<11:
			tlout[i].append(tlgen[i][k])
			i=i+1
	k=k+1

#print(tlout)

after=datetime.datetime.now()
after=str(after)
today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'
# begin save transitionlist pos to csv file
toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
transitionresultsdf=pd.DataFrame(tlout).transpose() #print('Transposed')
transitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
transitionresultsdf.to_csv(str(today)+'TL_for_TGFA_adjusted.csv', index=False)
nrows=len(tlout[0])
print('Transition list is saved as %sTL_for_TGFA_adjusted.csv (%d rows)' % (today, nrows))
# end save transitionlist pos to csv file	###########################################################





















