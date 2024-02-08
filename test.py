import pandas as pd
import matplotlib.pyplot as plt


def timeTableData(baseFolder):
    df = pd.read_csv("C:/Users/ashok/Desktop/IIT RESEARCH/SPIT_Interns_task/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Input_01_MTMM/TimeTableData.csv", header=None)
    rows = []
    final_dict = []
    for i in range(0, len(df)):
        if (df[0][i] == "TrainNumber "):
            rows.append(i)
    for j in range(0, len(rows)-1):
        stationName = []
        distanceFromStarting = []
        timeFromStarting = []
        dwelltime = []
        for k in range(rows[j]+4, rows[j+1]-1):
            stationName.append(df[1][k])
            distanceFromStarting.append(df[3][k])
            timeFromStarting.append(df[4][k])
            dwelltime.append(df[5][k])
        temp = {"trainnumber": df[0][rows[j]+1], "startTime": df[2][rows[j]+1],
                "stationName": stationName,
                "distanceFromStarting": distanceFromStarting,
                "timeFromStarting": timeFromStarting,
                "dwelltime": dwelltime}
        final_dict.append(temp)
    print(final_dict)


def routeAltitudeData(baseFolder):
    df2 = pd.read_csv(
        "C:/Users/ashok/Desktop/IIT RESEARCH/SPIT_Interns_task/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Input_01_MTMM/RouteAltitudeData.csv")
    print(df2)
    X_axis = df2["DistanceKM"]
    Y_axis = df2["HeightAboveGroundMSL"]
    plt.plot(X_axis, Y_axis)
    plt.legend()
    plt.show()
