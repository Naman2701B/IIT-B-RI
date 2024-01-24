import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QPushButton
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import io
from matplotlib import interactive


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.browse.clicked.connect(self.browsefiles)
        self.plotbtn.clicked.connect(self.plot)
        self.subplotbtn.clicked.connect(self.subplot)
        self.mergeplotbtn.clicked.connect(self.mergeplot)
        self.selectbtn.clicked.connect(self.showCheckBoxOpt)
        self.options.currentTextChanged.connect(self.current_text_changed)
        self.check1.clicked.connect(self.stateChange)
        self.check2.clicked.connect(self.stateChange)
        self.check3.clicked.connect(self.stateChange)
        self.checkboxes.setExclusive(False)
        self.checkboxes.addButton(self.check1, 0)
        self.checkboxes.addButton(self.check2, 1)
        self.checkboxes.addButton(self.check3, 2)
        self.check1.setEnabled(False)
        self.check2.setEnabled(False)
        self.check3.setEnabled(False)
        self.file_paths = []
        self.checkedButtons = []

    def browsefiles(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Choose a Folder', '')
        if (fname):
            folder_paths = self.findFolders(fname)
            self.options.clear()
            self.addOpt(folder_paths)
        self.filename.setText(fname)

    def addOpt(self, paths):
        for path in paths:
            self.options.addItem(path)

    def showCheckBoxOpt(self):
        self.check1.setEnabled(False)
        self.check2.setEnabled(False)
        self.check3.setEnabled(False)
        file_paths_local = self.findFiles(self.options.currentText())
        self.file_paths = file_paths_local
        file_names = []
        for i in range(0, len(file_paths_local)):
            file_names.append(os.path.basename(
                file_paths_local[i]).split('/')[-1])
        for i in range(0, len(file_names)):
            if (self.check1.text() in file_names[i]):
                self.check1.setEnabled(True)
        for i in range(0, len(file_names)):
            if (self.check2.text() in file_names[i]):
                self.check2.setEnabled(True)
        for i in range(0, len(file_names)):
            if (self.check3.text() in file_names[i]):
                self.check3.setEnabled(True)

    def current_text_changed(self, text):
        return text

    def stateChange(self):
        sender = self.sender()
        if (sender == self.check1):
            if (0 in self.checkedButtons):
                self.checkedButtons.remove(0)
            else:
                self.checkedButtons.append(0)
        elif (sender == self.check2):
            if (1 in self.checkedButtons):
                self.checkedButtons.remove(1)
            else:
                self.checkedButtons.append(1)
        else:
            if (2 in self.checkedButtons):
                self.checkedButtons.remove(2)
            else:
                self.checkedButtons.append(2)

    def plot(self):
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
            plt.plot(X_axis, Y_axis)
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
            axis[i].plot(X_axis, Y_axis)
        plt.show()

    def mergeplot(self):
        Y_axis = []
        for i in range(0, len(self.checkedButtons)):
            if (self.file_paths[self.checkedButtons[i]].endswith(".xlsx")):
                file = pd.read_excel(
                    self.file_paths[self.checkedButtons[i]], header=None)
                X_axis = file[0]
                Y_axis.append(file[1])
            else:
                file = io.loadmat(
                    file_name=self.file_paths[self.checkedButtons[i]])
                X_axis = file["a"]
                Y_axis.append(file["b"])
            plt.plot(X_axis, Y_axis[i])
        plt.show()

    def findFolders(self, start_dir):
        directory_results = []
        for root, dirs, files in os.walk(start_dir):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                directory_results.append(dir_path)
            break
        return directory_results

    def findFiles(self, start_dir):
        file_extension = [".xlsx", ".mat"]
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
widget.setFixedWidth(1000)
widget.setFixedHeight(500)
widget.show()
sys.exit(app.exec_())
