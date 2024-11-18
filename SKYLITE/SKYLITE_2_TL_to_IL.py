# -*- coding: UTF-8 -*-

# Developer: Dr. Jan Philipp Menzel 
# Summary: Generates inclusion lists based on transition list (input) (both pos and neg acquisitions)
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

# begin read TL
trdf=pd.read_csv('JPM_ILS_RAPID_TL_IS_pos.csv')
toprowx=[trdf.columns.values.tolist()]
toprow=toprowx[0]
trdf=trdf.transpose()
writelist=trdf.values.tolist()
ntrdf=pd.read_csv('JPM_ILS_RAPID_TL_IS_neg.csv')
ntoprowx=[ntrdf.columns.values.tolist()]
ntoprow=ntoprowx[0]
ntrdf=ntrdf.transpose()
nwritelist=ntrdf.values.tolist()
# end read TL

after=datetime.datetime.now()
after=str(after)
today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'

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
			ethercancel=1		# old addition of ether lipid targets into inclusion list, not required anymore
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

