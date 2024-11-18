# -*- coding: UTF-8 -*-

#Jan Philipp Menzel 
# Program: Calculate transition list for Skyline for EpoxFAD analysis, 
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
trdf=pd.read_csv('EpoxFAD_1_input_FA_initial_TL.csv')
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
while r<len(writelist[0]):      # Include unepoxidized FA in TL
    moleculegrouplist.append(writelist[0][r])
    precursornamelist.append('FA '+str(writelist[1][r]))
    precursorformulalist.append(writelist[2][r])
    precursoradductlist.append(writelist[3][r])
    precursormzlist.append(writelist[4][r])
    precursorchargelist.append(writelist[5][r])
    productnamelist.append(writelist[6][r])
    productformulalist.append(writelist[7][r])
    productadductlist.append(writelist[8][r])
    productmzlist.append(writelist[9][r])
    productchargelist.append(writelist[10][r]) 
    r=r+1

# begin add monoepoxidized species, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # precursor
    moleculegrouplist.append(str(writelist[0][r])+'_O')
    precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
    precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
    precursoradductlist.append(writelist[3][r]) 
    precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
    precursorchargelist.append(writelist[5][r]) 
    productnamelist.append(writelist[6][r]) 
    productformulalist.append(str(writelist[7][r][:-1])+'3') 
    productadductlist.append(writelist[8][r]) 
    productmzlist.append(round(float(writelist[9][r])+mzo, 6))
    productchargelist.append(writelist[10][r])  
    # begin add fragment ions in case of MUFA
    if int(writelist[1][r][3])==1:
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-2 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of MUFA
    # begin add fragment ions in case of BUFA
    if int(writelist[1][r][3])==2:
        #probe n-terminal double bond from n-2 to delta 6
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-2 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-5 to delta 3
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-5 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of BUFA

    # begin add fragment ions in case of TrisUFA
    if int(writelist[1][r][3])==3:
        #probe n-terminal double bond from n-2 to delta 9
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-2 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle double bond from n-5 to delta 6
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-5 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-8 to delta 3
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-8 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of TrisUFA

    # begin add fragment ions in case of TetraUFA
    if int(writelist[1][r][3])==4:
        #probe n-terminal double bond from n-2 to delta 12
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-2 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_II double bond from n-5 to delta 9
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-5 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_III double bond from n-8 to delta 9
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-5 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-11 to delta 3
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-8 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of TetraUFA





    # begin add fragment ions in case of PentaUFA
    if int(writelist[1][r][3])==5:
        #probe n-terminal double bond from n-2 to delta 15
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-14):  # probe DB positions from n-2 to delta 15
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_II double bond from n-5 to delta 12
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-5 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_III double bond from n-8 to delta 9
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-8 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_IV double bond from n-11 to delta 9
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-11 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-14 to delta 3
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-14 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of PentaUFA


    # begin add fragment ions in case of HexaUFA
    if int(writelist[1][r][3])==6:
       #probe n-terminal double bond from n-2 to delta 17
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-16):  # probe DB positions from n-2 to delta 17
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_II double bond from n-5 to delta 14
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-13):  # probe DB positions from n-5 to delta 14
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_III double bond from n-8 to delta 12
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-8 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_IV double bond from n-11 to delta 9
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-11 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_V double bond from n-14 to delta 6
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-14 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-17 to delta 3
        cdbp=17
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-17 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of HexaUFA

    # begin add fragment ions in case of HeptaUFA
    if int(writelist[1][r][3])==7:
        #probe n-terminal double bond from n-2 to delta 15
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-14):  # probe DB positions from n-2 to delta 15
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_II double bond from n-4 to delta 13
        cdbp=4
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-12):  # probe DB positions from n-4 to delta 13
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_III double bond from n-7 to delta 11
        cdbp=7
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-10):  # probe DB positions from n-7 to delta 11
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_IV double bond from n-10 to delta 9
        cdbp=10
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-10 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_V double bond from n-12 to delta 7
        cdbp=12
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-6):  # probe DB positions from n-12 to delta 7
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n_VI double bond from n-14 to delta 5
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-4):  # probe DB positions from n-14 to delta 5
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-17 to delta 3
        cdbp=16
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-16 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-12
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'3') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-12
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of HeptaUFA

    r=r+1
# end add monoepoxidized species, with diagnostic fragments
#
#
#
#
#
#
# begin add bisepoxidized BUFA and TrisUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    if int(writelist[1][r][3])==2:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_2O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'4') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+2*mzo, 6))
        productchargelist.append(writelist[10][r])  
        #probe n-terminal double bond from n-2 to delta 6
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-2 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-5 to delta 3
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-5 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    
    # begin add fragment ions in case of TrisUFA, bisepoxidized
    if int(writelist[1][r][3])==3:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_2O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'4') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+2*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 9
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-2 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle double bond from n-5 to delta 6
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-5 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-8 to delta 3
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-8 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_2O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_2O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'4') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+2*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of TrisUFA, bisepoxidized
    r=r+1

# end add bisepoxidized BUFA and TrisUFA, with diagnostic fragments
#
#
#
#
# begin add trisepoxidized TrisUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # begin add fragment ions in case of TrisUFA, trisepoxidized
    if int(writelist[1][r][3])==3:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_3O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'5') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+3*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 9
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-2 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle double bond from n-5 to delta 6
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-5 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-8 to delta 3
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-8 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_3O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_3O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'5') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+3*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of TrisUFA, trisepoxidized
    r=r+1
# end add trisepoxidized TrisUFA, with diagnostic fragments
#
#
#
#
# begin add tetraepoxidized TetraUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # begin add fragment ions in case of TetraUFA, tetraepoxidized
    if int(writelist[1][r][3])==4:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_4O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'6') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+4*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 12
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-2 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-II double bond from n-5 to delta 9
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-5 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-III double bond from n-8 to delta 6
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-8 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-11 to delta 3
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-11 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_4O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_4O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'6') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+4*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of TetraUFA, tetraepoxidized
    r=r+1
# end add tetraepoxidized TetraUFA, with diagnostic fragments
#
#
#
#
# begin add pentaepoxidized PentaUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # begin add fragment ions in case of PentaUFA, pentaepoxidized
    if int(writelist[1][r][3])==5:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_5O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'7') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+5*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 15
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-14):  # probe DB positions from n-2 to delta 15
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O7'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+5*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-II double bond from n-5 to delta 12
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-5 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-III double bond from n-8 to delta 9
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-8 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-IV double bond from n-11 to delta 6
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-11 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-14 to delta 3
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-14 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_5O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_5O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'7') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+5*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of PentaUFA, pentaepoxidized
    r=r+1
# end add pentaepoxidized PentaUFA, with diagnostic fragments
#
#
#
#
# begin add hexaepoxidized HexaUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # begin add fragment ions in case of HexaUFA, Hexaepoxidized
    if int(writelist[1][r][3])==6:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_6O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'8') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+6*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 18
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-17):  # probe DB positions from n-2 to delta 18
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O7'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+5*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O8'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+6*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-II double bond from n-5 to delta 15
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-14):  # probe DB positions from n-5 to delta 15
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O7'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+5*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-III double bond from n-8 to delta 12
        cdbp=8
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-11):  # probe DB positions from n-8 to delta 12
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-IV double bond from n-11 to delta 9
        cdbp=11
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-11 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-V double bond from n-14 to delta 6
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-5):  # probe DB positions from n-14 to delta 6
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-17 to delta 3
        cdbp=17
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-17 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VI-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_6O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_6O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'8') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+6*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VI-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of HexaUFA, Hexaepoxidized
    r=r+1
# end add hexaepoxidized HexaUFA, with diagnostic fragments
#
#
#
#
# begin add heptaepoxidized HeptaUFA, with diagnostic fragments
r=0
while r<len(writelist[0]):
    # begin add fragment ions in case of HeptaUFA, Heptaepoxidized
    if int(writelist[1][r][3])==7:
        # precursor
        moleculegrouplist.append(str(writelist[0][r])+'_7O')
        precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
        precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
        precursoradductlist.append(writelist[3][r]) 
        precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
        precursorchargelist.append(writelist[5][r]) 
        productnamelist.append(writelist[6][r]) 
        productformulalist.append(str(writelist[7][r][:-1])+'9') 
        productadductlist.append(writelist[8][r]) 
        productmzlist.append(round(float(writelist[9][r])+7*mzo, 6))
        productchargelist.append(writelist[10][r]) 
        #probe n-terminal double bond from n-2 to delta 15
        cdbp=2
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-14):  # probe DB positions from n-2 to delta 15
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O8'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+6*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O9'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+7*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-II double bond from n-5 to delta 13
        cdbp=5
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-12):  # probe DB positions from n-5 to delta 13
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O7'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+5*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_II-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-2
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O8'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+6*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-III double bond from n-7 to delta 11
        cdbp=7
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-10):  # probe DB positions from n-7 to delta 11
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_III-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-4
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O7'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+5*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-IV double bond from n-9 to delta 9
        cdbp=9
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-8):  # probe DB positions from n-9 to delta 9
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_IV-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-6
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O6'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+4*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-V double bond from n-12 to delta 7
        cdbp=12
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-6):  # probe DB positions from n-12 to delta 7
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_V-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-8
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O5'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+3*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe middle n-VI double bond from n-14 to delta 5
        cdbp=14
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-4):  # probe DB positions from n-14 to delta 5
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VI-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VI-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-10
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O4'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+2*mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
        #probe C-terminal double bond from n-16 to delta 3
        cdbp=16
        while cdbp<((10*int(writelist[1][r][0])+int(writelist[1][r][1]))-2):  # probe DB positions from n-16 to delta 3
            # ene fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VII-'+str(cdbp)+'_ene') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-12
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O2'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            # aldehyde fragment
            moleculegrouplist.append(str(writelist[0][r])+'_7O')
            precursornamelist.append('FA '+str(writelist[1][r])+'_7O') 
            precursorformulalist.append(str(writelist[2][r][:-1])+'9') 
            precursoradductlist.append(writelist[3][r]) 
            precursormzlist.append(round(float(writelist[4][r])+7*mzo, 6))
            precursorchargelist.append(writelist[5][r]) 
            productnamelist.append('n_VII-'+str(cdbp)+'_ald') 
            mc=1+(cdbp-1)
            mh=2+(2*(cdbp-1))-12
            cprodformula='C'+str((10*int(writelist[7][r][1])+int(writelist[7][r][2]))-mc)+'H'+str((10*int(writelist[7][r][4])+int(writelist[7][r][5]))-mh)+'O3'
            productformulalist.append(cprodformula) 
            productadductlist.append(writelist[8][r]) 
            cprodmz=writelist[9][r]-(mc*mzc)-(mh*mzh)+mzo
            productmzlist.append(round(float(cprodmz), 6))
            productchargelist.append(writelist[10][r])  
            cdbp=cdbp+1
    # end add fragment ions in case of HeptaUFA, Heptaepoxidized
    r=r+1
# end add heptaepoxidized HeptaUFA, with diagnostic fragments

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
transitionresultsdf.to_csv(str(today)+'EpoxFAD_1_output_FA_initial_TL.csv', index=False)
nrows=len(moleculegrouplist)
print('Transition list (pos) is saved as %sEpoxFAD_1_output_FA_initial_TL.csv (%d rows)' % (today, nrows))
# end save transition list to csv file
