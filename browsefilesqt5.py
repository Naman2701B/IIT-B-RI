import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import io
from utility import timeTableData, routeAltitudeData, VoltageData, CurrentData
from utility import ReactivePowerData, ActivePowerData, BrakingEffortData, TractiveEffortData, VelocityData
from utility import loadFlowAnalysis
# from utility import loadFlowAnalysis, powerQualityAnalysis, shortCircuitAnalysis
import mplcursors


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.stringlineplot.setEnabled(False)
        self.velocity.setEnabled(False)
        self.stringlineplot.clicked.connect(self.stringLinePlotClick)
        self.browse.clicked.connect(self.browsefiles)
        self.plotbtn.clicked.connect(self.clickEvent)
        self.subplotbtn.clicked.connect(self.clickEvent)
        self.mergeplotbtn.clicked.connect(self.clickEvent)
        self.selectbtn.clicked.connect(self.showCheckBoxOpt)
        self.pltlfa_pqa_sca.clicked.connect(self.clickEvent)
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
        self.lfaradio.setEnabled(False)
        self.pqaradio.setEnabled(False)
        self.scaradio.setEnabled(False)
        self.analysistab.setTabEnabled(1, False)
        self.analysistab.setTabEnabled(0, False)
        self.Tractiveeffort.toggled.connect(self.counter)
        self.Reactivepower.toggled.connect(self.counter)
        self.Activepower.toggled.connect(self.counter)
        self.Voltage.toggled.connect(self.counter)
        self.Brakingeffort.toggled.connect(self.counter)
        self.Current.toggled.connect(self.counter)
        self.velocity.toggled.connect(self.counter)
        self.Trainplots.toggled.connect(self.MTMM)
        self.lfaradio.clicked.connect(self.lfabrowse)
        self.lfaselect.clicked.connect(self.lfaconnect)
        self.pqa_sca_select.clicked.connect(self.pqaconnect)
        self.pqaradio.clicked.connect(self.lfabrowse)
        self.scaradio.clicked.connect(self.lfabrowse)
        self.lfaoptions.setEnabled(False)
        self.lfaselect.setEnabled(False)
        self.pqa_sca_select.setEnabled(False)
        self.pqa_scaoptions.setEnabled(False)
        self.timelist.doubleClicked.connect(self.removeListOptions)
        self.time_3d.setEnabled(False)
        self.timebuttons.setExclusive(True)
        self.frequencybuttons.setExclusive(True)
        self.voltCurrentbuttons.setExclusive(True)
        self.timebuttons.addButton(self.time_2d, 0)
        self.timebuttons.addButton(self.time_3d, 1)
        self.time_2d.clicked.connect(self.check2dstatus)
        self.frequency_2d.clicked.connect(self.check2dstatus)
        self.time_3d.clicked.connect(self.check3dstatus)
        self.frequency_3d.clicked.connect(self.check3dstatus)
        self.frequencybuttons.addButton(self.frequency_2d, 0)
        self.frequencybuttons.addButton(self.frequency_3d, 1)
        self.voltCurrentbuttons.addButton(self.nodeVoltRadio, 0)
        self.voltCurrentbuttons.addButton(self.branchCurrRadio, 1)
        self.pltlfa_pqa_sca.setEnabled(False)
        self.subpltlfa_pqa_sca.setEnabled(False)
        self.mergepltlfa_pqa_sca.setEnabled(False)
        self.timeoptions.setEnabled(False)
        self.frequencyoptions.setEnabled(False)
        self.timelist.setEnabled(False)
        self.frequencyList.setEnabled(False)
        self.time_2d.setEnabled(False)
        self.time_3d.setEnabled(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        self.nodeVoltRadio.setEnabled(False)
        self.branchCurrRadio.setEnabled(False)
        self.tsnap = []
        self.lfadirectories = []
        self.pqadirectories = []
        self.scadirectories = []
        self.selectedTsnaps = []
        self.selectedTsnapValue = []
        self.file_paths = []
        self.checkedButtons = []
        self.file_names = []
        self.folder_paths = []
        self.final_input_directories = []
        self.trains = []
        self.final_output_directories = []
        self.conductors = ["Catenary Node Voltage, kV (Uptrack)", "Rail1 Voltage, kV (Uptrack)", "Rail2 Voltage, kV (Uptrack)", "Catenary Node Voltage, kV (Downtrack)", "Rail1 Voltage, kV (Downtrack)",
                           "Rail2 Voltage, kV (Downtrack)", "Feeder Node Voltage, kV (Uptrack)", "Feeder Node Voltage, kV (Downtrack)", "Protective Wire Node Voltage, kV (Uptrack)", "Protective Wire Node Voltage, kV (Downtrack)"]

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

    def check3dstatus(self):
        self.subpltlfa_pqa_sca.setEnabled(False)
        self.mergepltlfa_pqa_sca.setEnabled(False)

    def check2dstatus(self):
        self.subpltlfa_pqa_sca.setEnabled(True)
        self.mergepltlfa_pqa_sca.setEnabled(True)

    def radiostatus(self):
        self.time_2d.setEnabled(True)
        if len(self.selectedTsnaps) >= 2:
            self.time_3d.setEnabled(True)
            self.pltlfa_pqa_sca.setEnabled(True)
            self.subpltlfa_pqa_sca.setEnabled(True)
            self.mergepltlfa_pqa_sca.setEnabled(True)

        elif len(self.selectedTsnaps) == 0:
            self.time_3d.setEnabled(False)
            self.time_2d.setEnabled(False)
            self.pltlfa_pqa_sca.setEnabled(False)
            self.subpltlfa_pqa_sca.setEnabled(False)
            self.mergepltlfa_pqa_sca.setEnabled(False)

        else:
            self.time_3d.setEnabled(False)
            self.pltlfa_pqa_sca.setEnabled(True)
            self.subpltlfa_pqa_sca.setEnabled(True)
            self.mergepltlfa_pqa_sca.setEnabled(True)

    def pqabrowse(self):
        dir = os.listdir(self.lfadirectories[self.lfaoptions.currentIndex()])
        scadirectories = []
        pqadirectories = []
        for i in range(0, len(dir)):
            if "SCA" in dir[i]:
                scadirectories.append(os.path.join(
                    self.lfadirectories[self.lfaoptions.currentIndex()], dir[i]))
            if "PQA" in dir[i]:
                pqadirectories.append(os.path.join(
                    self.lfadirectories[self.lfaoptions.currentIndex()], dir[i]))
        if (self.scaradio.isChecked()):
            if len(scadirectories) == 0:
                self.pqa_sca_select.setEnabled(False)
                self.pqa_scaoptions.setEnabled(False)
            else:
                self.pqa_scaoptions.addItems(scadirectories)
                self.pqa_sca_select.setEnabled(True)
                self.pqa_scaoptions.setEnabled(True)
        if (self.pqaradio.isChecked()):
            if len(pqadirectories) == 0:
                self.pqa_sca_select.setEnabled(False)
                self.pqa_scaoptions.setEnabled(False)
            else:
                self.pqa_scaoptions.addItems(pqadirectories)
                self.pqa_sca_select.setEnabled(True)
                self.pqa_scaoptions.setEnabled(True)

    def pqaconnect(self):
        self.lfaoptions.setEnabled(True)
        self.pqa_scaoptions.setEnabled(True)
        self.frequencyoptions.setEnabled(True)
        self.frequencyList.setEnabled(True)
        self.frequency_2d.setEnabled(True)
        self.frequency_3d.setEnabled(True)
        self.timeoptions.setEnabled(False)
        self.timelist.setEnabled(False)
        self.time_2d.setEnabled(False)
        self.time_3d.setEnabled(False)

    def removeListOptions(self):
        for i in range(0, len(self.selectedTsnapValue)):
            if self.selectedTsnapValue[i] == self.timelist.currentItem().text():
                self.timeoptions.insertItem(
                    self.selectedTsnaps[i]+1, self.selectedTsnapValue[i])
                self.selectedTsnaps.remove(self.selectedTsnaps[i])
                self.selectedTsnapValue.remove(self.selectedTsnapValue[i])
                break
        self.timelist.takeItem(self.timelist.currentRow())
        self.radiostatus()

    def lfabrowse(self):
        self.time_2d.setEnabled(False)
        self.time_3d.setEnabled(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        self.timeoptions.setEnabled(False)
        self.timeoptions.clear()
        self.conductorlist.clear()
        self.selectedTsnaps.clear()
        self.selectedTsnapValue.clear()
        self.frequencyoptions.clear()
        self.frequencyoptions.setEnabled(False)
        self.conductorlist.setEnabled(False)
        self.nodeVoltRadio.setEnabled(False)
        self.branchCurrRadio.setEnabled(False)
        self.frequencyList.clear()
        self.frequencyList.setEnabled(False)
        self.lfaselect.setEnabled(True)
        self.lfaoptions.clear()
        self.lfaoptions.setEnabled(True)
        self.pqa_scaoptions.setEnabled(False)
        for i in range(0, len(self.lfadirectories)):
            dispName = os.path.basename(self.lfadirectories[i]).split('/')[-1]
            self.lfaoptions.addItem(dispName)

    def lfaconnect(self):
        if (self.pqaradio.isChecked() or self.scaradio.isChecked()):
            self.pqabrowse()
        self.timeoptions.setEnabled(True)
        self.timelist.setEnabled(True)
        self.nodeVoltRadio.setEnabled(True)
        self.branchCurrRadio.setEnabled(True)
        self.frequencyoptions.setEnabled(False)
        self.frequencyList.setEnabled(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        self.conductorlist.setEnabled(True)
        self.selectedTsnaps.clear()
        self.timeoptions.clear()
        self.timeoptions.insertItem(0, "Select Time")
        self.conductorlist.clear()
        self.conductorlist.insertItems(0, self.conductors)
        self.location = self.final_output_directories[0] + \
            "/OLFA_213159_20-07-2023_R/data_ntwrk.mat"
        file = io.loadmat(self.location)
        self.tsnap = file["tsnap"]
        self.timeoptions.insertItems(1, self.tsnap)
        self.timeoptions.activated.connect(self.activated)
        self.timeoptions.setCurrentIndex(0)

    def activated(self, index):
        for i in range(len(self.tsnap)):
            if (self.timeoptions.itemText(index) == self.tsnap[i]):
                self.selectedTsnaps.append(i)
        self.timelist.addItem(self.timeoptions.itemText(index))
        self.selectedTsnapValue.append(self.timeoptions.itemText(index))
        self.timeoptions.removeItem(index)
        self.timeoptions.setCurrentIndex(0)
        self.radiostatus()

    def LFA_PQA_SCA(self):
        res = self.final_output_directories[0]
        r1 = os.listdir(res)
        for i in range(len(r1)):
            if "LFA" in r1[i]:
                self.lfadirectories.append(os.path.join(res, r1[i]))
            if "SCA" in r1[i]:
                self.scadirectories.append(os.path.join(res, r1[i]))
            if "PQA" in r1[i]:
                self.pqadirectories.append(os.path.join(res, r1[i]))

    def showCheckBoxOpt(self):
        self.lfaradio.setEnabled(True)
        self.scaradio.setEnabled(True)
        self.pqaradio.setEnabled(True)
        self.file_names.clear()
        self.Trainplots.setEnabled(True)
        self.Stringline.setEnabled(True)
        self.Conductorconfig.setEnabled(True)
        self.Routealtitude.setEnabled(True)
        self.Timetable.setEnabled(True)
        self.Trainplots1.setEnabled(True)
        self.Substationplots.setEnabled(True)
        self.stringlineplot.setEnabled(True)
        self.Time_radio.setChecked(True)
        self.analysistab.setTabEnabled(0, True)
        output_directory_results = []

        input_directory_results = []
        for path in self.folder_paths:
            for root, dirs, files in os.walk(path):
                for dir in dirs:
                    if "output" in dir.lower():
                        output_directory_results.append(
                            os.path.abspath(os.path.join(root, dir)))
                    if "input" in dir.lower():
                        input_directory_results.append(
                            os.path.abspath(os.path.join(root, dir)))
            for directories in input_directory_results:
                for root, dirs, files in os.walk(directories):
                    if (len(files) > 0):
                        self.final_input_directories.append(directories)
            for directories in output_directory_results:
                for root, dirs, files in os.walk(directories):
                    if (len(files) > 0):
                        self.final_output_directories.append(directories)
            self.LFA_PQA_SCA()

    def MTMM(self):
        self.MTMMList.clear()
        self.trains = []
        if (self.Trainplots.isChecked()):
            self.getTrainNumberData()
            self.MTMMList.addItems(self.trains)
            self.MTMMList.setCurrentItem(self.MTMMList.item(0))
            self.velocity.setEnabled(True)
            self.Tractiveeffort.setEnabled(True)
            self.Reactivepower.setEnabled(True)
            self.Activepower.setEnabled(True)
            self.Voltage.setEnabled(False)
            self.Brakingeffort.setEnabled(True)
            self.Current.setEnabled(False)
            self.Time_radio.setEnabled(True)
            self.Distance_radio.setEnabled(True)
            self.Time_radio.setChecked(True)
        else:
            self.Tractiveeffort.setEnabled(False)
            self.Reactivepower.setEnabled(False)
            self.Activepower.setEnabled(False)
            self.Voltage.setEnabled(False)
            self.Brakingeffort.setEnabled(False)
            self.Current.setEnabled(False)
            self.Time_radio.setEnabled(False)
            self.Distance_radio.setEnabled(False)
            self.velocity.setEnabled(False)

    def getTrainNumberData(self):
        for i in range(0, len(self.final_input_directories)):
            data = timeTableData(self.final_input_directories[i])
            for j in range(0, len(data["calculativeData"])):
                self.trains.append(data["calculativeData"][j]["trainnumber"])

    def current_text_changed(self, text):
        return text

    def counter(self):
        sender = self.sender()
        if (sender in self.checkedButtons):
            self.checkedButtons.remove(sender)
        else:
            self.checkedButtons.append(sender)
        if (len(self.checkedButtons) > 0):
            self.plotbtn.setEnabled(True)
            self.subplotbtn.setEnabled(True)
        else:
            self.plotbtn.setEnabled(False)
            self.subplotbtn.setEnabled(False)
            self.mergeplotbtn.setEnabled(False)
        if (len(self.checkedButtons) == 2):
            self.mergeplotbtn.setEnabled(True)
        else:
            self.mergeplotbtn.setEnabled(False)

    def clickEvent(self):
        self.trains = []
        self.getTrainNumberData()
        X_axis = []
        Y_axis = []
        keys = []
        if (self.Voltage.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = VoltageData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = VoltageData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Voltage")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.Current.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = CurrentData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = CurrentData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Current")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.Activepower.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = ActivePowerData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = ActivePowerData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Active Power")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.Reactivepower.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = ReactivePowerData(self.final_input_directories[0],
                                             self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = ReactivePowerData(self.final_input_directories[0],
                                             self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Reactive Power")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.Tractiveeffort.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = TractiveEffortData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = TractiveEffortData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Tractive Effort")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.Brakingeffort.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = BrakingEffortData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = BrakingEffortData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Braking Effort")
            X_axis.append(x)
            Y_axis.append(y)
        if (self.velocity.isChecked()):
            for i in range(0, len(self.final_output_directories)):
                if (self.Time_radio.isChecked()):
                    x, y = VelocityData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 1)
                else:
                    x, y = VelocityData(
                        self.final_output_directories[i], self.MTMMList.currentItem().text(), 0)
            keys.append("Velocity")
            X_axis.append(x)
            Y_axis.append(y)
        sender = self.sender()
        if (sender == self.plotbtn):
            self.plot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        elif (sender == self.subplotbtn):
            self.subplot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        elif (sender == self.mergeplotbtn):
            self.mergeplot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        if (sender == self.pltlfa_pqa_sca):
            self.LFA()
        if (sender == self.subpltlfa_pqa_sca):
            self.LFA()
        if (sender == self.mergepltlfa_pqa_sca):
            self.LFA()

    def plot(self, X_axis, Y_axis, keys, timeflag):
        for i in range(0, len(Y_axis)):
            for j in range(0, len(Y_axis[i])):
                plt.figure()
                if (timeflag == True):
                    plt.xlabel("Time in Minutes")
                else:
                    plt.xlabel("Distance in KM")
                plt.title(keys[i])
                plt.plot(X_axis[i][j], Y_axis[i][j],
                         label=str(self.MTMMList.currentItem().text()))
                plt.legend()
                plt.ylabel(keys[i])
                cursor = mplcursors.cursor(hover=True)
                plt.grid(alpha=0.3)
                plt.show()

    def subplot(self, X_axis, Y_axis, keys, timeflag):
        figure, axis = plt.subplots(len(Y_axis))
        for i in range(0, len(Y_axis)):
            if (timeflag == True):
                plt.xlabel("Time in Minutes")
            else:
                plt.xlabel("Distance in KM")
            for j in range(0, len(Y_axis[i])):
                axis[i].plot(X_axis[i][j], Y_axis[i][j],
                             label=str(self.MTMMList.currentItem().text()))
                axis[i].set_ylabel(keys[i])
                axis[i].legend()
                # axis[i].set_ylabel[keys[i]]
        cursor = mplcursors.cursor(hover=True)
        plt.grid(alpha=0.3)
        plt.show()

    def mergeplot(self, X_axis, Y_axis, keys, timeflag):
        fig, ax1 = plt.subplots()
        if (timeflag == True):
            plt.xlabel("Time in Minutes")
        else:
            plt.xlabel("Distance in KM")
        ax2 = ax1.twinx()
        ax1.plot(X_axis[0][0], Y_axis[0][0], label=(str(
            keys[0])+" "+str(self.MTMMList.currentItem().text())), color='tab:cyan')
        ax1.set_ylabel(str(keys[0]))
        ax2.plot(X_axis[0][0], Y_axis[1][0], label=(str(
            keys[1])+" "+str(self.MTMMList.currentItem().text())), color='tab:orange')
        ax2.set_ylabel(str(keys[1]))
        plt.legend()
        plt.grid(alpha=0.3)
        cursor = mplcursors.cursor(hover=True)
        plt.show()

    def LFA(self):
        radioflag = 0
        if self.branchCurrRadio.isChecked():
            radioflag = 1
        if self.time_3d.isChecked():
            loadFlowAnalysis(
                self.lfadirectories[self.lfaoptions.currentIndex()], self.selectedTsnaps, (self.conductorlist.currentRow()+10), radioflag, 1)
        else:
            X, Y = loadFlowAnalysis(self.lfadirectories[self.lfaoptions.currentIndex(
            )], self.selectedTsnaps, (self.conductorlist.currentRow()+10), radioflag, 0)
            for i in range(0, len(Y)):
                plt.plot(X[i], Y[i])
                plt.xlabel("Distance in KM")
                if radioflag == 1:
                    plt.ylabel("Branch Current")
                else:
                    plt.ylabel("Node Voltage in kV")
                plt.show()

    def getStringLineData(self):
        for i in range(0, len(self.final_input_directories)):
            data = timeTableData(self.final_input_directories[i])
            x_axis = []
            y_axis = []
            start = 0
            end = 0
            output_data = pd.read_csv(
                self.final_output_directories[i]+"/TrainModuleOutput.csv")
            for j in range(0, len(data["calculativeData"])):
                self.trains.append(data["calculativeData"][j]["trainnumber"])
            for j in range(0, len(data["calculativeData"])):
                if (int(output_data["Up/Downtrack_"+str(self.trains[j])+"_0"][1]) == 0):
                    partstr = "Uptrack"
                else:
                    partstr = "Downtrack"
                for k in range(0, len(output_data['Distance_'+partstr+'_'+str(self.trains[j])+'_0'])):
                    if (float(output_data["Velocity_"+partstr+"_"+str(self.trains[j])+"_0"][k]) > 0.0):
                        start = k
                        break
                for k in range(0, len(output_data['Distance_'+partstr+'_'+str(self.trains[j])+'_0'])):
                    if (float(output_data["Velocity_"+partstr+"_"+str(self.trains[j])+"_0"][k]) == 0.0):
                        if (float(output_data["Distance_"+partstr+"_"+str(self.trains[j])+"_0"][k]) == float(data["calculativeData"][j]["endDistance"])):
                            end = k
                            break
                x_axis.append(
                    (output_data['Distance_'+partstr+'_'+str(self.trains[j])+'_0'][start:end]))
                y_axis.append(
                    (output_data['Time_'+partstr+'_'+str(self.trains[j])+'_0'][start:end])*60)
                plt.plot(x_axis[j], y_axis[j],
                         label=self.trains[j])
            plt.gca().invert_yaxis()
            plt.yticks(data["plottingData"][1], data["plottingData"][0])
            plt.xticks(data["plottingData"][3], data["plottingData"][2])
            plt.xlim(left=0, right=max(data["plottingData"][3]))
            plt.legend(loc='center left', bbox_to_anchor=(1, 1))
            plt.xlabel("Distance from Starting Point",
                       fontsize=15, fontweight='bold')
            plt.ylabel("Time", fontsize=15, fontweight='bold')
            plt.title("String Line Diagram", fontsize=15, fontweight='bold')
            plt.get_current_fig_manager().resize(950, 500)
            plt.grid(alpha=0.3)
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
