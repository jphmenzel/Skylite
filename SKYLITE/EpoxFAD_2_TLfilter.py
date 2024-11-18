# -*- coding: UTF-8 -*-

#Jan Philipp Menzel 
# Program: Calculate filtered transition list for Skyline for EpoxFAD analysis based on initial Skyline analysis (no manual input, Skyline report read here)
# Calculation of epoxidized precursors and their diagnostic fragment ions based on input FA transition list
# First version created: 2024 09 20
#Notes: Reads csv intput file to generate csv output file
#Notes: 
import math
import datetime
import pandas as pd
#import scipy
#from scipy import stats
#import openpyxl
#from openpyxl import Workbook
#import matplotlib.pyplot as plt
#import numpy as np
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

# begin read initial TL
trdf=pd.read_csv('Skyline_Report_JPM_EpoxFAD_FAmix_NIST_MASH.csv')
toprowx=[trdf.columns.values.tolist()]
toprow=toprowx[0]
trdf=trdf.transpose()
writelist=trdf.values.tolist()
# end read initial TL

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

r=0
while r<len(writelist[0]):
    # go through report to check for FA fragments to be filtered out
    #identify blocks
    if 'FAmix' in str(writelist[20][r]):
        t=r+1
        s=r
        e=r+1
        got=1
        while got==1:
            if t<len(writelist[0]):
                if 'FAmix' in str(writelist[20][t]):
                    e=t-1
                    got=0
            else:
                got=0
            t=t+1
        if 'precursor' in writelist[6][r]:
            moleculegrouplist.append(writelist[0][r])
            precursornamelist.append(str(writelist[1][r]))
            precursorformulalist.append(writelist[2][r])
            precursoradductlist.append(writelist[3][r])
            precursormzlist.append(writelist[4][r])
            precursorchargelist.append(writelist[5][r])
            productnamelist.append(writelist[6][r])
            productformulalist.append(writelist[7][r])
            productadductlist.append(writelist[8][r])
            productmzlist.append(writelist[9][r])
            productchargelist.append(writelist[10][r]) 
            r=e
        else:
            k=s
            found=0
            while k<e+1:
                if float(writelist[13][k])>35000:
                    found=1
                k=k+1
            if found==1:
                moleculegrouplist.append(writelist[0][r])
                precursornamelist.append(str(writelist[1][r]))
                precursorformulalist.append(writelist[2][r])
                precursoradductlist.append(writelist[3][r])
                precursormzlist.append(writelist[4][r])
                precursorchargelist.append(writelist[5][r])
                productnamelist.append(writelist[6][r])
                productformulalist.append(writelist[7][r])
                productadductlist.append(writelist[8][r])
                productmzlist.append(writelist[9][r])
                productchargelist.append(writelist[10][r]) 
                r=e 
    r=r+1            

# 
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

after=datetime.datetime.now()
after=str(after)
today=after[0]+after[1]+after[2]+after[3]+'_'+after[5]+after[6]+'_'+after[8]+after[9]+'_'
# begin save transition list to csv file
toprow=['MoleculeGroup', 'PrecursorName', 'PrecursorFormula', 'PrecursorAdduct', 'PrecursorMz', 'PrecursorCharge', 'ProductName', 'ProductFormula', 'ProductAdduct', 'ProductMz', 'ProductCharge']
transitionresultsdf=pd.DataFrame(writelist).transpose() #print('Transposed')
transitionresultsdf.columns=[toprow[0],toprow[1],toprow[2],toprow[3],toprow[4],toprow[5],toprow[6],toprow[7],toprow[8],toprow[9],toprow[10]] #print('Transposed and DataFrame created')
transitionresultsdf.to_csv(str(today)+'EpoxFAD_2_output_FA_filtered_TL.csv', index=False)
nrows=len(moleculegrouplist)
print('Transition list (pos) is saved as %sEpoxFAD_2_output_FA_filtered_TL.csv (%d rows)' % (today, nrows))
# end save transition list to csv file













