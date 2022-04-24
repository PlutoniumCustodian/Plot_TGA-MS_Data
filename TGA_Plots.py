# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:43:30 2022

@author: Titus
"""
# Used to import TGA and MS data from excell files exported from TA Trios Software
#%% Intial setup
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.font_manager import FontProperties

#%% Import data

datpath = 'TGA_MS_ExcelData' # directory where data is stored relative to py script location
f_name = (os.listdir(datpath))#list of files in the directory of datpath

file_count = range(len(f_name))
TGA_names = []
MS_names = []

# Makes a list of TGA file and a seprate list of MS files
for x in file_count:
    # test = re.search("^MS",f_name[x])
    # if test != 'None':
    #     MS_names.append(f_name[x])
    # test = re.search("^TGA",f_name[x])
    # if test != 'None':
    #     TGA_names.append(f_name[x])
    if f_name[x].startswith('MS'):
        MS_names.append(f_name[x])
    if f_name[x].startswith('TGA'):
        TGA_names.append(f_name[x])
# Check that you have the same number of TGA and MS files
if len(MS_names) != len(TGA_names):
    print('Error MS and TGA data not matched')

TGA_MS_count = range(len(MS_names))
TGA_listOdf = []
MS_H2O_listOdf = []
MS_CO2_listOdf = []

#Read in the data from excell
for x in TGA_MS_count:
    #Read the TGA data
    tempTGA = pd.read_excel(os.path.join(datpath, TGA_names[x]), sheet_name=1, header=[1,2])
    TGA_listOdf.append(tempTGA)
    #Read the MS data
    tempMS_H20 = pd.read_excel(os.path.join(datpath, MS_names[x]), sheet_name="18.0 AMU", header=[1,2])
    MS_H2O_listOdf.append(tempMS_H20)
    tempMS_C02 = pd.read_excel(os.path.join(datpath, MS_names[x]), sheet_name="44.0 AMU", header=[1,2])
    MS_CO2_listOdf.append(tempMS_C02)

#%%get names for plot lables

Graph_Title = []
for x in TGA_MS_count:
    #find the end of the PC name by finding first number
    m = re.search(r"\d", TGA_names[x])
    temp_name = TGA_names[x][4 : m.span()[1]-1]
    temp_name = temp_name.replace("Axial", "-Axial")
    temp_name = temp_name.replace("Corner", "-Corner")
    Graph_Title.append(temp_name)
    
#%% Ready to polot ?

#Values for setting that are used multple places
ColPal = ['#256676', '#1f0133', '#696fc4', '#9b1b5c']
lnthikness= 0.5
legspot = 'upper right' # Determines where legend is placed

font = FontProperties()
font.set_family('sans-serf')
font.set_name('Arial')
font.set_size(9)
index = 1
# def TGA_MS_plot(index):
#Get TGA data out of dataframe
df = TGA_listOdf[index]
TGA_T = np.array(df.loc[:,'Temperature'])
TGA_M = np.array(df.loc[:,'Weight'])
TGA_dM = np.array(df.loc[:,'Deriv. Weight'])
# TGA_dM = TGA_dM[:,0] # gits rid of repeated dM data

#Get MS Data
df = MS_CO2_listOdf[index]
CO2_sig = np.array(df.loc[:,'Ion Current'])
CO2_T = np.array(df.loc[:,'Temperature'])
df = MS_H2O_listOdf[index]
H2O_sig = np.array(df.loc[:,'Ion Current'])
H2O_T = np.array(df.loc[:,'Temperature'])

# Plotting
fig, ax = plt.subplots() #size is in inches
plt.title(Graph_Title[index])
ax.plot(TGA_T,TGA_M, linewidth=lnthikness, color=ColPal[1])    
ax.set_xlabel("Temperature (°C)", fontsize=9)
ax.set_ylabel("Weight (%)", fontsize=9, color=ColPal[1])
ax.tick_params(axis='x', labelsize=8)
ax.xaxis.set_major_locator(MultipleLocator(100))
ax.xaxis.set_minor_locator(MultipleLocator(25))
ax.tick_params(axis='y', labelsize=8, colors=ColPal[1])
ax.set_xlim([30,1000])
ax.set_ylim([60,100])

ax2=ax.twinx()
ax2.plot(TGA_T,TGA_dM, linewidth=lnthikness, color=ColPal[0])
ax2.tick_params(axis='y', labelsize=8, colors=ColPal[0])
ax2.set_ylabel("Derivitave Weight (% / °C)", fontsize=9, color=ColPal[0])
ax2.set_ylim([-.3,.3])

# ax[1].plot(TGA_T,TGA_dM, linewidth=lnthikness)  



# # Hide x labels and tick labels for all but bottom plot.
# for ax in axs:
#     ax.label_outer()
    
    # ax.set_xlim(ylimits)
    # # ax.set_ylim(xlimits)
    # ax.xaxis.set_minor_locator(MultipleLocator(2.5))
    # ax.yaxis.set_ticklabels([])
    # ax.tick_params(axis='y',length=0)
    # plt.title(plt_title)
    # # ax.legend()
    # #Revers order of legend lables
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles[::-1], labels[::-1])

    # svg_name_path = 'Plots/' + svg_file_name + '.svg'
    # # Uncomment this line to save the figure.
    # fig.savefig(svg_name_path, transparent=False, bbox_inches="tight")
    # return fig