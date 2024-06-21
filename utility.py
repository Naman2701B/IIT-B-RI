import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime, timedelta
import numpy as np
import mplcursors
from scipy import io
import os

conductors = ["Catenary (Uptrack)", "Rail1 (Uptrack)", "Rail2 (Uptrack)", "Catenary (Downtrack)", "Rail1 (Downtrack)",
                           "Rail2 (Downtrack)", "Feeder (Uptrack)", "Feeder (Downtrack)", "Protective Wire (Uptrack)", "Protective Wire (Downtrack)"]

def timeTableData(basefolderinput):
    df = pd.read_csv(os.path.join(basefolderinput,"TimeTableData.csv"), header=None)
    df2 = pd.read_csv(os.path.join(basefolderinput,"AllStationData.csv"))
    rows = []
    final_dict = []
    timingGraph = []
    distanceGraph = []
    timingGraphInHrsAndMins = []
    for i in range(0, len(df)):
        if (df[0][i] == "TrainNumber "):
            rows.append(i)
    rows.append(len(df)+1)
    for j in range(1, len(rows)):
        stationName = []
        distanceFromStarting = []
        timeFromStarting = []
        timeFromStarting_mins = []
        for k in range(rows[j-1]+4, rows[j]-1):
            stationName.append(df[1][k])
            distanceFromStarting.append(df[3][k])
            timeFromStarting_mins.append(int(df[4][k]))
        for i in range(0, len(timeFromStarting_mins)):
            values = df[2][rows[j-1]+1].split(":")
            h = int(timeFromStarting_mins[i]) // 60
            m = int(timeFromStarting_mins[i]) % 60
            timeFromStarting.append(str(timedelta(
                hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
            timingGraphInHrsAndMins.append(timeFromStarting[i])
        for i in range(0, len(timeFromStarting_mins)):
            timeFromStarting_mins[i] = timeFromStarting_mins[i] + \
                int(datetime.strptime(df[2][rows[j-1]+1], "%H:%M").minute)
            timingGraph.append(timeFromStarting_mins[i])
            distanceGraph.append(int(distanceFromStarting[i]))
        temp = {"trainnumber": df[0][rows[j-1]+1], "startTime": df[2][rows[j-1]+1], "endDistance": df[3][rows[j-1]+len(stationName)+3], "startDistance": df[3][rows[j-1]+4],
                "trainType": df[6][rows[j-1]+1],
                "stationName": stationName,
                "distanceFromStarting": distanceFromStarting,
                "timeFromStarting": timeFromStarting,
                "timeFromStartingInMins": timeFromStarting_mins}
        final_dict.append(temp)
    splitDuration = (max(timingGraph) - min(timingGraph))//8
    splitDistance = (max(distanceGraph)-min(distanceGraph))//5
    timingGraph = [min(timingGraphInHrsAndMins)]
    distanceToReplace = df2["DistanceKMWithReferenceToStartingStation"].to_list()
    distanceGraph = [min(distanceGraph)]
    timeToReplaceInMins = [0]
    values = timingGraph[0].split(":")
    for i in range(1, 9):
        timeToReplaceInMins.append(int(timeToReplaceInMins[i-1]+splitDuration))
        h = int(timeToReplaceInMins[i]//60)
        m = int(timeToReplaceInMins[i]) % 60
        timingGraph.append(str(timedelta(
            hours=h, minutes=m) + timedelta(hours=int(values[0]), minutes=int(values[1]))))
    for i in range(1, 6):
        distanceGraph.append(distanceGraph[i-1]+splitDistance)
    dataToBeSent = {"calculativeData": final_dict,
                    "plottingData": [timingGraph, timeToReplaceInMins, distanceGraph, distanceToReplace]}
    return dataToBeSent


def routeAltitudeData(basefolder):
    df2 = pd.read_csv(os.path.join(basefolder ,"RouteAltitudeData.csv"))
    df3 = pd.read_csv(os.path.join(basefolder , "AllStationData.csv"))
    X_axis = df2["DistanceKM"]
    Y_axis = df2["HeightAboveGroundMSL"]
    markers_onx = []
    markers_ony = []
    station_names = []
    for i in range(0, len(df3["DistanceKMWithReferenceToStartingStation"])):
        markers_onx.append(df3["DistanceKMWithReferenceToStartingStation"][i])
        station_names.append(df3["StationName "][i])
    for i in range(0, len(X_axis)):
        if X_axis[i] in markers_onx:
            markers_ony.append(Y_axis[i])
    plt.scatter(markers_onx, markers_ony)
    for i, txt in enumerate(station_names):
        plt.annotate(
            txt, (markers_onx[i], markers_ony[i]), horizontalalignment='center')
    plt.plot(X_axis, Y_axis)
    plt.title('Route-Altitude graph', fontsize=15, fontweight='bold')
    plt.xlabel("Stations", fontsize=15, fontweight='bold')
    plt.ylabel("Altitude (m)", fontsize=15, fontweight='bold')
    plt.grid(alpha=0.3)
    cursor = mplcursors.cursor(hover=True)
    plt.show(block = False)


def TractiveEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    df_y = pd.read_csv(os.path.join(basefolderoutput,"EffortOutput.csv"))
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["TractiveEffort_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def BrakingEffortData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    df_y = pd.read_csv(os.path.join(basefolderoutput,"EffortOutput.csv"))
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["BrakingEffort_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def ReactivePowerData(basefolderinput, basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    df_p = pd.read_csv(os.path.join(basefolderinput,"TrainElectricalData.csv"), header=1)
    X_axis = []
    Y_axis = []
    inputdata = timeTableData(basefolderinput)
    for j in range(0, len(inputdata["calculativeData"])):
        if (inputdata["calculativeData"][j]["trainnumber"] == selected_trains):
            t_type = inputdata["calculativeData"][j]["trainType"]
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    result = df_p[str(t_type)][16]
    temp_y = df_x["ActivePower_"+partstr+"_"+str(selected_trains)+"_0"]
    Y_axis.append(temp_y*np.tan(np.arccos(result)))
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def ActivePowerData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_x["ActivePower_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis


def CurrentData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    df_y = pd.read_csv(os.path.join(basefolderoutput,"EffortOutput.csv"))
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_y["TractiveEffort_"+partstr +
                       "_"+str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    plt.plot(X_axis, Y_axis)
    plt.show(block = False)


def VoltageData(basefolderoutput, selected_trains, timeFlag):
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    df_y = pd.read_csv(os.path.join(basefolderoutput,"EffortOutput.csv"))
    X_axis = []
    Y_axis = []
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis = df_y["TractiveEffort_"+partstr +
                  "_"+str(selected_trains)+"_0"]
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    plt.plot(X_axis, Y_axis)
    plt.show(block = False)


def VelocityData(basefolderoutput, selected_trains, timeFlag):
    X_axis = []
    Y_axis = []
    df_x = pd.read_csv(os.path.join(basefolderoutput,"TrainModuleOutput.csv"))
    if (int(df_x["Up/Downtrack_"+str(selected_trains)+"_0"][0]) == 0):
        partstr = "Uptrack"
    else:
        partstr = "Downtrack"
    Y_axis.append(df_x["Velocity_"+partstr+"_" +
                       str(selected_trains)+"_0"])
    if (timeFlag == 1):
        X_axis.append(round(
            df_x["Time_"+partstr+"_"+str(selected_trains)+"_0"]*60))
    else:
        X_axis.append(df_x["Distance_"+partstr+"_" +
                           str(selected_trains)+"_0"])
    return X_axis, Y_axis

def D3plot(xvalues, super_y_axis, zvalue, radioflag, pqa_lfa,selectedconductors,conductors):
    ax = plt.figure().add_subplot(projection='3d')
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_box_aspect(aspect = (4,2,1))
    if(pqa_lfa==0):
        for i in range(0, len(zvalue)):
            for j in range(0, len(zvalue[i])):
                zvalue[i][j] = calculateTime(zvalue[i][j])
        zvalue = np.array(zvalue)
        super_y_axis = np.array(super_y_axis)
        ax.plot_surface(xvalues, zvalue, super_y_axis,edgecolor = 'black',cmap = cm.Spectral, rstride=1, cstride=8,linewidth = 0.3, antialiased=False, shade=True, alpha = 0.3)
        ax.view_init(elev=20, azim=-145, roll=0)
        ax.set(xlabel='Distance (km)',ylabel='Time (Hrs)', zlabel=conductors[selectedconductors]+" Voltage (kV)" if radioflag == 0 else conductors[selectedconductors]+" Current (kA)")
        plt.title("Load Flow Analysis 3D")
    else:
        for i in range(0, len(zvalue)):
            zticks.append([])
            for j in range(0, len(zvalue[i])):
                zticks[i].append(zvalue[i][j])
        zvalue = np.array(zvalue)   
        zticks = np.array(zticks)
        super_y_axis = np.array(super_y_axis)
        ax.plot_surface(xvalues, zvalue, super_y_axis, edgecolor='black',cmap = cm.Spectral, rstride=1, cstride=8, linewidth=0.3, antialiased=False,shade = True, alpha = 0.3)
        ax.view_init(elev=20, azim=-145, roll=0)
        zvaluestoshow=[]
        ztickstoshow =[]
        for i in range(0, len(zvalue)):
            for j in range(0, len(zticks)):
                zvaluestoshow.append(zvalue[i][j])
                ztickstoshow.append(zticks[i][j]*50)
        ax.set_yticks(zvaluestoshow, ztickstoshow)
        ax.set(xlabel='Distance (km)',
            ylabel='Frequencies (Hz)', zlabel=conductors[selectedconductors]+" Voltage (kV)" if radioflag == 0 else conductors[selectedconductors]+" Current (kA)")
        plt.title("Power Quality Analysis 3D")
    plt.show(block = False)


def loadFlowAnalysis(outputfolder, selectedtsnapindex, selectedconductor, radioflag, flag_3d, IAflag):
    if IAflag == 1:
        file = io.loadmat(file_name=os.path.join(outputfolder,"IA_Output.mat"))
    else:
        file = io.loadmat(file_name=os.path.join(outputfolder,"data_ntwrk.mat"))
    x_axis = []
    super_y_axis = []
    super_x_axis = []
    z_values = []
    if IAflag==0:
        for i in range(0, len(file["dev_seqn"])):
            if "line_" in str(file["dev_seqn"][i][0][0]):
                x_axis.append(float(file["dev_seqn"][i][3][0][0]))
    else:
        for i in range(0,len(file["section_length_main"])):
            x_axis.append(float(file["section_length_main"][i][1]))
    # x axis label is chainage in kilometers
    tsnap = file["tsnap"]
    if IAflag == 0:
        file2 = io.loadmat(file_name=os.path.join(outputfolder,"line_summary.mat"))
    else:
        file2 = io.loadmat(file_name = os.path.join(outputfolder,"IA_Output.mat"))
    if radioflag == 1:
        for i in range(len(selectedtsnapindex)):
            y_axis = []
            z_axis = [tsnap[selectedtsnapindex[i]]]
            y_axis.append(float(abs(file2['Line_Currents' if IAflag==0 else 'Cable_current']
                                    [selectedconductor][0][selectedtsnapindex[i]])))
            for j in range(len(file2["Line_Currents" if IAflag==0 else 'Cable_current'][0])):
                y_axis.append(float(abs(file2['Line_Currents' if IAflag==0 else 'Cable_current']
                                        [selectedconductor+10 if IAflag==0 else selectedconductor][j][selectedtsnapindex[i]])))
                z_axis.append(tsnap[selectedtsnapindex[i]])
            z_values.append(z_axis)
            super_y_axis.append(y_axis)
    else:
        for i in range(len(selectedtsnapindex)):
            y_axis = []
            z_axis = []
            z_axis = [tsnap[selectedtsnapindex[i]]]
            y_axis.append(float(abs(file2['Line_Voltages' if IAflag==0 else 'Cableterminal_voltage']
                                    [selectedconductor][0][selectedtsnapindex[i]])/1000))
            for j in range(len(file2["Line_Voltages" if IAflag==0 else 'Cableterminal_voltage'][0])):
                y_axis.append(float(abs(file2['Line_Voltages' if IAflag==0 else 'Cableterminal_voltage']
                                        [selectedconductor+10 if IAflag==0 else selectedconductor][j][selectedtsnapindex[i]])/1000))
                z_axis.append(tsnap[selectedtsnapindex[i]])
            z_values.append(z_axis)
            super_y_axis.append(y_axis)
    for j in range(0, len(selectedtsnapindex)):
        xvalues = [0]
        for i in range(0, len(x_axis)):
            xvalues.append(x_axis[i])
        super_x_axis.append(xvalues)
    if flag_3d == 0:
        return super_x_axis, super_y_axis
    else:
        D3plot(super_x_axis, super_y_axis, z_values, radioflag,0,selectedconductor,conductors)

def powerQualityAnalysis(outputfolder, selectedfrequency,selectedconductor, radioflag, flag_3d,IAflag):
    if IAflag==0:
        file = io.loadmat(file_name=os.path.join(outputfolder,"IA_linesummary.mat"))
    else:
        file = io.loadmat(file_name=os.path.join(outputfolder,"IA_Output.mat"))
    x_axis = []
    super_y_axis = []
    super_x_axis = []
    z_values = []
    if IAflag==0:
        for i in range(0, len(file["dev_seqn"])):
            if "line_" in str(file["dev_seqn"][i][0][0]):
                x_axis.append(float(file["dev_seqn"][i][3][0][0]))
    else:
        for i in range(0,len(file["section_length_main"])):
            x_axis.append(float(file["section_length_main"][i][1]))
    # x axis label is chainage in kilometers
    frequency = list(file["fh"][0])
    if IAflag == 0:
        file2 = io.loadmat(file_name=os.path.join(outputfolder,"line_summary_PQA.mat"))
    else:
        file2 = io.loadmat(file_name = os.path.join(outputfolder,"IA_Output.mat"))
    if radioflag == 1:
        for i in range(len(selectedfrequency)):
            y_axis = []
            z_axis = [frequency[selectedfrequency[i]]]
            y_axis.append(float(abs(file2['Line_Currents'if IAflag==0 else 'Cable_current']
                                    [selectedconductor][0][selectedfrequency[i]])))
            for j in range(len(file2["Line_Currents"if IAflag==0 else 'Cable_current'][0])):
                y_axis.append(float(abs(file2['Line_Currents'if IAflag==0 else 'Cable_current']
                                        [(selectedconductor+10) if IAflag==0 else selectedconductor][j][selectedfrequency[i]])))
                z_axis.append(frequency[selectedfrequency[i]])
            z_values.append(z_axis)
            super_y_axis.append(y_axis)
    else:
        for i in range(len(selectedfrequency)):
            y_axis = []
            z_axis = []
            z_axis = [frequency[selectedfrequency[i]]]
            y_axis.append(float(abs(file2['Line_Voltages'if IAflag==0 else 'Cableterminal_voltage']
                                    [selectedconductor][0][selectedfrequency[i]])/1000))
            for j in range(len(file2["Line_Voltages"if IAflag==0 else 'Cableterminal_voltage'][0])):
                y_axis.append(float(abs(file2['Line_Voltages'if IAflag==0 else 'Cableterminal_voltage']
                                        [(selectedconductor+10) if IAflag==0 else selectedconductor][j][selectedfrequency[i]])/1000))
                z_axis.append(frequency[selectedfrequency[i]])
            z_values.append(z_axis)
            super_y_axis.append(y_axis)
    for j in range(0, len(selectedfrequency)):
        xvalues = [0]
        for i in range(0, len(x_axis)):
            xvalues.append(x_axis[i])
        super_x_axis.append(xvalues)
    if flag_3d == 0:
        return super_x_axis, super_y_axis
    else:
        D3plot(super_x_axis, super_y_axis, z_values, radioflag,1,selectedconductor,conductors)

def ShortCircuitAnalysis(outputfolder, selectedconductor,conductors, radioflag):
    file = io.loadmat(file_name=os.path.join(outputfolder,"line_summary_SCA.mat"))
    file2 = io.loadmat(file_name = os.path.join(outputfolder,"IA_linesummary.mat"))
    x_axis = [{"label":file2["dev_seqn"][0][0][0],"data":float(file2["dev_seqn"][0][3][0][0])}]
    xvalues=[]
    y_axis = []
    for i in range(len(file2["dev_seqn"])):
        if "line_" in str(file2["dev_seqn"][i][0][0]):
            x_axis.append({"label": file2["dev_seqn"][i][0][0], "data": float(file2["dev_seqn"][i][3][0][0])})
    if radioflag==1:
        y_axis.append(float(abs(file['Line_Currents'][selectedconductor][0]))/1000)
        for j in range(len(file["Line_Currents"][0])):
            y_axis.append(float(abs(file['Line_Currents'][selectedconductor+10][j]))/1000)
        plt.ylabel((conductors[selectedconductor]+" Currents (kA)"),fontsize=15, fontweight='bold')
    else:
        y_axis.append(float(abs(file['Line_Voltages'][selectedconductor][0]))/1000)
        for j in range(len(file["Line_Voltages"][0])):
            y_axis.append(float(abs(file['Line_Voltages'][selectedconductor+10][j])/1000))
        plt.ylabel((conductors[selectedconductor]+" Voltages (kV)"),fontsize=15, fontweight='bold')
    for i in range(len(x_axis)):
        xvalues.append(x_axis[i]["data"])
    plt.plot(xvalues, y_axis, label = file2["timesnap"][0])
    plt.title("Short Circuit Analysis",fontsize=15, fontweight='bold')
    plt.xlabel("Distance (km)",fontsize=15, fontweight='bold')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show(block = False)

def ShortCircuitAnalysis_IA(outputfolder, selectedconductor,conductors, radioflag):
    file = io.loadmat(file_name=os.path.join(outputfolder,"IA_Output.mat"))
    x_axis = []
    xvalues=[]
    y_axis = []
    for i in range(len(file["section_length_main"])):
        x_axis.append(float(file["section_length_main"][i][1]))
    if radioflag==1:
        for j in range(len(file['Cable_current'][0])):
            y_axis.append(float(abs(file['Cable_current'][selectedconductor][j]))/1000)
        plt.ylabel((conductors[selectedconductor]+" Currents (kA)"),fontsize=15, fontweight='bold')
    else:
        for j in range(len(file['Cableterminal_voltage'][0])):
            y_axis.append(float(abs(file['Cableterminal_voltage'][selectedconductor][j])/1000))
        plt.ylabel((conductors[selectedconductor]+" Voltages (kV)"),fontsize=15, fontweight='bold')
    for i in range(len(x_axis)):
        xvalues.append(x_axis[i])
    plt.plot(xvalues, y_axis)
    plt.title("Current in Signalling Cables" if radioflag==1 else "Terminal Voltage in Signalling Cables",fontsize=15, fontweight='bold')
    plt.xlabel("Distance (km)",fontsize=15, fontweight='bold')
    plt.xlim(left=0, right=max(x_axis))
    plt.grid(alpha=0.3)
    plt.show(block = False)


def calculateTime(time):
    hours = datetime.strptime(time, "%H:%M:%S").hour
    mins = datetime.strptime(time, "%H:%M:%S").minute
    seconds = datetime.strptime(time, "%H:%M:%S").second
    return (hours+mins/60+seconds/3600)