from fpdf import FPDF
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import re

outputFolder = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output"

def hist_report(outputFolder):
    file = pd.read_csv(outputFolder+"/TrainResults.csv")
    columns = []
    for c in file.columns:
        if "Avg zonal voltage(V)_" in c:
            columns.append(c)
    temp = []
    images = []
    for i in range(len(columns)):
        temp.append(re.findall("\d+",columns[i]))
    for k in range(len(file)):
        fig,ax = plt.subplots()
        x_axis = []
        y_axis = []
        x_axis.append(0)
        y_axis.append(0)
        x = []
        for i in range (len(columns)):
            x.append(file.iloc[k][columns[i]])
        for i in range(len(x)):
            for m in range(int(temp[i][0]), int(temp[i][1])+1):
                x_axis.append(m)
                y_axis.append(x[i]/1000)
            x_axis.append(int(temp[i][1]))
            y_axis.append(0)
        plt.plot(x_axis,y_axis)
        plt.fill_between(x_axis,y_axis, 0, color='blue', alpha=.1)
        plt.title(int(file.iloc[k][0]))
        plt.xlim(left = 0, right = max(x_axis))
        plt.ylim(bottom = 0)
        plt.xlabel("Distance in kms")
        plt.ylabel("Avg Zonal Voltage (kV)")
        canvas = FigureCanvas(fig)
        canvas.draw()
        img1 = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        images.append(img1)
        # plt.legend()
    return images


def startReport(outputFolder, data):
    file = pd.read_csv(outputFolder+"/SubstationResults.csv")
    file2 = pd.read_csv(outputFolder+"/TrainResults.csv")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=18, style="B")
    pdf.cell(pdf.epw, 20, "Train Substation Results",align="C",ln=1)
    pdf.set_font("Times", size=8)
    with pdf.table(width=100, text_align="CENTER",align="LEFT",) as table:
        headings = table.row()
        headings.cell("")
        for j in range(0, len(file)):
            headings.cell("TSS"+str(j+1), colspan=2)
        headings = table.row()
        headings.cell("")
        for j in range(0, len(file)):
            headings.cell("Left Feed")
            headings.cell("Right Feed")
        row = table.row()
        row.cell("Max Insantaneous Current(A)")
        for j in range(0, len(file)):
            row.cell(str(round(float(file["Max instantaneous current SPT1(A)"][j]),2)))
            row.cell(str(round(float(file["Max instantaneous current SPT2(A)"][j]),2)))
        row1 = table.row()
        row1.cell("Max Moving Avg Current (1min)")
        for j in range(0, len(file)):
            row1.cell(str(round(float(file["Max moving average current SPT1(A,1min)"][j]),2)))
            row1.cell(str(round(float(file["Max moving average current SPT2(A,1min)"][j]),2)))
        row2=table.row()
        row2.cell("Max Moving Avg Current (5min)")
        for j in range(0, len(file)):
            row2.cell(str(round(float(file["Max moving average current SPT1(A,5min)"][j]),2)))
            row2.cell(str(round(float(file["Max moving average current SPT2(A,5min)"][j]),2)))  
    for i in range(0,len(file)):
        fig1,ax1 = plt.subplots()
        fig2,ax2 = plt.subplots()
        pie1 = float(file["Supplied energy without Transformer losses SPT1(kWh)"][i])
        pie2 = float(abs(file["Regenerative energy without Transformer losses SPT1(kWh)"][i]))
        pie3 = float(file["Supplied energy without Transformer losses SPT2(kWh)"][i])
        pie4 = float(abs(file["Regenerative energy without Transformer losses SPT2(kWh)"][i]))
        data_labels1 = ["Supplied energy without losses SPT1(kWh)","Regenerative energy without losses SPT1(kWh)"]
        data_labels2 = ["Supplied energy without losses SPT2(kWh)","Regenerative energy without losses SPT2(kWh)"]
        data1 = np.array([pie1,pie2])
        data2 = np.array([pie3,pie4])
        ax1.set_title("Left Feed Data", loc="left")
        ax1.pie(data1, autopct = '%.2f')
        ax1.legend(labels = data_labels1, bbox_to_anchor=(0.9,1), loc="center")
        ax2.set_title("Right Feed Data",loc = "left")
        ax2.pie(data2, autopct = '%.2f')
        ax2.legend(labels = data_labels2, bbox_to_anchor=(0.9,1), loc="center")
        canvas1 = FigureCanvas(fig1)
        canvas2 = FigureCanvas(fig2)
        canvas1.draw()
        img1 = Image.fromarray(np.asarray(canvas1.buffer_rgba()))
        pdf.image(img1,w=pdf.epw/2.5, x=120, y=30*(i+1))
        canvas2.draw()
        img2 = Image.fromarray(np.asarray(canvas2.buffer_rgba()))
        pdf.image(img2,w=pdf.epw/2.5, x=120, y=35+50*(i+1))
    pdf.add_page()
    pdf.set_font("Helvetica", size=18,style="B")
    pdf.cell(pdf.epw, 20, "Train Plot Results",align="C",ln=1)
    pdf.set_font("Times", size=8)
    with pdf.table(text_align="CENTER") as table:
        headings=table.row()
        headings.cell("")
        for i in range(len(file2)):
            headings.cell(str(file2["Train number"][i]))
        row1 = table.row()
        row1.cell("Start Time (in hh:mm)")
        for i in range(len(file2)):
            row1.cell(data[i]["startTime"])
        row2 = table.row()
        row2.cell("Maximum Voltage (kV)")
        for i in range(len(file2)):
            row2.cell(str(round(float(file2["Maximum Voltage (V)"][i])/1000,2)))
        row3 = table.row()
        row3.cell("Minimum Voltage (kV)")
        for i in range(len(file2)):
            row3.cell(str(round(float(file2["Minimum Voltage (V)"][i])/1000,2)))
        row4 = table.row()
        row4.cell("Mean Useful Voltage (kV)")
        for i in range(len(file2)):
            row4.cell(str(round(float(file2["U mean useful (train V)"][i])/1000,2)))
        row5 = table.row()
        row5.cell("Travel Time")
        for i in range(len(file2)):
            temp = int(file2["Travelling time (in second)"][i])
            m = temp // 60
            s = temp % 60
            row5.cell(str(timedelta(minutes=m, seconds=s)))
        row6 = table.row()
        row6.cell("End Time (in hh:mm:ss)")
        for i in range(len(file2)):
            temp1 = data[i]["startTime"].split(":")
            hours = int(temp1[0])
            minutes = int(temp1[1])
            temp = int(file2["Travelling time (in second)"][i])
            m = temp // 60
            s = temp % 60
            row6.cell(str(timedelta(hours=hours, minutes=minutes)+timedelta(minutes=m,seconds=s)))
    values = hist_report(outputFolder)
    j=-60
    for i in range(len(values)):
        pdf.image(values[i],w=pdf.epw/2.5, x=70+j, y=120+60*(i//2))
        j=j*(-1)
    pdf.output("matplotlib.pdf")
    return

# startReport(outputFolder)
# fig = Figure(figsize=(6, 4), dpi=300)
# fig.subplots_adjust(top=0.8)
# ax1 = fig.add_subplot(211)
# ax1.set_ylabel("volts")
# ax1.set_title("a sine wave")

# t = np.arange(0.0, 1.0, 0.01)
# s = np.sin(2 * np.pi * t)
# (line,) = ax1.plot(t, s, color="blue", lw=2)

# # Fixing random state for reproducibility
# np.random.seed(19680801)

# ax2 = fig.add_axes([0.15, 0.1, 0.7, 0.3])
# n, bins, patches = ax2.hist(
#     np.random.randn(1000), 50, facecolor="yellow", edgecolor="yellow"
# )
# ax2.set_xlabel("time (s)")

# # Converting Figure to an image:
# canvas = FigureCanvas(fig)
# canvas.draw()
# img = Image.fromarray(np.asarray(canvas.buffer_rgba()))

# pdf = FPDF()
# pdf.add_page()
# pdf.image(img, w=pdf.epw)  # Make the image full width
# pdf.output("matplotlib.pdf")