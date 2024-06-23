
"""ETPSSModule.py

This module is part of the railway simulation software and provides a graphical user interface (GUI) for interacting with various data analysis functionalities. 
It uses PyQt5 for the GUI components and includes several functions for loading and processing data, as well as generating plots and reports.

Imports:
    - sys: Provides access to some variables used or maintained by the Python interpreter.
    - PyQt5: Used for creating the graphical user interface.
        - QtWidgets, QtCore, QtGui: Core classes for GUI components.
        - QDialog, QApplication, QFileDialog, QMessageBox, QPushButton: Specific classes for dialog, application, file dialog, message box, and push button.
        - QDesktopServices: Provides methods for accessing desktop services.
        - QUrl: Provides methods for handling URLs.
    - matplotlib.pyplot: Used for creating static, animated, and interactive visualizations.
    - pandas: Used for data manipulation and analysis.
    - numpy: Used for numerical operations.
    - os: Provides a way of using operating system dependent functionality.
    - scipy.io: Used for reading and writing MATLAB files.
    - Dependencies: Contains various data processing functions.
        - timeTableData, routeAltitudeData, VoltageData, CurrentData, ReactivePowerData, ActivePowerData, BrakingEffortData, TractiveEffortData, VelocityData
        - loadFlowAnalysis, ShortCircuitAnalysis, powerQualityAnalysis, ShortCircuitAnalysis_IA
    - TimeTableOutput: Contains the function to export timetable data to Excel.
    - mplcursors: Used for interactive data cursors in matplotlib.
    - ReportGenerator: Contains the function to start the report generation.
    - TemperatureAnalysis: Contains functions for temperature analysis plots.
        - D3Plot_TA_LFA, D3Plot_TA_SCA
    - UIFile: Contains the user interface definition.

Classes:
    - MainWindow: Inherits from QDialog and Ui_Dialog, handles the main operations and interactions with the GUI.

Functions:
    - __init__(self, parent=None): Initializes the main window.
    - loadData(self): Loads the required data for analysis.
    - showMessage(self, title, message): Displays a message box with a given title and message.
    - saveFileDialog(self): Opens a file dialog to select a file for saving.
    - openFileDialog(self): Opens a file dialog to select a file for opening.
    - loadDataForAnalysis(self): Loads data for analysis.
    - plotGraph(self): Plots the required graphs based on user selection.
    - generateReport(self): Generates a report based on the loaded data.
    - timetablePlotClick(self): Handles the event when the timetable plot button is clicked.
    - stringLinePlotClick(self): Handles the event when the string line plot button is clicked.
    - findFolders(self, start_dir): Finds and returns a list of directories containing output files.
    - findFiles(self, start_dir): Finds and returns a list of files with specified extensions.

Usage:
    This module is designed to be used as part of a larger railway simulation software. 
    It provides a user-friendly GUI for interacting with the simulation data, performing analysis, and generating reports.
"""
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import io
from Dependencies import timeTableData, routeAltitudeData, VoltageData, CurrentData
from Dependencies import ReactivePowerData, ActivePowerData, BrakingEffortData, TractiveEffortData, VelocityData
from Dependencies import loadFlowAnalysis, ShortCircuitAnalysis, powerQualityAnalysis, ShortCircuitAnalysis_IA
from TimeTableOutput import timeTableExcel
import mplcursors
from ReportGenerator import startReport
from TemperatureAnalysis import D3Plot_TA_LFA, D3Plot_TA_SCA
from UIFile import Ui_Dialog
# from PyQt5.uic import loadUi
from datetime import timedelta

class MainWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # loadUi("gui.ui", self)
        flagsWindow = QtCore.Qt.WindowFlags()
        self.setWindowFlags(flagsWindow)
        self.timetable_trainstat.setHidden(True)
        self.trainStat.setEnabled(False)
        self.trainStat.clicked.connect(self.reportTrigger)
        self.selectAllTime.setEnabled(False)
        self.selectAllFrequency.setEnabled(False)
        self.reportGenerate.setEnabled(False)
        self.stringlineplot.setEnabled(False)
        self.velocity.setEnabled(False)
        self.selectbtn.setEnabled(False)
        self.options.setEnabled(False)
        self.stringlineplot.clicked.connect(self.stringLinePlotClick)
        self.browse.clicked.connect(self.browsefiles)
        self.plotbtn.clicked.connect(self.clickEvent)
        self.subplotbtn.clicked.connect(self.clickEvent)
        self.mergeplotbtn.clicked.connect(self.clickEvent)
        self.selectbtn.clicked.connect(self.resetState)
        self.pltlfa_pqa_sca.clicked.connect(self.LFA)
        self.subpltlfa_pqa_sca.clicked.connect(self.LFA)
        self.mergepltlfa_pqa_sca.clicked.connect(self.LFA)
        self.options.currentTextChanged.connect(self.current_text_changed)
        self.reportGenerate.clicked.connect(self.reportTrigger)
        self.Tractiveeffort.setEnabled(False)
        self.Reactivepower.setEnabled(False)
        self.Activepower.setEnabled(False)
        self.Voltage.setEnabled(False)
        self.Brakingeffort.setEnabled(False)
        self.Current.setEnabled(False)
        self.Trainplots.setEnabled(False)
        self.Stringline.setEnabled(False)
        self.Routealtitude.setEnabled(False)
        self.showTimeTable.setEnabled(False)
        self.timetableflag= False
        self.trainstatflag= False
        self.showTimeTable.clicked.connect(self.showdialog)
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
        self.analysistab.setTabEnabled(1, True)
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
        self.pqa_sca_select.clicked.connect(self.pqa_sca_connect)
        self.pqaradio.clicked.connect(self.lfabrowse)
        self.scaradio.clicked.connect(self.lfabrowse)
        self.lfaoptions.setEnabled(False)
        self.lfaselect.setEnabled(False)
        self.pqa_sca_select.setEnabled(False)
        self.pqa_scaoptions.setEnabled(False)
        self.timelist.doubleClicked.connect(self.removeListOptions)
        self.frequencyList.doubleClicked.connect(self.removeListOptions)
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
        self.selectAllTime.clicked.connect(self.selectAll)
        self.selectAllFrequency.clicked.connect(self.selectAll)
        self.frequencyList.setEnabled(False)
        self.time_2d.setEnabled(False)
        self.time_3d.setEnabled(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        self.nodeVoltRadio.setEnabled(False)
        self.branchCurrRadio.setEnabled(False)
        self.IARadioOptions.setExclusive(False)
        self.IARadioOptions.addButton(self.IAButton, 0)
        self.IARadioOptions.addButton(self.TAButton, 1)
        self.IARadioOptions.buttonClicked.connect(self.IACheck)
        self.lfaradiooptions.addButton(self.lfaradio, 0)
        self.lfaradiooptions.addButton(self.scaradio, 1)
        self.lfaradiooptions.addButton(self.pqaradio, 2)
        self.ia_options.setHidden(True)
        self.ia_options.setEnabled(False)
        self.ia_select.setHidden(True)
        self.ia_select.setEnabled(False)
        self.tsnap = []
        self.lfadirectories = []
        self.pqadirectories = []
        self.scadirectories = []
        self.selectedTsnaps = []
        self.selectedTsnapValue = []
        self.selectedFrequency = []
        self.selectedFrequencyValue = []
        self.file_paths = []
        self.checkedButtons = []
        self.file_names = []
        self.folder_paths = []
        self.final_input_directories = []
        self.trains = []
        self.final_output_directories = []
        self.iadirectories = []
        self.tadirectories = []
        self.conductors = ["Catenary (Uptrack)", "Rail1 (Uptrack)", "Rail2 (Uptrack)", "Catenary (Downtrack)",
                           "Rail1 (Downtrack)",
                           "Rail2 (Downtrack)", "Feeder (Uptrack)", "Feeder (Downtrack)", "Protective Wire (Uptrack)",
                           "Protective Wire (Downtrack)"]
        self.isConnectedTime = False
        self.isConnectedFrequency = False
        return

    def resetState(self):
        self.selectAllTime.setEnabled(False)
        self.selectAllFrequency.setEnabled(False)
        self.reportGenerate.setEnabled(False)
        self.stringlineplot.setEnabled(False)
        self.velocity.setEnabled(False)
        self.Tractiveeffort.setEnabled(False)
        self.Reactivepower.setEnabled(False)
        self.Activepower.setEnabled(False)
        self.Voltage.setEnabled(False)
        self.Brakingeffort.setEnabled(False)
        self.Current.setEnabled(False)
        self.Trainplots.setEnabled(False)
        self.Trainplots.setChecked(False)
        self.Stringline.setEnabled(False)
        self.Stringline.setChecked(False)
        self.Routealtitude.setEnabled(False)
        self.showTimeTable.setEnabled(False)
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
        self.analysistab.setTabEnabled(1, True)
        self.analysistab.setTabEnabled(0, False)
        self.lfaoptions.setEnabled(False)
        self.lfaselect.setEnabled(False)
        self.pqa_sca_select.setEnabled(False)
        self.pqa_scaoptions.setEnabled(False)
        self.time_3d.setEnabled(False)
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
        self.timebuttons.setExclusive(True)
        self.frequencybuttons.setExclusive(True)
        self.voltCurrentbuttons.setExclusive(True)
        self.tsnap = []
        self.lfadirectories = []
        self.pqadirectories = []
        self.scadirectories = []
        self.selectedTsnaps = []
        self.selectedTsnapValue = []
        self.selectedFrequency = []
        self.selectedFrequencyValue = []
        self.checkedButtons = []
        self.final_input_directories = []
        self.trains = []
        self.final_output_directories = []
        self.iadirectories = []
        self.tadirectories = []
        self.conductors = ["Catenary (Uptrack)", "Rail1 (Uptrack)", "Rail2 (Uptrack)", "Catenary (Downtrack)",
                           "Rail1 (Downtrack)",
                           "Rail2 (Downtrack)", "Feeder (Uptrack)", "Feeder (Downtrack)", "Protective Wire (Uptrack)",
                           "Protective Wire (Downtrack)"]
        self.showCheckBoxOpt()
        return

    def IACheck(self, radiobutton):
        """Handles the selection of an IA (Insulation Assessment) option from a set of radio buttons.
    
         This function ensures that only the selected radio button remains checked, updates UI elements
         visibility based on the selection, and modifies internal variables and texts based on whether the
         IA option is selected or not.
    
         Parameters:
         radiobutton (QRadioButton): The radio button that was selected.

        Returns:
        None"""
        
        for button in self.IARadioOptions.buttons():
            if button is not radiobutton:
                button.setChecked(False)
        self.ia_options.setHidden(False)
        self.ia_select.setHidden(False)
        if (not self.IAButton.isChecked()):
            self.ia_options.setHidden(True)
            self.ia_select.setHidden(True)
            self.nodeVoltRadio.setText("Node Voltage")
            self.branchCurrRadio.setText("Branch Current")
            self.conductors = ["Catenary (Uptrack)", "Rail1 (Uptrack)", "Rail2 (Uptrack)", "Catenary (Downtrack)",
                               "Rail1 (Downtrack)",
                               "Rail2 (Downtrack)", "Feeder (Uptrack)", "Feeder (Downtrack)",
                               "Protective Wire (Uptrack)", "Protective Wire (Downtrack)"]
        if (self.IAButton.isChecked()):
            for i in range(len(self.final_input_directories)):
                if "IA" in self.final_input_directories[i]:
                    file = pd.read_csv(self.final_input_directories[i] + "/Cable_Data.csv")
                    self.cablelist = file["name "].to_list()
                    self.nodeVoltRadio.setText("Cable Voltage")
                    self.branchCurrRadio.setText("Cable Current")
                    self.conductors = self.cablelist
        return

    def open_pdf(self):
        """Opens a PDF report using the default PDF viewer on the user's system.
    
        This function constructs the file path of the PDF report from the specified directory and report name,
        then uses QDesktopServices to open the PDF file. It also closes any message dialog that may be open.
    
        Parameters:
        None
    
        Returns:
        None"""
        
        pdf_path = self.final_output_directories[0] + "/" + self.reportName + ".pdf"
        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_path))
        self.msg.close()
        return

    def reportTrigger(self):
        """Triggers the report generation or toggles the display of train statistics based on the sender.

        This function checks which UI element triggered the event and either shows/hides train statistics 
        or generates a PDF report. If the train statistics button is toggled, it updates the table with relevant data.
        If another button is clicked, it generates a PDF report and displays a notification with an option to open the PDF.

        Parameters:
        None

        Returns:
        None"""
        
        sender = self.sender()
        if(sender == self.trainStat):
            self.trainstatflag = not (self.trainstatflag)
            if(self.trainstatflag):
                data = timeTableData(self.final_input_directories[0])
                file = pd.read_csv(self.final_output_directories[0]+"/TrainResults.csv",header=None)
                self.timetable_trainstat.setColumnCount(len(file[0]))
                self.timetable_trainstat.setRowCount(6)
                self.timetable_trainstat.setHorizontalHeaderLabels(file[0])
                self.timetable_trainstat.setColumnWidth(0,250)
                self.timetable_trainstat.setHidden(False)
                for j in range(len(data["calculativeData"])):
                    item = QtWidgets.QTableWidgetItem("Start Time (HH:MM)")
                    self.timetable_trainstat.setItem(0,0,item)
                    item = QtWidgets.QTableWidgetItem(data["calculativeData"][j]["startTime"])
                    self.timetable_trainstat.setItem(0,j+1,item)
                for i in range(1,len(file[0])):
                    item = QtWidgets.QTableWidgetItem("Travel Time (HH:MM:SS)")
                    self.timetable_trainstat.setItem(4,0,item)
                    temp = int(file[1][i])
                    h = temp // 3600
                    m = (temp % 3600) // 60
                    s = temp % 60
                    item = QtWidgets.QTableWidgetItem(str(timedelta(hours=h, minutes=m, seconds=s)))
                    self.timetable_trainstat.setItem(4,i,item)
                    item = QtWidgets.QTableWidgetItem("End Time (HH:MM:SS)")
                    self.timetable_trainstat.setItem(5,0,item)
                    temp1 = data["calculativeData"][i-1]["startTime"].split(":")
                    hours = int(temp1[0])
                    minutes = int(temp1[1])
                    item = QtWidgets.QTableWidgetItem(str(timedelta(hours=hours, minutes=minutes)+timedelta(hours= h, minutes=m,seconds=s)))
                    self.timetable_trainstat.setItem(5,i,item)
                for i in range(1, len(file[0])):
                    item = QtWidgets.QTableWidgetItem("Maximum Voltage (kV)")
                    self.timetable_trainstat.setItem(1,0,item)
                    item = QtWidgets.QTableWidgetItem(str(round(float(file[4][i])/1000,2)))
                    self.timetable_trainstat.setItem(1,i,item)
                    item = QtWidgets.QTableWidgetItem("Minimum Voltage (kV)")
                    self.timetable_trainstat.setItem(2,0,item)
                    item = QtWidgets.QTableWidgetItem(str(round(float(file[3][i])/1000,2)))
                    self.timetable_trainstat.setItem(2,i,item)
                    item = QtWidgets.QTableWidgetItem("Mean Useful Voltage (kV)")
                    self.timetable_trainstat.setItem(3,0,item)
                    item = QtWidgets.QTableWidgetItem(str(round(float(file[2][i])/1000,2)))
                    self.timetable_trainstat.setItem(3,i,item)
                self.showTimeTable.setText("Show Time Table")
                self.trainStat.setText("Hide Train Statistics")
                self.timetableflag = False
            else:
                self.trainStat.setText("Show Train Statistics")
                self.timetable_trainstat.setHidden(True)
        else:
            data = timeTableData(self.final_input_directories[0])
            self.reportName = startReport(self.final_output_directories[0], data["calculativeData"])
            self.msg = QMessageBox()
            self.msg.setWindowTitle("PDF Notification")
            button = QPushButton("Open PDF", self.msg)
            button.setGeometry(15, 60, 110, 30)
            button.clicked.connect(self.open_pdf)
            self.msg.setText("PDF Successfully Created.")
            self.msg.exec()
        return

    def browsefiles(self):
        """Opens a file dialog for the user to select a directory and processes the selected directory.

        This function opens a QFileDialog to allow the user to select a folder. If a folder is selected,
        it finds subfolders within the selected directory, updates the options in the UI, and displays
        the selected folder path.

        Parameters:
        None

        Returns:
        None"""
        
        fname = QFileDialog.getExistingDirectory(
            self, 'Choose a Folder', '')
        if (fname):
            self.folder_paths = self.findFolders(fname)
            self.options.clear()
            self.addOpt()
        self.filename.setText(fname)
        return

    def addOpt(self):
        """Adds options to the UI based on the found folder paths and enables relevant UI elements.

        This function enables the options UI element and the select button. It iterates over the folder
        paths and adds each folder's display name to the options list. If no folder paths are found, it
        disables the select button.

        Parameters:
        None

        Returns:
        None"""
        
        self.options.setEnabled(True)
        self.selectbtn.setEnabled(True)
        for path in self.folder_paths:
            dispName = os.path.basename(path).split('/')[-1]
            self.options.addItem(dispName)
        if(len(self.folder_paths)==0):
            self.selectbtn.setEnabled(False)
        return

    def check3dstatus(self):
        """Disables the 3D plotting options in the UI.

        This function disables specific UI elements related to 3D plotting. It is used to ensure
        that the options for 3D plotting are not available for the user.

        Parameters:
        None

        Returns:
        None"""
        
        self.subpltlfa_pqa_sca.setEnabled(False)
        self.mergepltlfa_pqa_sca.setEnabled(False)
        return

    def check2dstatus(self):
        """Enables the 2D plotting options in the UI.

        This function enables specific UI elements related to 2D plotting. It is used to ensure
        that the options for 2D plotting are available for the user.

        Parameters:
        None

        Returns:
        None"""
        
        self.subpltlfa_pqa_sca.setEnabled(True)
        self.mergepltlfa_pqa_sca.setEnabled(True)
        return

    def radiostatus(self, freq):
        """Updates the status of various UI elements based on the selected frequency and other conditions.

        This function enables or disables specific UI elements related to 2D and 3D plotting based on the
        frequency parameter and the length of selected time snapshots or selected frequencies. It also
        checks the state of the TA and IA buttons to further adjust the UI elements' statuses.

        Parameters:
        freq (int): The selected frequency (0 for time-based, non-zero for frequency-based).

        Returns:
        None"""
        if (freq == 0):
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
        else:
            self.frequency_2d.setEnabled(True)
            if len(self.selectedFrequency) >= 2:
                self.frequency_3d.setEnabled(True)
                self.pltlfa_pqa_sca.setEnabled(True)
                self.subpltlfa_pqa_sca.setEnabled(True)
                self.mergepltlfa_pqa_sca.setEnabled(True)

            elif len(self.selectedFrequency) == 0:
                self.frequency_3d.setEnabled(False)
                self.frequency_2d.setEnabled(False)
                self.pltlfa_pqa_sca.setEnabled(False)
                self.subpltlfa_pqa_sca.setEnabled(False)
                self.mergepltlfa_pqa_sca.setEnabled(False)

            else:
                self.frequency_3d.setEnabled(False)
                self.pltlfa_pqa_sca.setEnabled(True)
                self.subpltlfa_pqa_sca.setEnabled(True)
                self.mergepltlfa_pqa_sca.setEnabled(True)
        if (self.TAButton.isChecked()):
            self.mergepltlfa_pqa_sca.setEnabled(False)
            self.subpltlfa_pqa_sca.setEnabled(False)
            self.time_2d.setEnabled(False)
            self.time_2d.setChecked(False)
            self.frequency_2d.setChecked(False)
            self.frequency_2d.setEnabled(False)
        if(self.IAButton.isChecked()):
            self.time_3d.setEnabled(False)
            self.time_3d.setChecked(False)
            self.frequency_3d.setEnabled(False)
            self.frequency_3d.setChecked(False)
        return

    def pqabrowse(self):
        """Updates the UI options for PQA and SCA directories based on the selected LFA directory.

        This function clears the current PQA/SCA options, lists the contents of the selected LFA directory,
        and updates the options for PQA and SCA directories based on the contents. It also enables or disables
        the relevant UI elements based on the availability of PQA and SCA directories.

        Parameters:
        None

        Returns:
        None"""
        
        self.pqa_scaoptions.clear()
        dir = os.listdir(self.lfadirectories[self.lfaoptions.currentIndex()])
        scadirectoriesToShow = []
        pqadirectoriesToShow = []
        self.locationDirectories = []
        for i in range(0, len(dir)):
            if "SCA" in dir[i]:
                self.locationDirectories.append(os.path.join(
                    self.lfadirectories[self.lfaoptions.currentIndex()], dir[i]))
                scadirectoriesToShow.append(dir[i])
            if "PQA" in dir[i]:
                self.locationDirectories.append(os.path.join(
                    self.lfadirectories[self.lfaoptions.currentIndex()], dir[i]))
                pqadirectoriesToShow.append(dir[i])
        if (self.scaradio.isChecked()):
            self.selectAllFrequency.setEnabled(False)
            self.selectAllTime.setEnabled(False)
            if len(scadirectoriesToShow) == 0:
                self.pqa_sca_select.setEnabled(False)
                self.pqa_scaoptions.setEnabled(False)
                self.pltlfa_pqa_sca.setEnabled(False)
            else:
                self.pqa_scaoptions.addItems(scadirectoriesToShow)
                self.pqa_sca_select.setEnabled(True)
                self.pqa_scaoptions.setEnabled(True)

        if (self.pqaradio.isChecked()):
            self.selectAllTime.setEnabled(False)
            if len(pqadirectoriesToShow) == 0:
                self.pqa_sca_select.setEnabled(False)
                self.pqa_scaoptions.setEnabled(False)
            else:
                self.pqa_scaoptions.addItems(pqadirectoriesToShow)
                self.pqa_sca_select.setEnabled(True)
                self.pqa_scaoptions.setEnabled(True)
        return

    def pqa_sca_connect(self):
        """Configures the UI elements and loads data based on the selected PQA or SCA option.

        This function updates the status of various UI elements and loads the necessary data from the selected
        directory based on whether the SCA radio button or the PQA radio button is checked. It enables or disables
        relevant options for time and frequency plotting and handles the IA options if the IA button is checked.

        Parameters:
        None

        Returns:
        None"""
        if (self.scaradio.isChecked()):
            self.timelist.clear()
            self.timeoptions.setEnabled(False)
            self.frequencyoptions.setEnabled(False)
            self.timelist.setEnabled(False)
            self.frequencyList.setEnabled(False)
            self.time_2d.setEnabled(False)
            self.time_3d.setEnabled(False)
            self.frequency_2d.setEnabled(False)
            self.frequency_3d.setEnabled(False)
            self.frequency_2d.setChecked(True)
            self.time_2d.setChecked(True)
            self.pltlfa_pqa_sca.setEnabled(True)
            file = io.loadmat(
                os.path.join(self.locationDirectories[self.pqa_scaoptions.currentIndex()], "IA_linesummary.mat"))
            self.timelist.addItem(file["timesnap"][0])
            self.frequencyList.clear()
            self.frequencyList.addItem("50")
            self.subpltlfa_pqa_sca.setEnabled(False)
            self.mergepltlfa_pqa_sca.setEnabled(False)
            dir = os.listdir(self.locationDirectories[self.pqa_scaoptions.currentIndex()])
            self.iadirectories = []
            for i in range(0, len(dir)):
                if 'IA' in dir[i] and '.' not in dir[i]:
                    self.iadirectories.append(
                        os.path.join(self.locationDirectories[self.pqa_scaoptions.currentIndex()], dir[i]))
            if self.IAButton.isChecked():
                self.ia_options.clear()
                for i in range(0, len(self.iadirectories)):
                    dispName = os.path.basename(self.iadirectories[i]).split('/')[-1]
                    self.ia_options.addItem(dispName)
                if(len(self.iadirectories)==0):
                    self.ia_options.setEnabled(False)
                    self.ia_select.setEnabled(False)
        else:
            self.selectAllFrequency.setEnabled(True)
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
            file = io.loadmat(
                os.path.join(self.locationDirectories[self.pqa_scaoptions.currentIndex()], "IA_linesummary.mat"))
            self.frequencyAvailable = []
            for i in range(len(file["fh"][0])):
                self.frequencyAvailable.append(str(file["fh"][0][i] * 50))
            self.frequencyoptions.clear()
            self.frequencyoptions.insertItems(0, self.frequencyAvailable)
            if(self.isConnectedFrequency):
                self.frequencyoptions.activated.disconnect(self.activated)
                self.isConnectedFrequency=False
            self.frequencyoptions.activated.connect(self.activated)
            self.isConnectedFrequency = True
            self.frequencyoptions.setCurrentIndex(0)
            dir = os.listdir(self.locationDirectories[self.pqa_scaoptions.currentIndex()])
            self.iadirectories = []
            for i in range(0, len(dir)):
                if 'IA' in dir[i] and '.' not in dir[i]:
                    self.iadirectories.append(
                        os.path.join(self.locationDirectories[self.pqa_scaoptions.currentIndex()], dir[i]))
            if self.IAButton.isChecked():
                self.ia_options.clear()
                for i in range(0, len(self.iadirectories)):
                    self.ia_options.setEnabled(True)
                    self.ia_select.setEnabled(True)
                    dispName = os.path.basename(self.iadirectories[i]).split('/')[-1]
                    self.ia_options.addItem(dispName)
                if(len(self.iadirectories)==0):
                    self.ia_options.setEnabled(False)
                    self.ia_select.setEnabled(False)
        return

    def selectAll(self):
        """Toggles the selection of all available time snapshots or frequencies.

        This function checks the sender to determine whether to select or deselect all time snapshots or frequencies.
        It updates the `selectedTsnaps`, `selectedTsnapValue`, `selectedFrequency`, and `selectedFrequencyValue` lists,
        and modifies the respective UI elements accordingly.

        Parameters:
        None

        Returns:
        None"""
        sender = self.sender()
        if sender == self.selectAllTime:
            if len(self.selectedTsnaps) <= 1:
                for i in range(0, (len(self.tsnap) - len(self.selectedTsnaps))):
                    self.selectedTsnaps.append(i)
                    self.timelist.addItem(self.timeoptions.itemText(0))
                    self.selectedTsnapValue.append(self.timeoptions.itemText(0))
                    self.timeoptions.removeItem(0)
                    # self.timeoptions.setCurrentIndex(0)
                self.radiostatus(0)
                self.selectAllTime.setText("Deselect All")
            else:
                for i in range(len(self.selectedTsnapValue) - 1, -1, -1):
                    self.timeoptions.insertItem(self.selectedTsnaps[i], self.selectedTsnapValue[i])
                    self.selectedTsnaps.remove(self.selectedTsnaps[i])
                    self.selectedTsnapValue.remove(self.selectedTsnapValue[i])
                self.timelist.clear()
                self.selectAllTime.setText("Select All")
                self.radiostatus(0)
        else:
            if len(self.selectedFrequency) <= 1:
                for i in range(0, (len(self.frequencyAvailable) - len(self.selectedFrequency))):
                    self.selectedFrequency.append(i)
                    self.frequencyList.addItem(self.frequencyoptions.itemText(0))
                    self.selectedFrequencyValue.append(self.frequencyoptions.itemText(0))
                    self.frequencyoptions.removeItem(0)
                    # self.timeoptions.setCurrentIndex(0)
                self.radiostatus(1)
                self.selectAllFrequency.setText("Deselect All")
            else:
                for i in range(len(self.selectedFrequencyValue) - 1, -1, -1):
                    self.frequencyoptions.insertItem(self.selectedFrequency[i], self.selectedFrequencyValue[i])
                    self.selectedFrequency.remove(self.selectedFrequency[i])
                    self.selectedFrequencyValue.remove(self.selectedFrequencyValue[i])
                self.frequencyList.clear()
                self.selectAllFrequency.setText("Select All")
                self.radiostatus(1)
        return

    def removeListOptions(self):
        """Removes the selected option from the timelist or frequencyList and updates the UI.

        This function checks the sender to determine whether the timelist or frequencyList item was removed.
        It updates the `selectedTsnaps`, `selectedTsnapValue`, `selectedFrequency`, and `selectedFrequencyValue` lists,
        and modifies the respective UI elements accordingly. It also calls the `radiostatus` function to update
        the status of related UI elements.

        Parameters:
        None

        Returns:
        None"""
        sender = self.sender()
        if (sender == self.timelist):
            for i in range(0, len(self.selectedTsnapValue)):
                if self.selectedTsnapValue[i] == self.timelist.currentItem().text():
                    self.timeoptions.insertItem(
                        self.selectedTsnaps[i], self.selectedTsnapValue[i])
                    self.selectedTsnaps.remove(self.selectedTsnaps[i])
                    self.selectedTsnapValue.remove(self.selectedTsnapValue[i])
                    break
            self.timelist.takeItem(self.timelist.currentRow())
            self.radiostatus(0)
        if (sender == self.frequencyList):
            for i in range(0, len(self.selectedFrequencyValue)):
                if self.selectedFrequencyValue[i] == self.frequencyList.currentItem().text():
                    self.frequencyoptions.insertItem(
                        self.selectedFrequency[i], self.selectedFrequencyValue[i])
                    self.selectedFrequency.remove(self.selectedFrequency[i])
                    self.selectedFrequencyValue.remove(self.selectedFrequencyValue[i])
                    break
            self.frequencyList.takeItem(self.frequencyList.currentRow())
            self.radiostatus(1)
        return

    def lfabrowse(self):
        self.selectAllTime.setEnabled(False)
        self.selectAllFrequency.setEnabled(False)
        self.time_2d.setEnabled(False)
        self.time_3d.setEnabled(False)
        self.time_2d.setChecked(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        self.timeoptions.setEnabled(False)
        self.conductorlist.clear()
        self.timelist.clear()
        self.selectedTsnaps.clear()
        self.selectedTsnapValue.clear()
        self.frequencyoptions.setEnabled(False)
        self.conductorlist.setEnabled(False)
        self.nodeVoltRadio.setEnabled(False)
        self.branchCurrRadio.setEnabled(False)
        self.frequencyList.clear()
        self.frequencyList.setEnabled(False)
        self.lfaselect.setEnabled(True)
        self.lfaoptions.clear()
        self.pqa_scaoptions.clear()
        self.lfaoptions.setEnabled(True)
        self.pqa_scaoptions.setEnabled(False)
        for i in range(0, len(self.lfadirectories)):
            dispName = os.path.basename(self.lfadirectories[i]).split('/')[-1]
            if ("_T" in dispName and self.TAButton.isChecked()):
                self.tadirectories.append(self.lfadirectories[i])
                self.lfaoptions.addItem(dispName)
            else:
                if not (self.TAButton.isChecked()): 
                    if not ("_T" in dispName):
                        self.lfaoptions.addItem(dispName)
        if (len(self.lfaoptions) == 0):
            self.lfaselect.setEnabled(False)
        return

    def lfaconnect(self):
        """Configures the UI elements and updates the LFA options based on the selected directories.

        This function disables various UI elements and clears the current selections and lists. It then updates
        the LFA options based on the available directories, enabling the selection of appropriate directories.

        Parameters:
        None

        Returns:
        None"""
        self.tsnap = np.array([])
        self.selectedTsnaps.clear()
        self.selectedTsnapValue.clear()
        self.timelist.clear()
        self.timeoptions.clear()
        self.conductorlist.clear()
        self.conductorlist.setEnabled(True)
        self.nodeVoltRadio.setEnabled(True)
        self.branchCurrRadio.setEnabled(True)
        self.time_2d.setChecked(True)
        self.selectAllFrequency.setEnabled(False)
        self.selectAllTime.setEnabled(True)
        if (self.IAButton.isChecked()):
            self.conductorlist.insertItems(0, self.cablelist)
        elif (self.TAButton.isChecked()):
            self.TA_conductors = ["Contact Up-track", "Contact Down-track", "Contact Up-track Difference",
                                  "Contact Down-track Difference"]
            self.conductorlist.insertItems(0, self.TA_conductors)
            self.nodeVoltRadio.setEnabled(False)
            self.branchCurrRadio.setEnabled(False)
            self.time_2d.setChecked(False)
            self.time_2d.setEnabled(False)
        else:
            self.conductorlist.insertItems(0, self.conductors)
        if (self.pqaradio.isChecked() or self.scaradio.isChecked()):
            self.pqabrowse()
            return
        self.timeoptions.setEnabled(True)
        self.timelist.setEnabled(True)
        self.frequencyoptions.setEnabled(False)
        self.frequencyList.setEnabled(False)
        self.frequency_2d.setEnabled(False)
        self.frequency_3d.setEnabled(False)
        if (self.TAButton.isChecked()):
            self.location = os.path.join(self.tadirectories[self.lfaoptions.currentIndex()], "data_ntwrk.mat")
        else:
            self.location = os.path.join(self.lfadirectories[self.lfaoptions.currentIndex()], "data_ntwrk.mat")
        file = io.loadmat(self.location)
        self.tsnap = file["tsnap"]
        self.timeoptions.addItems(self.tsnap)
        if self.isConnectedTime:
            self.timeoptions.activated.disconnect(self.activated)
            self.isConnectedTime = False
        self.timeoptions.activated.connect(self.activated)
        self.isConnectedTime = True

        dir = os.listdir(self.lfadirectories[self.lfaoptions.currentIndex()])
        self.iadirectories = []
        for i in range(0, len(dir)):
            if 'IA' in dir[i] and '.' not in dir[i]:
                self.iadirectories.append(os.path.join(self.lfadirectories[self.lfaoptions.currentIndex()], dir[i]))
        if self.IAButton.isChecked():
            self.ia_options.clear()
            for i in range(0, len(self.iadirectories)):
                dispName = os.path.basename(self.iadirectories[i]).split('/')[-1]
                self.ia_select.setEnabled(True)
                self.ia_options.setEnabled(True)
                self.ia_options.addItem(dispName)
            if(len(self.iadirectories)==0):
                self.ia_options.setEnabled(False)
                self.ia_select.setEnabled(False)
        return

    def activated(self, index):
        """Handles the activation of an item in the time or frequency options.

        This function checks whether the PQA radio button is checked to determine if the frequency options should
        be updated. It adds the selected item to the appropriate list, updates the selected values, removes the item
        from the options, and calls the `radiostatus` function to update the status of related UI elements.

        Parameters:
        index (int): The index of the activated item.

        Returns:
        None"""
        if (self.pqaradio.isChecked()):
            for i in range(len(self.frequencyAvailable)):
                if (self.frequencyoptions.itemText(index) == self.frequencyAvailable[i]):
                    self.selectedFrequency.append(i)
            self.frequencyList.addItem(self.frequencyoptions.itemText(index))
            self.selectedFrequencyValue.append(self.frequencyoptions.itemText(index))
            self.frequencyoptions.removeItem(index)
            self.radiostatus(1)
        else:
            for i in range(len(self.tsnap)):
                if (self.timeoptions.itemText(index) == self.tsnap[i]):
                    self.selectedTsnaps.append(i)
            self.timelist.addItem(self.timeoptions.itemText(index))
            self.selectedTsnapValue.append(self.timeoptions.itemText(index))
            self.timeoptions.removeItem(index)
            self.radiostatus(0)
            return

    def LFA_PQA_SCA(self):
        """Identifies and categorizes directories containing LFA, SCA, and PQA data.

        This function scans the final output directory for subdirectories containing "LFA", "SCA", or "PQA" in their names.
        It then categorizes these directories into `lfadirectories`, `scadirectories`, and `pqadirectories` lists.

        Parameters:
        None

        Returns:
        None"""
        res = self.final_output_directories[0]
        r1 = os.listdir(res)
        for i in range(len(r1)):
            if "LFA" in r1[i]:
                self.lfadirectories.append(os.path.join(res, r1[i]))
            if "SCA" in r1[i]:
                self.scadirectories.append(os.path.join(res, r1[i]))
            if "PQA" in r1[i]:
                self.pqadirectories.append(os.path.join(res, r1[i]))
        return

    def showCheckBoxOpt(self):
        """Configures and enables various UI elements and directories based on the folder paths.

        This function enables radio buttons and plots options, clears file names, and iterates through the specified
        folder paths to find input and output directories. It checks for the presence of specific files to enable
        related UI elements. It also calls the `LFA_PQA_SCA` function to categorize LFA, PQA, and SCA directories.

        Parameters:
        None

        Returns:
        None"""
        self.lfaradio.setEnabled(True)
        self.scaradio.setEnabled(True)
        self.pqaradio.setEnabled(True)
        self.file_names.clear()
        self.Trainplots.setEnabled(True)
        self.Substationplots.setEnabled(True)
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
                        break
        for i in range(len(self.final_input_directories)):
            if 'TimeTableData.csv' in os.listdir(self.final_input_directories[i]) and (
                    'TrainModuleOutput.csv' in os.listdir(self.final_output_directories[0])):
                self.Stringline.setEnabled(True)
                break
        for i in range(len(self.final_input_directories)):
            if 'AllStationData.csv' in os.listdir(self.final_input_directories[i]) and (
                    'TimeTableData.csv' in os.listdir(self.final_input_directories[i])):
                self.Routealtitude.setEnabled(True)
                break
        for i in range(len(self.final_input_directories)):
            if 'AllStationData.csv' in os.listdir(self.final_input_directories[i]) and (
                    'RouteAltitudeData.csv' in os.listdir(self.final_input_directories[i])):
                self.showTimeTable.setEnabled(True)
                break
        if (self.Stringline.isEnabled() or self.Routealtitude.isEnabled()):
            self.stringlineplot.setEnabled(True)
        self.LFA_PQA_SCA()
        for i in range(len(self.final_output_directories)):
            if 'TrainResults.csv' in os.listdir(
                    self.final_output_directories[i]) and 'SubstationResults.csv' in os.listdir(
                    self.final_output_directories[i]):
                self.trainStat.setEnabled(True)
                self.reportGenerate.setEnabled(True)
            else:
                self.trainStat.setEnabled(False)
                self.reportGenerate.setEnabled(False)
        return

    def MTMM(self):
        """Configures the UI elements and updates the MTMMList based on the selected train plots.

        This function clears the MTMM list and the trains list, checks if the Trainplots option is selected,
        and populates the MTMM list with train data if available. It enables or disables various UI elements
        based on the presence of train data.

        Parameters:
        None

        Returns:
        None"""
        self.MTMMList.clear()
        self.trains = []
        if (self.Trainplots.isChecked()):
            self.getTrainNumberData()
            self.MTMMList.addItems(self.trains)
            self.MTMMList.setCurrentItem(self.MTMMList.item(0))
            if(len(self.trains)):
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
            self.counter()
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
            self.plotbtn.setEnabled(False)
            self.subplotbtn.setEnabled(False)
            self.mergeplotbtn.setEnabled(False)
        return

    def getTrainNumberData(self):
        """Retrieves train number data from input directories and filters based on output data.

        This function iterates through the final input directories, extracting train number data from the 
        time table data. It then cross-references this data with the output data to ensure that only valid 
        train numbers are retained in the `trains` list.

        Parameters:
        None

        Returns:
        None"""
        for i in range(0, len(self.final_input_directories)):
            if ("MTMM" in self.final_input_directories[i]):
                data = timeTableData(self.final_input_directories[i])
                for j in range(0, len(data["calculativeData"])):
                    self.trains.append(data["calculativeData"][j]["trainnumber"])
                output_data = pd.read_csv(os.path.join(
                    self.final_output_directories[i], "TrainModuleOutput.csv"))
                for k in range(0, len(self.trains)):
                    popflag = False
                    if (k<len(self.trains)):
                        for j in range(0, len(output_data.columns)//5):
                            if (self.trains[k] in output_data.columns[5*j]):
                                popflag = True
                                break
                    else:
                        continue
                    if not(popflag):
                        self.trains.pop(k)
                        data["calculativeData"].pop(k)
        return

    def current_text_changed(self, text):
        return text

    def counter(self):
        """Updates the state of plot buttons based on the checked status of certain UI elements.

        This function manages the `checkedButtons` list, which contains references to buttons that have been checked.
        It enables or disables plot-related buttons (`plotbtn`, `subplotbtn`, `mergeplotbtn`) based on the number of
        checked buttons in the `checkedButtons` list.

        Parameters:
        None

        Returns:
        None"""
        sender = self.sender()
        if (sender in self.checkedButtons):
            self.checkedButtons.remove(sender)
        else:
            if not (sender == self.Trainplots):
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
        return

    def clickEvent(self):
        """Handles the click event for plotting data based on selected options.

        This function retrieves train number data and then checks which data options (Voltage, Current, Active Power,
        Reactive Power, Tractive Effort, Braking Effort, Velocity) are selected. It collects the corresponding data
        from the output directories, and then calls the appropriate plotting function (plot, subplot, or mergeplot)
        based on the sender of the event.

        Parameters:
        None

        Returns:
        None"""
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
            keys.append("Active Power (kW)")
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
            keys.append("Reactive Power (kVar)")
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
            keys.append("Velocity (km/hr)")
            X_axis.append(x)
            Y_axis.append(y)
        sender = self.sender()
        if (sender == self.plotbtn):
            self.plot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        elif (sender == self.subplotbtn):
            self.subplot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        elif (sender == self.mergeplotbtn):
            self.mergeplot(X_axis, Y_axis, keys, self.Time_radio.isChecked())
        return

    def plot(self, X_axis, Y_axis, keys, timeflag):
        """Plots the data on separate figures based on the provided X and Y axis data.

        This function iterates through the Y_axis data and creates separate figures for each dataset.
        It sets the x-axis label based on the timeflag, adds titles and legends, and configures the plot with
        gridlines and cursors for better visualization.

        Parameters:
        X_axis (list): List of lists containing X-axis data.
        Y_axis (list): List of lists containing Y-axis data.
        keys (list): List of strings representing the titles and y-axis labels for the plots.
        timeflag (bool): Flag to determine whether the x-axis should represent time (True) or distance (False).

        Returns:
        None"""
        for i in range(0, len(Y_axis)):
            for j in range(0, len(Y_axis[i])):
                plt.figure()
                if (timeflag == True):
                    plt.xlabel("Time in Minutes", fontsize=15, fontweight='bold')
                else:
                    plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                plt.title(keys[i], fontsize=15, fontweight='bold')
                plt.plot(X_axis[i][j], Y_axis[i][j],
                         label=str(self.MTMMList.currentItem().text()))
                plt.legend()
                plt.ylabel(keys[i], fontsize=15, fontweight='bold')
                cursor = mplcursors.cursor(hover=True)
                plt.grid(alpha=0.3)
                plt.show(block=False)
        return

    def subplot(self, X_axis, Y_axis, keys, timeflag):
        """Plots the data on subplots within a single figure based on the provided X and Y axis data.

        This function creates subplots for each dataset in Y_axis. If there is only one dataset, it calls the
    `   plot` function to plot it on a single figure. For multiple datasets, it creates subplots within a single
        figure, sets appropriate labels, titles, and legends, and configures the plots with gridlines and cursors
        for better visualization.

        Parameters:
        X_axis (list): List of lists containing X-axis data.
        Y_axis (list): List of lists containing Y-axis data.
        keys (list): List of strings representing the titles and y-axis labels for the plots.
        timeflag (bool): Flag to determine whether the x-axis should represent time (True) or distance (False).

        Returns:
        None"""
        if (len(Y_axis) == 1):
            self.plot(X_axis, Y_axis, keys, timeflag)
            return
        figure, axis = plt.subplots(len(Y_axis))
        for i in range(0, len(Y_axis)):
            if (timeflag == True):
                plt.xlabel("Time in Minutes", fontsize=15, fontweight='bold')
            else:
                plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
            for j in range(0, len(Y_axis[i])):
                axis[i].plot(X_axis[i][j], Y_axis[i][j],
                             label=str(self.MTMMList.currentItem().text()))
                axis[i].set_ylabel(keys[i])
                axis[i].legend()
                axis[i].grid(alpha=0.3)
        cursor = mplcursors.cursor(hover=True)
        plt.show(block=False)
        return

    def mergeplot(self, X_axis, Y_axis, keys, timeflag):
        """Plots two datasets on a single figure with dual y-axes for comparison.

        This function creates a plot with two datasets sharing the same x-axis but having separate y-axes.
        It configures the labels, legends, and gridlines for the plot, and adds interactive cursors for better visualization.

        Parameters:
        X_axis (list): List of lists containing X-axis data.
        Y_axis (list): List of lists containing Y-axis data.
        keys (list): List of strings representing the titles and y-axis labels for the plots.
        timeflag (bool): Flag to determine whether the x-axis should represent time (True) or distance (False).

        Returns:
        None  """
        fig, ax1 = plt.subplots()
        if (timeflag == True):
            plt.xlabel("Time in Minutes", fontsize=15, fontweight='bold')
        else:
            plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
        ax2 = ax1.twinx()
        ax1.plot(X_axis[0][0], Y_axis[0][0], label=(str(
            keys[0]) + " " + str(self.MTMMList.currentItem().text())), color='tab:cyan')
        ax1.set_ylabel(str(keys[0]))
        ax2.plot(X_axis[0][0], Y_axis[1][0], label=(str(
            keys[1]) + " " + str(self.MTMMList.currentItem().text())), color='tab:orange')
        ax2.set_ylabel(str(keys[1]))
        ax1.legend(bbox_to_anchor=(1, 0.95))
        ax2.legend(bbox_to_anchor=(1, 1))
        # plt.legend()
        plt.grid(alpha=0.3)
        cursor = mplcursors.cursor(hover=True)
        plt.show(block=False)
        return

    def PQA(self):
        """Handles the Power Quality Analysis (PQA) based on the selected options.

        This function determines the analysis parameters based on the selected radio buttons and options,
        and calls the appropriate analysis function (`powerQualityAnalysis` or `D3Plot_TA_LFA`) with the 
        correct arguments. It supports both 3D frequency analysis and other analyses with or without IA/TA flags.
        It also plots the results based on the sender of the event (plot, subplot, or mergeplot).

        Parameters:
        None

        Returns:
        None"""
        radioflag = 0
        if self.branchCurrRadio.isChecked():
            radioflag = 1
        sender = self.sender()
        if self.frequency_3d.isChecked():
            powerQualityAnalysis(self.locationDirectories[self.pqa_scaoptions.currentIndex()], self.selectedFrequency,
                                 self.conductorlist.currentRow(), radioflag, 1, 0)
            return
        else:
            IAFlag = 0
            if (self.IAButton.isChecked()):
                IAFlag = 1
                X, Y = powerQualityAnalysis(self.iadirectories[self.ia_options.currentIndex()], self.selectedFrequency,
                                            self.conductorlist.currentRow(), radioflag, 0, IAFlag)
            elif (self.TAButton.isChecked()):
                D3Plot_TA_LFA(self.tadirectories[self.pqa_scaoptions.currentIndex()], self.selectedTsnaps,
                              (self.conductorlist.currentRow()), radioflag, self.TA_conductors)
                return
            else:
                X, Y = powerQualityAnalysis(self.locationDirectories[self.pqa_scaoptions.currentIndex()],
                                            self.selectedFrequency, self.conductorlist.currentRow(), radioflag, 0,
                                            IAFlag)

        if sender == self.pltlfa_pqa_sca:
            if self.frequency_3d.isChecked() == False:
                for i in range(0, len(Y)):
                    plt.figure()
                    plt.title("Power Quality Analysis 2D" if IAFlag == 0 else "Interference Analysis", fontsize=15,
                              fontweight='bold')
                    plt.plot(X[i], Y[i], label=self.selectedFrequencyValue[i])
                    plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                    if radioflag == 1:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=12,
                                   fontweight='bold')
                    else:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=12,
                                   fontweight='bold')
                    plt.xlim(left=min(X[i]), right=max(X[i]))
                    plt.grid(alpha=0.3)
                    plt.legend()
                    for j in range(len(X[i])):
                            if (j%6==0):
                                plt.scatter(X[i][j],Y[i][j],c="red",marker='x')
                    plt.show(block=False)
        if (sender == self.subpltlfa_pqa_sca):
            t = len(Y)
            while (t > 0):
                if (t // 3 > 0):
                    j = 3
                else:
                    j = t
                if (j == 1):
                    plt.figure()
                    plt.title("Power Quality Analysis 2D" if not self.IAButton.isChecked() else (
                        "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                              fontsize=15, fontweight='bold')
                    plt.plot(X[t - 1], Y[t - 1], label=self.selectedFrequencyValue[t - 1])
                    plt.xlabel("Distance (km)", fontsize=12, fontweight='bold')
                    if radioflag == 1:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=15,
                                   fontweight='bold')
                    else:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=15,
                                   fontweight='bold')
                    plt.xlim(left=min(X[t - 1]), right=max(X[t - 1]))
                    plt.grid(alpha=0.3)
                    plt.legend()
                    plt.show(block=False)
                    break
                else:
                    figure, axis = plt.subplots(j)
                    plt.suptitle("Power Quality Analysis 2D" if not self.IAButton.isChecked() else (
                        "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                              fontsize=15, fontweight='bold')
                    for i in range(0, len(Y)):
                        axis[i].plot(X[t - 1], Y[t - 1], label=self.selectedFrequencyValue[t - 1])
                        if radioflag == 1:
                            axis[i].set_ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)",
                                               fontsize=12, fontweight='bold')
                        else:
                            axis[i].set_ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)",
                                               fontsize=12, fontweight='bold')
                        axis[i].set_xlabel("Distance (km)", fontsize=12, fontweight='bold')
                        axis[i].legend()
                        axis[i].set_xlim(left=min(X[t - 1]), right=max(X[t - 1]))
                        axis[i].grid(alpha=0.3)
                        t -= 1
                        if (t == 0):
                            break
                    plt.show(block=False)
        if (sender == self.mergepltlfa_pqa_sca):
            for i in range(0, len(Y)):
                plt.title("Power Quality Analysis 2D" if IAFlag == 0 else (
                    "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                          fontsize=15, fontweight='bold')
                plt.plot(X[i], Y[i], label=self.selectedFrequencyValue[i])
                plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                if radioflag == 1:
                    plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=15,
                               fontweight='bold')
                else:
                    plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=15,
                               fontweight='bold')
                plt.xlim(left=min(X[i]), right=max(X[i]))
                plt.grid(alpha=0.3)
                plt.legend()
                plt.show(block=False)
        return

    def LFA(self):
        """Handles the Load Flow Analysis (LFA) based on the selected options.

        This function determines the analysis parameters based on the selected radio buttons and options,
        and calls the appropriate analysis function (`loadFlowAnalysis`, `D3Plot_TA_LFA`, or `ShortCircuitAnalysis`) 
        with the correct arguments. It supports both 3D time analysis and other analyses with or without IA/TA flags.
        It also plots the results based on the sender of the event (plot, subplot, or mergeplot).

        Parameters:
        None

        Returns:
        None"""
        if (self.pqaradio.isChecked()):
            self.PQA()
            return
        sender = self.sender()
        radioflag = 0
        if self.branchCurrRadio.isChecked():
            radioflag = 1
        if (self.lfaradio.isChecked()):
            if self.time_3d.isChecked() and not (self.TAButton.isChecked()):
                loadFlowAnalysis(self.lfadirectories[self.lfaoptions.currentIndex()], self.selectedTsnaps,
                                 self.conductorlist.currentRow(), radioflag, 1, 0)
            else:
                IAFlag = 0
                if (self.IAButton.isChecked()):
                    IAFlag = 1
                    X, Y = loadFlowAnalysis(self.iadirectories[self.ia_options.currentIndex()], self.selectedTsnaps,
                                            (self.conductorlist.currentRow()), radioflag, 0, IAFlag)
                elif (self.TAButton.isChecked()):
                    D3Plot_TA_LFA(self.tadirectories[self.lfaoptions.currentIndex()], self.selectedTsnaps,
                                  (self.conductorlist.currentRow()), radioflag, self.TA_conductors)
                    return
                else:
                    X, Y, TSS = loadFlowAnalysis(self.lfadirectories[self.lfaoptions.currentIndex()], self.selectedTsnaps,
                                            (self.conductorlist.currentRow()), radioflag, 0, IAFlag)
            if (sender == self.pltlfa_pqa_sca):
                if self.time_3d.isChecked() == False:
                    for i in range(0, len(Y)):
                        plt.figure()
                        plt.title("Load Flow Analysis 2D" if IAFlag == 0 else (
                            "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                                  fontsize=15, fontweight='bold')
                        plt.plot(X[i], Y[i], label=self.selectedTsnapValue[i])
                        if not(self.IAButton.isChecked()):
                            for j in range (0, len(TSS['distance'])):
                                xcoord = float(TSS['distance'][j][0][0])/max(X[i]) +0.005
                                plt.text(xcoord, 0.97, TSS['name'][j][0],transform=plt.gca().transAxes)
                                plt.axvline(x = float(TSS['distance'][j][0][0]), linestyle = '--',color = 'b')
                        plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                        if radioflag == 1:
                            plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=15,
                                       fontweight='bold')
                        else:
                            plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=15,
                                       fontweight='bold')
                        plt.xlim(left=min(X[i]), right=max(X[i]))
                        plt.grid(alpha=0.3)
                        plt.legend()
                        for j in range(len(X[i])):
                            if (j%6==0):
                                plt.scatter(X[i][j],Y[i][j],c="red",marker='x')
                        plt.show(block=False)
        if self.scaradio.isChecked():
            if (self.IAButton.isChecked()):
                ShortCircuitAnalysis_IA(self.iadirectories[self.ia_options.currentIndex()],
                                        self.conductorlist.currentRow(), self.conductors, radioflag)
            elif (self.TAButton.isChecked()):
                D3Plot_TA_SCA(self.locationDirectories[self.pqa_scaoptions.currentIndex()],
                              self.conductorlist.currentRow(), 1, self.conductors)
                return
            else:
                ShortCircuitAnalysis(self.locationDirectories[self.pqa_scaoptions.currentIndex()],
                                     self.conductorlist.currentRow(), self.conductors, radioflag)
        if (sender == self.subpltlfa_pqa_sca):
            t = len(Y)
            while (t > 0):
                if (t // 3 > 0):
                    j = 3
                else:
                    j = t
                if (j == 1):
                    plt.figure()
                    plt.title("Load Flow Analysis 2D" if IAFlag == 0 else (
                        "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                              fontsize=15, fontweight='bold')
                    plt.plot(X[t - 1], Y[t - 1], label=self.selectedTsnapValue[t - 1])
                    if not(self.IAButton.isChecked()):
                        for j in range (0, len(TSS['distance'])):
                                xcoord = float(TSS['distance'][j][0][0])/max(X[i]) +0.005
                                plt.text(xcoord, 0.97, TSS['name'][j][0],transform=plt.gca().transAxes)
                                plt.axvline(x = float(TSS['distance'][j][0][0]), linestyle = '--',color = 'b')
                    plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                    if radioflag == 1:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=15,
                                   fontweight='bold')
                    else:
                        plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=15,
                                   fontweight='bold')
                    plt.xlim(left=min(X[t - 1]), right=max(X[t - 1]))
                    plt.grid(alpha=0.3)
                    plt.legend()
                    plt.show(block=False)
                    break
                else:
                    figure, axis = plt.subplots(j)
                    plt.suptitle("Load Flow Analysis 2D" if IAFlag == 0 else (
                        "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                              fontsize=15, fontweight='bold')
                    for i in range(0, j):
                        if not(self.IAButton.isChecked()):
                            for k in range (0, len(TSS['distance'])):
                                xcoord = float(TSS['distance'][k][0][0])/max(X[i]) +0.005
                                axis[i].text(xcoord, 0.97, TSS['name'][k][0],transform=plt.gca().transAxes)
                                axis[i].axvline(x = float(TSS['distance'][k][0][0]), linestyle = '--',color = 'b')
                        
                        axis[i].plot(X[t - 1], Y[t - 1], label=self.selectedTsnapValue[t - 1])
                        if radioflag == 1:
                            axis[i].set_ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)",
                                               fontweight='bold')
                        else:
                            axis[i].set_ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)",
                                               fontweight='bold')
                        axis[i].set_xlabel("Distance (km)", fontweight='bold')
                        axis[i].legend()
                        axis[i].set_xlim(left=min(X[t - 1]), right=max(X[t - 1]))
                        axis[i].grid(alpha=0.3)
                        t -= 1
                        if (t == 0):
                            break
                    plt.show(block=False)
        if (sender == self.mergepltlfa_pqa_sca):
            for i in range(0, len(Y)):
                plt.title("Load Flow Analysis 2D" if IAFlag == 0 else (
                    "Current in Signalling Cables" if radioflag == 1 else "Terminal Voltage in Signalling Cables"),
                          fontsize=15, fontweight='bold')
                if not(self.IAButton.isChecked()):
                    for j in range (0, len(TSS['distance'])):
                        xcoord = float(TSS['distance'][j][0][0])/max(X[i]) +0.005
                        plt.text(xcoord, 0.97, TSS['name'][j][0],transform=plt.gca().transAxes)
                        plt.axvline(x = float(TSS['distance'][j][0][0]), linestyle = '--',color = 'b')
                plt.plot(X[i], Y[i], label=self.selectedTsnapValue[i])
                plt.xlabel("Distance (km)", fontsize=15, fontweight='bold')
                if radioflag == 1:
                    plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Current (A)", fontsize=15,
                               fontweight='bold')
                else:
                    plt.ylabel(self.conductors[self.conductorlist.currentRow()] + " Voltage (kV)", fontsize=15,
                               fontweight='bold')
                plt.xlim(left=min(X[i]), right=max(X[i]))
                plt.grid(alpha=0.3)
                plt.legend()
                plt.show(block=False)
        return

    def getStringLineData(self):
        """Generates a string line diagram based on train data from input and output directories.

        This function retrieves train data from the final input directories, filters it based on the presence in the
        output directories, and generates a string line diagram. It plots the distance vs. time for each train,
        inverts the y-axis, sets custom ticks, and configures the plot with legends, labels, and interactive cursors.

        Parameters:
        None

        Returns:
        None"""
        for i in range(0, len(self.final_input_directories)):
            if ("MTMM" in self.final_input_directories[i]):
                x_axis = []
                y_axis = []
                start = 0
                end = 0
                output_data = pd.read_csv(os.path.join(
                    self.final_output_directories[i], "TrainModuleOutput.csv"))
                data = timeTableData(self.final_input_directories[i])
                trains = []
                for j in range(0, len(data["calculativeData"])):
                    trains.append(data["calculativeData"][j]["trainnumber"])

                for k in range(0, len(trains)):
                    popflag = False
                    if (k<len(trains)):
                        for j in range(0, len(output_data.columns)//5):
                            if (trains[k] in output_data.columns[5*j]):
                                popflag = True
                                break
                    else:
                        continue
                    if not(popflag):
                        trains.pop(k)
                        data["calculativeData"].pop(k)
                    
                for j in range(0, len(data["calculativeData"])):
                    if (int(output_data["Up/Downtrack_" + str(trains[j]) + "_0"][1]) == 0):
                        partstr = "Uptrack"
                    else:
                        partstr = "Downtrack"
                    for k in range(0, len(output_data['Distance_' + partstr + '_' + str(trains[j]) + '_0'])):
                        if (float(output_data["Velocity_" + partstr + "_" + str(trains[j]) + "_0"][k]) > 0.0):
                            start = k
                            break
                    for k in range(0, len(output_data['Distance_' + partstr + '_' + str(trains[j]) + '_0'])):
                        if (float(output_data["Velocity_" + partstr + "_" + str(trains[j]) + "_0"][k]) == 0.0):
                            if (float(
                                    output_data["Distance_" + partstr + "_" + str(trains[j]) + "_0"][k]) == float(
                                    data["calculativeData"][j]["endDistance"])):
                                end = k
                                break
                    x_axis.append(
                        (output_data['Distance_' + partstr + '_' + str(trains[j]) + '_0'][start:end]))
                    y_axis.append(
                        (output_data['Time_' + partstr + '_' + str(trains[j]) + '_0'][start:end]) * 60)
                    plt.plot(x_axis[j], y_axis[j],
                             label=trains[j])
                plt.gca().invert_yaxis()
                plt.yticks(data["plottingData"][1], data["plottingData"][0])
                plt.xticks(data["plottingData"][3], data["plottingData"][2])
                plt.xlim(left=min(data["plottingData"][3]), right=max(data["plottingData"][3]))
                plt.legend(loc='center left', bbox_to_anchor=(1, 1))
                plt.xlabel("Distance from Starting Point (km)",
                           fontsize=15, fontweight='bold')
                plt.ylabel("Time", fontsize=15, fontweight='bold')
                plt.title("String Line Diagram", fontsize=15, fontweight='bold')
                plt.get_current_fig_manager().resize(950, 500)
                plt.grid(alpha=0.3)
                cursor = mplcursors.cursor(hover=True)
                # binding_id = plt.connect('motion_notify_event', on_move)
                plt.show(block=False)
        return

    def showdialog(self):
        """Toggles the visibility of the timetable dialog and populates it with train data.

        This function toggles the visibility of the timetable dialog and, if the dialog is to be shown,
        it populates the table with train timetable data from the input directories. It sets the table's
        column and row counts, headers, and fills the table with arrival, dwell, and departure times for each station.

        Parameters:
        None

        Returns:
        None"""
        self.timetableflag = not (self.timetableflag)
        if self.timetableflag:
            for i in range(len(self.final_input_directories)):
                if ("MTMM" in self.final_input_directories[i]):
                    dict = timeTableExcel(self.final_input_directories[i])
            self.timetable_trainstat.setColumnCount(1 + 3 * (len(dict)))
            self.timetable_trainstat.setRowCount(1 + len(dict[0]["stationNameToDisplay"]))
            labels = ["Station Name"]
            for i in range(len(dict)):
                column = (i * 3) + 1
                item = QtWidgets.QTableWidgetItem(dict[i]["trainnumber"])
                self.timetable_trainstat.setSpan(0, column, 1, 3)
                self.timetable_trainstat.setItem(0, column, item)
                temp = ["Arrival Time", "Dwell Time (in mins)", "Departure Time"]
                labels.extend(temp)
                for j in range(len(dict[0]["stationNameToDisplay"])):
                    item3 = QtWidgets.QTableWidgetItem(dict[0]["stationNameToDisplay"][j])
                    self.timetable_trainstat.setItem(j + 1, 0, item3)
                    for k in range(len(dict[i]["actualStationName"])):
                        for l in range(len(dict[0]["stationNameToDisplay"])):
                            if (dict[i]["actualStationName"][k] == dict[0]["stationNameToDisplay"][l]):
                                item = QtWidgets.QTableWidgetItem(
                                    dict[i]["timeFromStarting"][int(dict[i]["stationNumber"][l]) - 1])
                                item2 = QtWidgets.QTableWidgetItem(
                                    dict[i]["dwellTime"][int(dict[i]["stationNumber"][l]) - 1])
                                item3 = QtWidgets.QTableWidgetItem(
                                    dict[i]["departureTime"][int(dict[i]["stationNumber"][l]) - 1])
                                self.timetable_trainstat.setItem(l + 1, column, item)
                                self.timetable_trainstat.setItem(l + 1, column + 1, item2)
                                self.timetable_trainstat.setItem(l + 1, column + 2, item3)
                                break
                            else:
                                item = QtWidgets.QTableWidgetItem(dict[i]["timeFromStarting"][j])
                                item2 = QtWidgets.QTableWidgetItem(dict[i]["dwellTime"][j])
                                item3 = QtWidgets.QTableWidgetItem(dict[i]["departureTime"][j])
                                self.timetable_trainstat.setItem(j + 1, column, item)
                                self.timetable_trainstat.setItem(j + 1, column + 1, item2)
                                self.timetable_trainstat.setItem(j + 1, column + 2, item3)
            self.timetable_trainstat.setHorizontalHeaderLabels(labels)
            self.timetable_trainstat.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.timetable_trainstat.resizeColumnsToContents()
            self.timetable_trainstat.setHidden(False)
            self.showTimeTable.setText("Hide Time Table")
            self.trainStat.setText("Show Train Statistics")
            self.trainstatflag = False
            return
        else:
            self.showTimeTable.setText("Show Time Table")
            self.timetable_trainstat.setHidden(True)
            return

    def stringLinePlotClick(self):
        """Handles the click event for plotting string line and route altitude data.

        This function checks if the Stringline or Routealtitude options are selected.
        If Stringline is selected, it calls the `getStringLineData` function to plot the string line data.
        If Routealtitude is selected, it iterates over the input directories and calls the `routeAltitudeData` 
        function to plot the route altitude data.

        Parameters:
        None

        Returns:
        None"""
        if (self.Stringline.isChecked()):
            plt.figure()
            self.getStringLineData()
        if (self.Routealtitude.isChecked()):
            plt.figure()
            for i in range(0, len(self.final_input_directories)):
                if ("MTMM" in self.final_input_directories[i]):
                    routeAltitudeData(self.final_input_directories[i])
        return

    def findFolders(self, start_dir):
        """Finds directories containing 'output' in their name within a starting directory.

        This function walks through the given starting directory and its subdirectories to find directories
        that contain 'output' in their name. It collects the absolute paths of the parent directories of these
        'output' directories and returns them.

        Parameters:
        start_dir (str): The starting directory to begin the search.

        Returns:
        list: A list of absolute paths to the parent directories of found 'output' directories."""
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
        """Finds files with specific extensions within a starting directory.

        This function walks through the given starting directory and its subdirectories to find files with
        extensions '.xlsx', '.mat', and '.csv'. It collects the absolute paths of these files and returns them.

        Parameters:
        start_dir (str): The starting directory to begin the search.

        Returns:
        list: A list of absolute paths to the found files"""
        file_extension = [".xlsx", ".mat", ".csv"]
        file_results_path = []
        for ext in file_extension:
            for root, dirs, files in os.walk(start_dir):
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        file_results_path.append(file_path)
        return file_results_path


# app = QApplication(sys.argv)
# font = QtGui.QFont()
# font.setPointSize(12)
# app.setFont(font)
# mainwindow = MainWindow()
# mainwindow.showMaximized()
# sys.exit(app.exec_())
