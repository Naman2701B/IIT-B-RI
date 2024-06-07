import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QComboBox
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import io


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.browse.clicked.connect(self.browsefiles)
        self.plotbtn.clicked.connect(self.plot)
        self.options.currentTextChanged.connect(self.current_text_changed)

    def browsefiles(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Choose a Folder', '')
        if (fname):
            file_paths = self.findFiles(fname)
            self.addOpt(file_paths)
        self.filename.setText(fname)

    def addOpt(self, paths):
        for path in paths:
            self.options.addItem(path)

    def current_text_changed(self, text):
        return text

    def plot(self):
        if (self.options.currentText().endswith(".xlsx")):
            file = pd.read_excel(self.options.currentText(), header=None)
            X_axis = file[0]
            Y_axis = file[1]
        else:
            file = io.loadmat(file_name=self.options.currentText())
            X_axis = file["a"]
            Y_axis = file["b"]
        plt.plot(X_axis, Y_axis)
        plt.show()

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
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_())
