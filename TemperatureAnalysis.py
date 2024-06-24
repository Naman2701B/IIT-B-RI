"""
TemperatureAnalysis.py

This module is part of the railway simulation software and provides functionalities for analyzing temperature data and generating 3D plots for load flow analysis (LFA) and short circuit analysis (SCA). It uses various libraries for data processing and visualization.

Imports:
    - scipy.io: Used for reading and writing MATLAB files.
    - matplotlib.pyplot: Used for creating static, animated, and interactive visualizations.
    - cm: Colormap from matplotlib.
    - datetime: Used for manipulating dates and times.
    - numpy: Used for numerical operations.
    - os: Provides a way of using operating system dependent functionality.

Global Variables:
    - outputfolder: The path to the folder containing the output files.

Functions:
    - calculateTime(time): Converts time in HH:MM:SS format to total seconds.
    - D3Plot_TA_LFA(outputfolder, selectedtsnapindex, selectedconductor, scaflag, TACondutors): Generates a 3D plot for load flow analysis (LFA).
    - D3Plot_TA_SCA(outputfolder, selectedtsnapindex, selectedconductor, scaflag, TACondutors): Generates a 3D plot for short circuit analysis (SCA).
"""

from scipy import io
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
import numpy as np
import os

outputfolder = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output/OLFA_110134_20-05-2024_R_T"

def calculateTime(time):
    """Converts a time string in "HH:MM:SS" format to the total number of seconds.

    This function parses the given time string, extracts the hours, minutes, and seconds,
    and calculates the total number of seconds.

    Parameters:
    time (str): A string representing time in "HH:MM:SS" format.

    Returns:
    int: The total number of seconds."""
    hours = datetime.strptime(time, "%H:%M:%S").hour
    mins = datetime.strptime(time, "%H:%M:%S").minute
    seconds = datetime.strptime(time, "%H:%M:%S").second
    return (hours*3600+mins*60+seconds)

def D3Plot_TA_LFA(outputfolder,selectedtsnapindex,selectedconductor,scaflag,TACondutors):
    """Generates a 3D plot for thermal analysis in load flow analysis.

    This function loads thermal analysis data from MATLAB files, processes the data, and generates
    a 3D surface plot to visualize the temperature distribution over time and distance for the selected
    conductor and time snapshots.

    Parameters:
    outputfolder (str): The path to the folder containing the thermal analysis data.
    selectedtsnapindex (list): A list of indices for the selected time snapshots.
    selectedconductor (int): The index of the selected conductor.
    scaflag (int): Flag indicating if the analysis is for SCA (1) or not (0).
    TACondutors (list): A list of conductor names.

    Returns:
    None"""
    font = {'family': 'serif',
    'color':  'black',
    'weight': 'bold',
    'size': 16,
    }
    fig, ax = plt.subplots(figsize=(20,15),subplot_kw={"projection": "3d"})
    fig.set_figheight(20)
    fig.set_figwidth(25)
    if scaflag==0:
        file1 = io.loadmat(file_name=os.path.join(outputfolder,"data_ntwrk.mat"))
    else:
        file1 = io.loadmat(file_name=os.path.join(outputfolder,"../data_ntwrk.mat"))
    allfiles = os.listdir(outputfolder)
    for i in range (len(allfiles)):
        finalfolder = os.path.join(outputfolder,allfiles[i])
        if os.path.isdir(finalfolder) and 'TEMP' in allfiles[i]:
            break
    file2 = io.loadmat(file_name=os.path.join(finalfolder,"Temp.mat"))
    tsnap = file1['tsnap']
    super_x_axis = []
    super_y_axis = []
    super_z_axis = []
    for i in range(len(selectedtsnapindex)):
        y_axis =[]
        z_axis =[]
        for j in range(len(file2['Tavg'][0])):
            y_axis.append(float(file2['Tavg' if (selectedconductor==0 or selectedconductor==1)else 'diff_Tavg'][selectedtsnapindex[i]][j][selectedconductor]))
            z_axis.append(tsnap[selectedtsnapindex[i]])
        super_y_axis.append(y_axis)
        super_z_axis.append(z_axis)
    for i in range(len(selectedtsnapindex)):
        x_axis =[]
        x_axis.append(float(0))
        for j in range(0, len(file1["dev_seqn"])):
            if "line_" in str(file1["dev_seqn"][j][0][0]):
                x_axis.append(float(file1["dev_seqn"][j][3][0][0]))
        super_x_axis.append(x_axis)
    super_x_axis = np.array(super_x_axis)
    super_y_axis = np.array(super_y_axis)
    final_z = []
    for i in range (len(super_z_axis)):
        zshow = []
        for j in range(0, len(super_z_axis[i])):
            zshow.append((calculateTime(super_z_axis[i][j]))/3600)
        final_z.append(zshow)
    final_z = np.array(final_z)
    ax.set_box_aspect(aspect = (10,8,6))
    surf = ax.plot_surface(super_x_axis,final_z, super_y_axis,cmap = cm.YlOrRd, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False, alpha = 0.3)
    fig.colorbar(surf, ax=ax,shrink=0.5, aspect=5,pad=0.2)
    ax.set_xlabel('Distance (km)', fontdict = font)
    ax.set_ylabel('Time (Hours)', fontdict = font)
    ax.set_zlabel("Temperature (Degree C)"if (selectedconductor==0 or selectedconductor==1) else "Temperature Difference (Degree C)", fontdict = font)
    # ax.set(xlabel='Distance (km)', ylabel='Time (Hours)',zlabel="Temperature (Degree C)"if (selectedconductor==0 or selectedconductor==1) else "Temperature Difference (Degree C)")
    ax.view_init(elev=7, azim=63, roll=0)
    plt.title(TACondutors[selectedconductor], fontdict=font)
    plt.tight_layout(pad=5)
    plt.show()

def D3Plot_TA_SCA (outputfolder,selectedconductor,scaflag,TACondutors):
    """Generates a 3D plot for thermal analysis in short circuit analysis (SCA).

    This function loads thermal analysis data and time snapshot data from MATLAB files, processes the data, 
    and calls the `D3Plot_TA_LFA` function to generate a 3D surface plot. The plot visualizes the temperature 
    distribution over time and distance for the selected conductor.

    Parameters:
    outputfolder (str): The path to the folder containing the thermal analysis data.
    selectedconductor (int): The index of the selected conductor.
    scaflag (int): Flag indicating if the analysis is for SCA (1) or not (0).
    TACondutors (list): A list of conductor names.

    Returns:
    None"""
    file1 = io.loadmat(file_name = os.path.join(outputfolder,"../data_ntwrk.mat"))
    file3 = io.loadmat(file_name= os.path.join(outputfolder,"IA_linesummary.mat"))
    sc_tsnap = file3['timesnap']
    temp_tsnap = file1['tsnap']
    tsnap = []
    i=0
    while (temp_tsnap[i]!= sc_tsnap[0]):
        tsnap.append(i)
        i +=1
    D3Plot_TA_LFA(outputfolder,tsnap,selectedconductor,scaflag,TACondutors)