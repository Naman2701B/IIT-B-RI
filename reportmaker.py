from fpdf import FPDF
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image
import os
import pandas as pd
import matplotlib.pyplot as plt

outputFolder = "C:/Users/ashok/Desktop/IIT RESEARCH/Task 4/eTPSS/Traction_Power_Supply_System_Modules/HSRIC_00_Projects/Case_2_P0.25B/Case_2_P0.25B_Output"
def startReport(outputFolder):
    file = pd.read_csv(outputFolder+"/SubstationResults.csv")
    fig,ax = plt.subplots()
    pie1 = float(file["Supplied energy without Transformer losses SPT1(kWh)"])
    pie2 = float(abs(file["Regenerative energy without Transformer losses SPT1(kWh)"]))
    data_labels = ["Supplied energy without losses SPT1(kWh)","Regenerative energy without losses SPT1(kWh)"]
    data = np.array([pie1,pie2])
    ax.pie(data)
    ax.legend(labels = data_labels, bbox_to_anchor=(0.4,1), loc="center")
    plt.show()
    canvas = FigureCanvas(fig)
    canvas.draw()
    img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
    pdf = FPDF()
    pdf.add_page()
    pdf.image(img,w=pdf.epw/2, x=120, y=10) 
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
