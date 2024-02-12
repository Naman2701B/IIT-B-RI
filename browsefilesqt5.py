import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import io
from test import timeTableData, routeAltitudeData


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.stringlineplot.setEnabled(False)
        self.velocity.setEnabled(False)
        self.stringlineplot.clicked.connect(self.stringLinePlotClick)
        self.browse.clicked.connect(self.browsefiles)
        self.plotbtn.clicked.connect(self.plot)
        self.subplotbtn.clicked.connect(self.subplot)
        self.mergeplotbtn.clicked.connect(self.mergeplot)
        self.selectbtn.clicked.connect(self.showCheckBoxOpt)
        self.options.currentTextChanged.connect(self.current_text_changed)
        self.Tractiveeffort.setEnabled(False)
        self.Reactivepower.setEnabled(False)
        self.Activepower.setEnabled(False)
        self.Voltage.setEnabled(False)
        self.Brakingeffort.setEnabled(False)
        self.Current.setEnabled(False)
        self.Trainplots.setEnabled(False)
        self.Stringline.setEnabled(False)
        self.Conductorconfig.setEnabled(False)
        self.Routealtitude.setEnabled(False)
        self.Timetable.setEnabled(False)
        self.Trainplots1.setEnabled(False)
        self.Substationplots.setEnabled(False)
        self.Time_radio.setEnabled(False)
        self.Distance_radio.setEnabled(False)
        self.plotbtn.setEnabled(False)
        self.subplotbtn.setEnabled(False)
        self.mergeplotbtn.setEnabled(False)
        self.file_paths = []
        self.checkedButtons = []
        self.file_names = []
        self.folder_paths = []
        self.final_input_directories = []
        self.trains = []

    def browsefiles(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Choose a Folder', '')
        if (fname):
            self.folder_paths = self.findFolders(fname)
            self.options.clear()
            self.addOpt()
        self.filename.setText(fname)

    def addOpt(self):
        for path in self.folder_paths:
            dispName = os.path.basename(path).split('/')[-1]
            self.options.addItem(dispName)

    def showCheckBoxOpt(self):
        self.file_names.clear()
        self.Tractiveeffort.setEnabled(True)
        self.Reactivepower.setEnabled(True)
        self.Activepower.setEnabled(True)
        self.Voltage.setEnabled(True)
        self.Brakingeffort.setEnabled(True)
        self.Current.setEnabled(True)
        self.Trainplots.setEnabled(True)
        self.Stringline.setEnabled(True)
        self.Conductorconfig.setEnabled(True)
        self.Routealtitude.setEnabled(True)
        self.Timetable.setEnabled(True)
        self.Trainplots1.setEnabled(True)
        self.Substationplots.setEnabled(True)
        self.Time_radio.setEnabled(True)
        self.Distance_radio.setEnabled(True)
        self.stringlineplot.setEnabled(True)
        self.plotbtn.setEnabled(True)
        self.subplotbtn.setEnabled(True)
        self.mergeplotbtn.setEnabled(True)
        output_file_results = []
        input_directory_results = []
        for path in self.folder_paths:
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    for root, dirs, files in os.walk(dir_path):
                        for file in files:
                            if "output" in file.lower():
                                output_file_results = (os.path.abspath(
                                    os.path.join(dir_path, file)))
                break
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    if "output" in dir.lower():
                        output_directory_results = (
                            os.path.abspath(os.path.join(root, dir)))
                    if "input" in dir.lower():
                        input_directory_results.append(
                            os.path.abspath(os.path.join(root, dir)))
            for directories in input_directory_results:
                for root, dirs, files in os.walk(directories):
                    if (len(files) > 0):
                        self.final_input_directories.append(directories)
        # self.unselected.addItem(data[j]["trainnumber"])

    # def on_move(event):
    # if event.inaxes:
    #     print(f'data coords {event.xdata} {event.ydata},',
    #           f'pixel coords {event.x} {event.y}')

    def current_text_changed(self, text):
        return text

    def plot(self):
        print()
        for i in range(0, len(self.checkedButtons)):
            if (self.file_paths[self.checkedButtons[i]].endswith(".xlsx")):
                file = pd.read_excel(
                    self.file_paths[self.checkedButtons[i]], header=None)
                X_axis = file[0]
                Y_axis = file[1]
            else:
                file = io.loadmat(
                    file_name=self.file_paths[self.checkedButtons[i]])
                X_axis = file["a"]
                Y_axis = file["b"]
            plt.figure(i)
            plt.plot(X_axis, Y_axis, label=self.checkboxes.button(
                self.checkedButtons[i]).text())
            plt.legend()
            plt.show()

    def subplot(self):
        figure, axis = plt.subplots(len(self.checkedButtons))
        for i in range(0, len(self.checkedButtons)):
            if (self.file_paths[self.checkedButtons[i]]).endswith(".xlsx"):
                file = pd.read_excel(
                    self.file_paths[self.checkedButtons[i]], header=None)
                X_axis = file[0]
                Y_axis = file[1]
            else:
                file = io.loadmat(
                    file_name=self.file_paths[self.checkedButtons[i]])
                X_axis = file["a"]
                Y_axis = file["b"]
            axis[i].plot(X_axis, Y_axis,
                         label=self.checkboxes.button(self.checkedButtons[i]).text())
            axis[i].legend()
        plt.show()

    def mergeplot(self):
        Y_axis = []
        for i in range(0, len(self.checkedButtons)):
            if (self.file_paths[self.checkedButtons[i]].endswith(".xlsx")):
                file = pd.read_excel(
                    self.file_paths[self.checkedButtons[i]], header=None)
                X_axis = file[0]
                Y_axis.append(file[1])
            elif (self.file_paths[self.checkedButtons[i]].endswith(".csv")):
                file = pd.read_csv(
                    self.file_paths[self.checkedButtons[i]], header=None)
                X_axis = file[0]
                Y_axis.append(file[1])
            else:
                file = io.loadmat(
                    file_name=self.file_paths[self.checkedButtons[i]])
                X_axis = file["a"]
                Y_axis.append(file["b"])
            plt.plot(X_axis, Y_axis[i], label=self.checkboxes.button(
                self.checkedButtons[i]).text())
            plt.legend()
        plt.show()

    def getStringLineData(self):
        for i in range(0, len(self.final_input_directories)):
            data = timeTableData(self.final_input_directories[i])
            for j in range(0, len(data["calculativeData"])):
                self.trains.append(data["calculativeData"][j]["trainnumber"])
            for j in range(0, len(data["calculativeData"])):
                x_axis = []
                y_axis = []
                for z in range(0, len(data["calculativeData"][j]["timeFromStarting"])):
                    x_axis.append(
                        int(data["calculativeData"][j]['distanceFromStarting'][z]))
                    y_axis.append(
                        (int(data["calculativeData"][j]['timeFromStartingInMins'][z])))
                plt.plot(x_axis, y_axis,
                         label=data["calculativeData"][j]["trainnumber"])
                plt.gca().invert_yaxis()
            plt.yticks(data["plottingData"][1], data["plottingData"][0])
            plt.legend(loc='center left', bbox_to_anchor=(1, 1))
            plt.xlabel("Distance from Starting Point")
            plt.ylabel("Time")
            plt.title("String Line Diagram")
            plt.get_current_fig_manager().resize(950, 500)
            # binding_id = plt.connect('motion_notify_event', on_move)
            plt.show()

    def stringLinePlotClick(self):
        if (self.Stringline.isChecked()):
            plt.figure()
            self.getStringLineData()
        if (self.Routealtitude.isChecked()):
            plt.figure()
            for i in range(0, len(self.final_input_directories)):
                routeAltitudeData(self.final_input_directories[i])

    def findFolders(self, start_dir):
        directory_results = []
        for root, dirs, files in os.walk(start_dir):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if "output" in dir.lower():
                    directory_results.append(os.path.abspath(
                        os.path.join(dir_path, os.pardir)))
                break
        return directory_results

    def findFiles(self, start_dir):
        file_extension = [".xlsx", ".mat", ".csv"]
        file_results_path = []
        for ext in file_extension:
            for root, dirs, files in os.walk(start_dir):
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        file_results_path.append(file_path)
        return file_results_path


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1129)
widget.setFixedHeight(976)
widget.show()
sys.exit(app.exec_())
