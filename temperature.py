from scipy import io
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
import numpy as np
import os
# import plotly.graph_objects as go

outputfolder = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output/OLFA_110134_20-05-2024_R_T"

def calculateTime(time):
    hours = datetime.strptime(time, "%H:%M:%S").hour
    mins = datetime.strptime(time, "%H:%M:%S").minute
    seconds = datetime.strptime(time, "%H:%M:%S").second
    return (hours*3600+mins*60+seconds)

def D3Plot_TA_LFA(outputfolder,selectedtsnapindex,selectedconductor,scaflag,TACondutors):
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
    # fig = go.Figure(data = [go.Surface(z=final_z,x=super_x_axis,y=super_y_axis)])
    # fig.update_layout(title='TA LFA', autosize=False,
    #               width=1000, height=1000,
    #               margin=dict(l=65, r=50, b=65, t=90))
    # fig.show()
    ax.set_box_aspect(aspect = (10,8,6))
    surf = ax.plot_surface(super_x_axis,final_z, super_y_axis,cmap = cm.YlOrRd, rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False, alpha = 0.3)
    fig.colorbar(surf, ax=ax,shrink=0.5, aspect=5,pad=0.2)
    # for showing all the z ticks
    # zticks = []
    # for i in range(0, len(final_z)):
    #     zticks.append([])
    #     for j in range(0, len(final_z[i])):
    #         zticks[i].append(super_z_axis[i][j])
    # zvaluestoshow=[]
    # ztickstoshow =[]
    # for i in range(0, len(final_z)):
    #     for j in range(0, len(zticks)):
    #         zvaluestoshow.append(final_z[i][j])
    #         ztickstoshow.append(zticks[i][j])
    # ax.set_yticks(zvaluestoshow,ztickstoshow)
    ax.set(xlabel='Distance (km)', ylabel='Time (Hours)',zlabel="Temperature (Degree C)"if (selectedconductor==0 or selectedconductor==1) else "Temperature Difference (Degree C)")
    ax.view_init(elev=7, azim=63, roll=0)
    plt.title(TACondutors[selectedconductor])
    plt.tight_layout(pad=5)
    plt.show()

# For SCA, x axis is in TEMP_linesummary_sca.mat, y axis is in TEMP.mat, timesnaps?????
def D3Plot_TA_SCA (outputfolder,selectedconductor,scaflag,TACondutors):
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


# D3Plot_TA_LFA(outputfolder,[0,5],0,0,["Conductor 1","","",""])
