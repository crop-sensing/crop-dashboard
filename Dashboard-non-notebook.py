# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:11:09 2024

@author: audrey
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
from matplotlib import rcParams
import datetime
import os
from datetime import timedelta
from datetime import date
import numpy as np
import fnmatch
from matplotlib.backends.backend_pdf import PdfPages
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import plotly.express as px

#1

# Cleaning Data

path = 'C:/Users/mrcoo/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/suplementary/old_datafiles/Datalogger_Data_May_2024'
sites = ['OLA', 'WWF', 'VAC', 'SLC', 'FLT', 'WES']

all_st = []

for i in range(0,6):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat1*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    df.TIMESTAMP= pd.to_datetime(df['TIMESTAMP'], format= 'mixed')
    appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  #dff.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/' +sites[i]+ '_out.csv',index=False,na_rep='NAN')
  dff_all=dff
  all_st.append(dff_all)
df_all=pd.concat(all_st)
#df_all.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/All_stations_out.csv',index=False,na_rep='NAN')


df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()
#df_all.TIMESTAMP= pd.to_datetime(df_all['TIMESTAMP'], format= '%Y-%m-%d %H:%M:%S')
start_date = pd.Timestamp('2023-08-01')
mask = (df_all['TIMESTAMP'] >= start_date)
df_all = df_all.loc[mask]
df_all['ET'] = np.where(df_all['ET']<=0 , np.nan, df_all['ET'])
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])
VAC1 = df_all[df_all.Site=='VAC']
WWF1 = df_all[df_all.Site=='WWF']
OLA1 = df_all[df_all.Site=='OLA']
SLC1 = df_all[df_all.Site=='SLC']
FLT1 = df_all[df_all.Site=='FLT']
WES1 = df_all[df_all.Site=='WES']


rangepath = r'\Users\mrcoo\Box\TREX\MISCELLANEOUS\Datalogger_Report_Files\suplementary\all_dl_ranges.csv'
rangedf = pd.read_csv(rangepath, header=[0],sep=',',na_values="NAN",engine='python')

rangedf.at[0, 'e_probe'] = -2
rangedf.at[0, 'H2O_probe'] = -10
rangedf.at[0, 'RH_3_1_1'] = -100
rangedf.at[0, 'T_DP_3_1_1'] = -100
rangedf.at[0, 'P_Tot'] = -2

all_calls = ['batt_volt', 'SG_1_1_1', 'SG_2_1_1','SG_3_1_1','SG_4_1_1','SG_5_1_1', 'TS1_2cm', 'TS1_6cm', 'TS2_2cm','TS2_6cm', 'TS3_2cm','TS3_6cm', 'TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1', 'G', 'G_1_1_1',
              'hydra1_temp', 'SoilWater_1', 'G_2_1_1', 'hydra2_temp', 'SoilWater_2', 'G_3_1_1', 'hydra3_temp', 'SoilWater_3', 'G_4_1_1', 'hydra4_temp', 'SoilWater_4', 'G_5_1_1', 'hydra5_temp', 'SoilWater_5', 'FW', 'FW_SIGMA', 'H_FW', 'LW_IN', 'LW_OUT', 'NETRAD', 'SW_IN', 'SW_OUT',
             'H', 'T_SONIC', 'T_SONIC_SIGMA', 'TAU', 'TAU_QC', 'TKE', 'TSTAR', 'USTAR', 'Ux', 'Ux_SIGMA', 'Uy', 'Uy_SIGMA', 'Uz', 'Uz_SIGMA', 'WD', 'WD_SIGMA', 'WD_SONIC', 'WS', 'WS_MAX', 'WS_RSLT', 'Bowen_ratio', 'ET', 'LE', 'energy_closure', 'CO2_density',
             'H2O_density', 'CO2_density_SIGMA', 'H2O_density_SIGMA', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'RH_2_1_1', 'T_DP_2_1_1', 'TA_2_1_1', 'FC_mass', 'e', 'e_sat', 'amb_e', 'amb_e_sat',
             'PA', 'RH_1_1_1', 'T_DP_1_1_1', 'TA_1_1_1', 'Duty_cycle_TS100_Fan_Avg', 'e_probe', 'e_sat_probe', 'Freq_tach_TS100_Avg', 'H2O_probe', 'RH_3_1_1', 'T_DP_3_1_1', 'TA_3_1_1', 'VPD', 'T_CANOPY', 'T_SI111_body', 'air_mass_coeff','FETCH_MAX', 'FP_DIST_INTRST', 'hour_angle', 'sun_azimuth', 'sun_declination', 'sun_elevation']


test_calls = ['FW', 'H_FW', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_3_1_1', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P_Tot', 'batt_volt']

#2 TREX

path = 'C:/Users/mrcoo/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files'
sites = ['OLA', 'WWF', 'VAC', 'SLC', 'FLT', 'WES']

all_st = []

for i in range(0,6):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    df.TIMESTAMP= pd.to_datetime(df['TIMESTAMP'], format= 'mixed')
    appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  #dff.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/' +sites[i]+ '_out.csv',index=False,na_rep='NAN')
  dff_all=dff
  all_st.append(dff_all)
df_all=pd.concat(all_st)
#df_all.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/All_stations_out.csv',index=False,na_rep='NAN')


df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()
#df_all.TIMESTAMP= pd.to_datetime(df_all['TIMESTAMP'], format= '%Y-%m-%d %H:%M:%S')
start_date = pd.Timestamp('2023-08-01')
mask = (df_all['TIMESTAMP'] >= start_date)
df_all = df_all.loc[mask]
df_all['ET'] = np.where(df_all['ET']<=0 , np.nan, df_all['ET'])
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])
# VAC2 = df_all[df_all.Site=='VAC']
# WWF2 = df_all[df_all.Site=='WWF']
# OLA2 = df_all[df_all.Site=='OLA']
# SLC2 = df_all[df_all.Site=='SLC']
# FLT2 = df_all[df_all.Site=='FLT']
# WES2 = df_all[df_all.Site=='WES']


# VACS = [VAC1, VAC2]
# VAC = pd.concat(VACS)
# VAC = VAC.sort_values(by=['TIMESTAMP'])
# VAC = VAC.drop_duplicates()

# WWFS = [WWF1, WWF2]
# WWF = pd.concat(WWFS)
# WWF = WWF.sort_values(by=['TIMESTAMP'])
# WWF = WWF.drop_duplicates()

# OLAS = [OLA1, OLA2]
# OLA = pd.concat(OLAS)
# OLA = OLA.sort_values(by=['TIMESTAMP'])
# OLA = OLA.drop_duplicates()

# SLCS = [SLC1, SLC2]
# SLC = pd.concat(SLCS)
# SLC = SLC.sort_values(by=['TIMESTAMP'])
# SLC = SLC.drop_duplicates()

# FLTS = [FLT1, FLT2]
# FLT = pd.concat(FLTS)
# FLT = FLT.sort_values(by=['TIMESTAMP'])
# FLT = FLT.drop_duplicates()

# WESS = [WES1, WES2]
# WES = pd.concat(WESS)
# WES = WES.sort_values(by=['TIMESTAMP'])
# WES = WES.drop_duplicates()

trex_all = df_all

test_calls = ['e_probe', 'e_sat_probe', 'H2O_probe', 'RH_3_1_1', 'T_DP_3_1_1', 'FW', 'H_FW', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_3_1_1', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P_Tot', 'batt_volt']

#1 matt

path = path = 'C:/Users/mrcoo/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/suplementary/old_datafiles/Datalogger_Data_May_2024'
sites = ['BLS_001', 'BLS_002', 'ORO_022', 'ORO_043', 'COR_CS3', 'ART_011']

all_st = []

for i in range(0,6):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat1*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    df.TIMESTAMP= pd.to_datetime(df['TIMESTAMP'], format= 'mixed')
    appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  dff['Site'] = sites[i]
  #dff.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/'+sites[i]+'_out.csv',index=False,na_rep='NAN')

  dff_all=dff
  all_st.append(dff_all)
df_all=pd.concat(all_st)
#df_all.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/Matt_All_stations_out.csv',index=False,na_rep='NAN')

df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()

#df_all['ET'] = np.where(df_all['ET']<=0 , np.nan, df_all['ET'])
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])
BL1 = df_all[df_all.Site=='BLS_001']
BL2 = df_all[df_all.Site=='BLS_002']
OR2 = df_all[df_all.Site=='ORO_022']
OR4 = df_all[df_all.Site=='ORO_043']
COR = df_all[df_all.Site=='COR_CS3']
ART = df_all[df_all.Site=='ART_011']


rangepath = r'\Users\mrcoo\Box\TREX\MISCELLANEOUS\Datalogger_Report_Files\suplementary\all_dl_ranges.csv'
rangedf = pd.read_csv(rangepath, header=[0],sep=',',na_values="NAN",engine='python')

all = ['TIMESTAMP', 'RECORD', 'V_batt', 'FC_mass', 'FC_QC', 'FC_samples', 'LE', 'LE_QC', 'LE_samples', 'H', 'H_QC', 'H_samples', 'NETRAD', 'G', 'G_1_1_1', 'G_2_1_1', 'G_3_1_1', 'G_4_1_1', 'G_5_1_1', 'SG_1_1_1',
       'SG_2_1_1', 'SG_3_1_1', 'SG_4_1_1', 'SG_5_1_1', 'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1', 'energy_closure', 'Bowen_ratio', 'TAU', 'TAU_QC', 'USTAR', 'TSTAR',
       'TKE', 'TA_1_1_1', 'RH_1_1_1', 'T_DP_1_1_1', 'e_amb', 'e_sat_amb', 'TA_1_1_2', 'RH_1_1_2', 'T_DP_1_1_2', 'e', 'e_sat', 'PA', 'VPD', 'Ux', 'Ux_SIGMA', 'Uy', 'Uy_SIGMA', 'Uz', 'Uz_SIGMA', 'T_SONIC',
       'T_SONIC_SIGMA', 'sonic_azimuth', 'WS', 'WS_RSLT', 'WD_SONIC', 'WD_SIGMA', 'WD', 'WS_MAX', 'CO2_density', 'CO2_density_SIGMA', 'H2O_density', 'H2O_density_SIGMA', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min',
       'ALB', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'sun_azimuth', 'sun_elevation', 'hour_angle', 'sun_declination', 'air_mass_coeff', 'daytime', 'TS1_2cm', 'TS1_6cm', 'TS2_2cm', 'TS2_6cm', 'TS3_2cm', 'TS3_6cm',
       'TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 'SWC_1_1_1', 'SWC_2_1_1', 'SWC_3_1_1', 'SWC_4_1_1', 'SWC_5_1_1', 'TS_CS65X_1_1_1', 'TS_CS65X_1_1_2', 'TS_CS65X_1_1_3', 'TS_CS65X_1_1_4', 'TS_CS65X_1_1_5',
       'cs65x_ec_1_1_1', 'cs65x_ec_1_1_2', 'cs65x_ec_1_1_3', 'cs65x_ec_1_1_4', 'cs65x_ec_1_1_5', 'FETCH_MAX', 'FETCH_90', 'FETCH_55', 'FETCH_40', 'UPWND_DIST_INTRST',
       'poor_enrg_clsur', 'TA_1_1_3', 'RH_1_1_3', 'T_DP_1_1_3', 'e_probe', 'e_sat_probe', 'H2O_density_probe', 'P','T_nr_in', 'T_nr_out', 'T_CANOPY', 'T_SI111_body', 'T_nr', 'R_LW_in_meas', 'R_LW_out_meas']


reports = ['SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']
issues = ['SWC_5_1_1', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']


winds = ['Ux', 'Ux_SIGMA', 'Uy', 'Uy_SIGMA', 'Uz', 'Uz_SIGMA', 'WS', 'WS_RSLT', 'WD_SONIC', 'WD_SIGMA', 'WD', 'WS_MAX']


thurs = ['G', 'G_1_1_1', 'G_2_1_1', 'G_3_1_1', 'G_4_1_1', 'G_5_1_1', 'SG_1_1_1', 'SG_2_1_1', 'SG_3_1_1', 'SG_4_1_1', 'SG_5_1_1', 
       'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1',
       'TS1_2cm', 'TS1_6cm', 'TS2_2cm', 'TS2_6cm', 'TS3_2cm', 'TS3_6cm', 'TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 
       'SWC_1_1_1', 'SWC_2_1_1', 'SWC_3_1_1', 'SWC_4_1_1', 'SWC_5_1_1', 
       'TS_CS65X_1_1_1', 'TS_CS65X_1_1_2', 'TS_CS65X_1_1_3', 'TS_CS65X_1_1_4', 'TS_CS65X_1_1_5', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']


rangedf.at[1, 'cs65x_ec_1_1_1'] = 2
rangedf.at[1, 'cs65x_ec_1_1_2'] = 2
rangedf.at[1, 'cs65x_ec_1_1_3'] = 2
rangedf.at[1, 'cs65x_ec_1_1_4'] = 2
rangedf.at[1, 'cs65x_ec_1_1_5'] = 2


test = ['FC_mass', 'FC_QC', 'FC_samples', 'LE', 'LE_QC', 'LE_samples', 'H', 'H_QC', 'H_samples', 'NETRAD', 'energy_closure', 'Bowen_ratio', 'TAU', 'TAU_QC', 'USTAR', 'TSTAR',
       'TKE', 'TA_1_1_1', 'RH_1_1_1', 'T_DP_1_1_1', 'e_amb', 'e_sat_amb', 'TA_1_1_2', 'RH_1_1_2', 'T_DP_1_1_2', 'e', 'e_sat', 'PA', 'VPD', 'Ux', 'Ux_SIGMA', 'Uy', 'Uy_SIGMA', 'Uz', 'Uz_SIGMA', 'T_SONIC',
       'T_SONIC_SIGMA', 'sonic_azimuth', 'WS', 'WS_RSLT', 'WD_SONIC', 'WD_SIGMA', 'WD', 'WS_MAX', 'CO2_density', 'CO2_density_SIGMA', 'H2O_density', 'H2O_density_SIGMA', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min',
       'ALB', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'sun_azimuth', 'sun_elevation', 'hour_angle', 'sun_declination', 'air_mass_coeff', 'daytime', 'FETCH_MAX', 'FETCH_90', 'FETCH_55', 'FETCH_40', 'UPWND_DIST_INTRST',
       'poor_enrg_clsur', 'TA_1_1_3', 'RH_1_1_3', 'T_DP_1_1_3', 'e_probe', 'e_sat_probe', 'H2O_density_probe', 'P','T_nr_in', 'T_nr_out', 'T_CANOPY', 'T_SI111_body', 'T_nr', 'R_LW_in_meas', 'R_LW_out_meas']

issues = ['SWC_5_1_1', 'FC_samples', 'LE_samples', 'H_samples', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']


#2 MATT

path = 'C:/Users/mrcoo/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files'
sites = ['BLS_001', 'BLS_002', 'ORO_022', 'ORO_043', 'COR_CS3', 'ART_011']

all_st = []

for i in range(0,6):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    appended_data.append(df)
  dff=pd.concat(appended_data)
#   Why does the below line not work anymore?
#   dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  dff['Site'] = sites[i]
  #dff.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/'+sites[i]+'_out.csv',index=False,na_rep='NAN')

  dff_all=dff
  all_st.append(dff_all)
df_all=pd.concat(all_st)
#df_all.to_csv('/Users/mina.swintek/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/output/Matt_All_stations_out.csv',index=False,na_rep='NAN')

df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()
df_all.TIMESTAMP= pd.to_datetime(df_all['TIMESTAMP'], format= '%Y-%m-%d %H:%M:%S')

#df_all['ET'] = np.where(df_all['ET']<=0 , np.nan, df_all['ET'])
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])
# BL12 = df_all[df_all.Site=='BLS_001']
# BL22 = df_all[df_all.Site=='BLS_002']
# OR22 = df_all[df_all.Site=='ORO_022']
# OR42 = df_all[df_all.Site=='ORO_043']
# COR2 = df_all[df_all.Site=='COR_CS3']
# ART2 = df_all[df_all.Site=='ART_011']


# BL1S = [BL1, BL12]
# BL1 = pd.concat(BL1S)
# BL1=BL1.sort_values(by=['TIMESTAMP'])
# BL1=BL1.drop_duplicates()

# BL2S = [BL2, BL22]
# BL2 = pd.concat(BL2S)
# BL2=BL2.sort_values(by=['TIMESTAMP'])
# BL2=BL2.drop_duplicates()

# OR2S = [OR2, OR22]
# OR2 = pd.concat(OR2S)
# OR2=OR2.sort_values(by=['TIMESTAMP'])
# OR2=OR2.drop_duplicates()

# OR4S = [OR4, OR42]
# OR4 = pd.concat(OR4S)
# OR4=OR4.sort_values(by=['TIMESTAMP'])
# OR4=OR4.drop_duplicates()

# CORS = [COR, COR2]
# COR = pd.concat(CORS)
# COR=COR.sort_values(by=['TIMESTAMP'])
# COR=COR.drop_duplicates()

# ARTS = [ART, ART2]
# ART = pd.concat(ARTS)
# ART=ART.sort_values(by=['TIMESTAMP'])
# ART=ART.drop_duplicates()

all_ = ['V_batt', 'FC_mass', 'FC_QC', 'FC_samples', 'LE', 'LE_QC', 'LE_samples', 'H', 'H_QC', 'H_samples', 'NETRAD', 'G', 'G_1_1_1', 'G_2_1_1', 'G_3_1_1', 'G_4_1_1', 'G_5_1_1', 'SG_1_1_1',
       'SG_2_1_1', 'SG_3_1_1', 'SG_4_1_1', 'SG_5_1_1', 'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1', 'energy_closure', 'Bowen_ratio', 'TAU', 'TAU_QC', 'USTAR', 'TSTAR',
       'TKE', 'TA_1_1_1', 'RH_1_1_1', 'T_DP_1_1_1', 'e_amb', 'e_sat_amb', 'TA_1_1_2', 'RH_1_1_2', 'T_DP_1_1_2', 'e', 'e_sat', 'PA', 'VPD', 'Ux', 'Ux_SIGMA', 'Uy', 'Uy_SIGMA', 'Uz', 'Uz_SIGMA', 'T_SONIC',
       'T_SONIC_SIGMA', 'sonic_azimuth', 'WS', 'WS_RSLT', 'WD_SONIC', 'WD_SIGMA', 'WD', 'WS_MAX', 'CO2_density', 'CO2_density_SIGMA', 'H2O_density', 'H2O_density_SIGMA', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min',
       'ALB', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'sun_azimuth', 'sun_elevation', 'hour_angle', 'sun_declination', 'air_mass_coeff', 'daytime', 'TS1_2cm', 'TS1_6cm', 'TS2_2cm', 'TS2_6cm', 'TS3_2cm', 'TS3_6cm',
       'TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 'SWC_1_1_1', 'SWC_2_1_1', 'SWC_3_1_1', 'SWC_4_1_1', 'SWC_5_1_1', 'TS_CS65X_1_1_1', 'TS_CS65X_1_1_2', 'TS_CS65X_1_1_3', 'TS_CS65X_1_1_4', 'TS_CS65X_1_1_5',
       'cs65x_ec_1_1_1', 'cs65x_ec_1_1_2', 'cs65x_ec_1_1_3', 'cs65x_ec_1_1_4', 'cs65x_ec_1_1_5', 'FETCH_MAX', 'FETCH_90', 'FETCH_55', 'FETCH_40', 'UPWND_DIST_INTRST',
       'poor_enrg_clsur', 'TA_1_1_3', 'RH_1_1_3', 'T_DP_1_1_3', 'e_probe', 'e_sat_probe', 'H2O_density_probe', 'P','T_nr_in', 'T_nr_out', 'T_CANOPY', 'T_SI111_body', 'T_nr', 'R_LW_in_meas', 'R_LW_out_meas']


reports = ['SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']
issues = ['SWC_5_1_1', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']

matt_all = df_all
matt_all


reports = ['G', 'G_1_1_1', 'G_2_1_1', 'G_3_1_1', 'G_4_1_1', 'G_5_1_1', 'SG_1_1_1', 'SG_2_1_1', 'SG_3_1_1', 'SG_4_1_1', 'SG_5_1_1', 'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1', 'TS1_2cm', 'TS1_6cm', 'TS2_2cm', 'TS2_6cm', 'TS3_2cm', 'TS3_6cm','TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 'SWC_1_1_1', 'SWC_2_1_1', 'SWC_3_1_1', 'SWC_4_1_1', 'SWC_5_1_1', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']


almonds = ["VAC", "OLA", "WWF", "WES"]
olives = ["ART_011", "ORO_022", "ORO_043", "COR_CS3"]
pistachios = ["BLS_001", "BLS_002"]
grapes = ["FLT", "SLC"]

# Dashboard

calls = test_calls

today = date.today()
ini = today - timedelta(days=6)
ini2 = today - timedelta(days=30)

# Read in parameters classified by equipment group
equip_list = pd.read_csv("C:/Users/mrcoo/Desktop/Audrey Work/Dashboard/TREX_Equipment.csv")
matt_equip_list = pd.read_csv("C:/Users/mrcoo/Desktop/Audrey Work/Dashboard/MATT_Equipment.csv")

# Read in coordinates for sites
coords = pd.read_csv("C:/Users/mrcoo/Desktop/Audrey Work/Dashboard/Site_Long_Lat.csv")

# Creates and populates two different dictionaries, based on existing DFs, to simplify dropdown menu code later.

equip_dict = dict()
for j in equip_list.loc[0].unique():
    equip_dict[j] = []

for i in range(0, len(equip_list.loc[0])):
    equip_dict[equip_list.loc[0][i]].append(equip_list.columns[i])
    
matt_dict = dict()
for j in matt_equip_list.loc[0].unique():
    matt_dict[j] = []

for i in range(0, len(matt_equip_list.loc[0])):
    matt_dict[matt_equip_list.loc[0][i]].append(matt_equip_list.columns[i])


app = Dash(__name__)

app.layout = [html.Div(
    html.Div([
        html.H1(["Dashboard"], style = {"padding-left": 5}),
        
        # This container creates a label for radio items, creates a radio items object
        # with all crop options, and stylizes the text and positioning of each.
        
        html.Div([
        html.Label(["Crops:"], style = {"text-align": "left", "font-weight": "bold", 
                                            "padding-left": 5}),
            dcc.RadioItems(options = [
                {"label": html.Div(["All"], style = {'display':'inline-block', "margin-right": 5, 
                                                      "padding-left": 3}), 
                 "value": "All"},
                {"label": html.Div(["Almonds"], style = {'display':'inline-block', "margin-right": 5,
                                                         "padding-left": 1}), 
                 "value": "Almonds"},
                {"label": html.Div(["Grapes"], style = {'display':'inline-block', "padding-left": 2}), 
                 "value": "Grapes"},
                {"label": html.Div(["Olives"], style = {'display':'inline-block', "margin-right": 5,
                                                        "padding-left": 1}), 
                 "value": "Olives"},
                {"label": html.Div(["Pistachios"], style = {'display':'inline-block', "margin-right": 5,
                                                            "padding-left": 2}),
                 "value": "Pistachios"}],
            value = "All",
            id = "crop-radio",
            inline = True,
            style = {"margin-bottom": 20})]),
        html.Div([
            
            # This container creates two empty dropdown menu objects,
            # its options are assigned based on user input and assigned in "callback" section of code
            
                html.Label(["Equipment Group:"], style = {"text-align": "left", "font-weight": "bold", 
                                                          "padding-left": 5}),
                dcc.Dropdown(
                    id = 'equip-group',
                    style = {"width": "55%", "margin-bottom": 20, "margin-top": 5, 
                            "padding-left": 5},
                    clearable = False),
                html.Label(["Parameter:"], style = {"text-align": "left", "font-weight": "bold", 
                                                    "padding-left": 5}),
                dcc.Dropdown(
                    id = "param-select",
                    style = {"width": "55%", "margin-top": 5,
                             "padding-left": 5},
                    clearable = False
                )
                     ]),
        
        # Generates two graph objects: one for the map, one for the graph.
        
        html.Div([dcc.Graph(id = "map-graph",
                 style = {"width": "45%", "display": "inline-block", "padding-left": 5}),
        dcc.Graph(id = "norm-graph",
                 style = {"width": "50%", "display": "inline-block"})],
                style = {"vertical-align": "center"}),
        dcc.Store(id = "drop-store",
                  data={'drop1': 'option1', 'drop2': 'option2'})
    ]),
)]

# Fills equipment group dropdown based on radio selection. Alphabetizes equipment group names for continuity.

@callback(
    Output("equip-group", "options"),
    Input("crop-radio", "value"))

def populate_dropdown(radio):
    if radio == "Almonds" or radio == "Grapes":
        return [{'label': i, 'value': i} for i in sorted(equip_dict.keys())]
    elif radio == "Olives" or radio == "Pistachios":
        return [{'label': i, 'value': i} for i in sorted(matt_dict.keys())]
    else:
        return [{'label': i, 'value': i} for i in sorted(equip_dict.keys())]

# Automatically puts an equipment group in dropdown to avoid error.
    
@callback(
    Output("equip-group", "value"),
    Input("equip-group", "options"))

def default_group(options):
    return options[0]['value']

# Populates second dropdown based on equipment selected in first dropdown.

@callback(
    Output("param-select", "options"),
    Input("equip-group", "value"),
    Input("crop-radio", "value"))

def talking_dropdown(selected_param, radio):
    if radio == "Almonds" or radio == "Grapes":
        return [{'label': i, 'value': i} for i in equip_dict[selected_param]]
    elif radio == "Olives" or radio == "Pistachios":
        return [{'label': i, 'value': i} for i in matt_dict[selected_param]]
    else:
        return [{'label': i, 'value': i} for i in equip_dict[selected_param]]

# Automatically places a parameter in dropdown to avoid error.
    
@callback(
    Output("param-select", "value"),
    Input("param-select", "options"))

def default_graph(options):
    return options[0]['value']

# # Attempt to store dropdown selections when changing radio options.
    
# @callback(
#     Output('drop-store', 'data'),
#     Input('crop-radio', 'value'),
#     State('equip-group', 'value'), 
#     State('param-select', 'value')
# )

# def update_store(radio_value, drop1_value, drop2_value):
#     return {'drop1': drop1_value, 'drop2': drop2_value}

# @callback(
#     Output('equip-group', 'value'),
#     Input('drop-store', 'data')
# )
# def update_dropdowns1(store_data):
#     return store_data['drop1']

# @callback(
#     Output('param_select', 'value'),
#     Input('drop-store', 'data')
# )
# def update_dropdowns2(store_data):
#     return store_data['drop2']


# Generates and customizes map.
# Displays sites on map depending on user input from radio items.

@callback(
    Output("map-graph", "figure"),
    Input("crop-radio", "value"))

def plot_map(sites):
    
    # Sets default zoom for plot depending on site, some crops have sites that are very close/far together/apart.
    
    if sites != "All":
        coords_temp = coords[coords["Crop"] == sites]
        if sites != "Almonds":
            h_set = 8
        else:
            h_set = 6.25
    else:
        coords_temp = coords
        h_set = 6
        
    fig = px.scatter_mapbox(coords_temp, lat = "Lat", lon = "Lon", hover_name = "Site",
                            zoom = h_set, height = 440,
                            center = {"lat": coords_temp.iloc[0,0], "lon": coords_temp.iloc[0,1]},
                            color = "Crop",
                            color_discrete_map={
                            "Almonds": "Blue",
                            "Olives": "Red",
                            "Pistachios": "Green",
                            "Grapes": "Purple"}
                            )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Generates a plot based on selected parameter and crop.

@callback(
    Output("norm-graph", "figure"),
    Input("crop-radio", "value"),
    Input("param-select", "value"))

def plot_graph(crops, yaxis_column_name):
    
    # Generates a data frame for plot based on crop selected.
    
    if crops == "All":
        sites = almonds + grapes + olives + pistachios
        temp = trex_all.Site.isin(sites)
        data_temp = trex_all[temp]
    elif crops == "Almonds":
        sites = almonds
        temp = trex_all.Site.isin(sites)
        data_temp = trex_all[temp]
    elif crops == "Grapes":
        sites = grapes
        temp = trex_all.Site.isin(sites)
        data_temp = trex_all[temp]
    elif crops == "Olives":
        sites = olives
        temp = matt_all.Site.isin(sites)
        data_temp = matt_all[temp]
    elif crops == "Pistachios":
        sites = pistachios
        temp = matt_all.Site.isin(sites)
        data_temp = matt_all[temp]
   
    fig = px.line(data_temp, x = data_temp.TIMESTAMP, y = data_temp[yaxis_column_name], color = data_temp.Site,
                 color_discrete_map={
                "BLS_001": "lime",
                "BLS_002": "blue",
                "ORO_022": "goldenrod",
                "ORO_043": "green",
                "COR_CS3": "magenta",
                "ART_011": "red",
                "OLA": "green",
                "WWF": "blue",
                "VAC": "red",
                "SLC": "goldenrod",
                "FLT": "lime",
                "WES": "magenta"},
                 height = 500)
    fig.update_layout(legend_title_text = "Sites (Click to Toggle)")
    
    # Assigns starting range for plot based on parameter.
    # Still allows user to pan up/down and left/right.
    
    ylow = int(rangedf[yaxis_column_name][0])
    yhi = int(rangedf[yaxis_column_name][1])
    fig.update_yaxes(range = [ylow, yhi], fixedrange = False)
    
    # Creates a slider to choose range of data you're viewing. Also has buttons which show last day, week, month.
    # All options are negotiable just placeholder for now.
    
    fig.update_layout(plot_bgcolor= "#efefef")
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1D",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="1W",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1M",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig

if __name__ == '__main__':
    app.run(debug=True)