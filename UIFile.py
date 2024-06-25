from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("ETPSS Output Module")
        Dialog.resize(817, 599)
        labelImage = QtWidgets.QLabel(Dialog)
        pixmap = QtGui.QPixmap("IITB.png")
        pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        labelImage.setPixmap(pixmap)
        labelImage.move(1765,800)
        namelabel = QtWidgets.QLabel("Made By Naman Badlani, Onam Sarode, Allen Andrew",Dialog)
        namelabel.move(20,960)
        self.filename = QtWidgets.QLineEdit(Dialog)
        self.filename.setGeometry(QtCore.QRect(20, 10, 601, 31))
        self.filename.setObjectName("filename")
        self.browse = QtWidgets.QPushButton(Dialog)
        self.browse.setGeometry(QtCore.QRect(640, 10, 201, 31))
        self.browse.setObjectName("browse")
        self.options = QtWidgets.QComboBox(Dialog)
        self.options.setGeometry(QtCore.QRect(861, 10, 400, 31))
        self.options.setObjectName("options")
        self.selectbtn = QtWidgets.QPushButton(Dialog)
        self.selectbtn.setGeometry(QtCore.QRect(1281, 10, 93, 31))
        self.selectbtn.setObjectName("selectbtn")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 50, 1704, 910))
        self.groupBox_2.setObjectName("groupBox_2")
        self.timetable_trainstat = QtWidgets.QTableWidget(parent=self.groupBox_2)
        self.timetable_trainstat.setGeometry(QtCore.QRect(10,380,1120,500))
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(520, 30, 610, 340))
        self.groupBox_3.setObjectName("groupBox_3")
        self.MTMMList = QtWidgets.QListWidget(self.groupBox_3)
        self.MTMMList.setGeometry(QtCore.QRect(20, 60, 161, 273))
        self.MTMMList.setObjectName("MTMMList")
        self.Tractiveeffort = QtWidgets.QCheckBox(self.groupBox_3)
        self.Tractiveeffort.setGeometry(QtCore.QRect(201, 180, 200, 30))
        self.Tractiveeffort.setObjectName("Tractiveeffort")
        self.line_4 = QtWidgets.QFrame(self.groupBox_3)
        self.line_4.setGeometry(QtCore.QRect(395, 60, 20, 210))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(281, 30, 90, 30))
        self.label_5.setObjectName("label_5")
        self.Reactivepower = QtWidgets.QCheckBox(self.groupBox_3)
        self.Reactivepower.setGeometry(QtCore.QRect(201, 150, 200, 30))
        self.Reactivepower.setObjectName("Reactivepower")
        self.Activepower = QtWidgets.QCheckBox(self.groupBox_3)
        self.Activepower.setGeometry(QtCore.QRect(201, 120, 171, 30))
        self.Activepower.setObjectName("Activepower")
        self.Voltage = QtWidgets.QCheckBox(self.groupBox_3)
        self.Voltage.setGeometry(QtCore.QRect(201, 60, 171, 30))
        self.Voltage.setObjectName("Voltage")
        self.Brakingeffort = QtWidgets.QCheckBox(self.groupBox_3)
        self.Brakingeffort.setGeometry(QtCore.QRect(201, 210, 200, 30))
        self.Brakingeffort.setObjectName("Brakingeffort")
        self.velocity = QtWidgets.QCheckBox(self.groupBox_3)
        self.velocity.setGeometry(QtCore.QRect(201, 240, 171, 30))
        self.velocity.setObjectName("velocity")
        self.Current = QtWidgets.QCheckBox(self.groupBox_3)
        self.Current.setGeometry(QtCore.QRect(201, 90, 171, 30))
        self.Current.setObjectName("Current")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(471, 30, 90, 30))
        self.label_7.setObjectName("label_7")
        self.mergeplotbtn = QtWidgets.QPushButton(self.groupBox_3)
        self.mergeplotbtn.setGeometry(QtCore.QRect(501, 300, 100, 36))
        self.mergeplotbtn.setObjectName("mergeplotbtn")
        self.subplotbtn = QtWidgets.QPushButton(self.groupBox_3)
        self.subplotbtn.setGeometry(QtCore.QRect(351, 300, 100, 36))
        self.subplotbtn.setObjectName("subplotbtn")
        self.plotbtn = QtWidgets.QPushButton(self.groupBox_3)
        self.plotbtn.setGeometry(QtCore.QRect(201, 300, 100, 36))
        self.plotbtn.setObjectName("plotbtn")
        self.Trainplots = QtWidgets.QCheckBox(self.groupBox_3)
        self.Trainplots.setGeometry(QtCore.QRect(20, 30, 161, 30))
        self.Trainplots.setObjectName("Trainplots")
        self.Time_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.Time_radio.setGeometry(QtCore.QRect(411, 60, 171, 30))
        self.Time_radio.setObjectName("Time_radio")
        self.Distance_radio = QtWidgets.QRadioButton(self.groupBox_3)
        self.Distance_radio.setGeometry(QtCore.QRect(411, 90, 171, 30))
        self.Distance_radio.setObjectName("Distance_radio")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 500, 340))
        self.groupBox.setObjectName("groupBox")
        self.Stringline = QtWidgets.QCheckBox(self.groupBox)
        self.Stringline.setGeometry(QtCore.QRect(30, 30, 261, 30))
        self.Stringline.setObjectName("Stringline")
        self.unselected = QtWidgets.QListWidget(self.groupBox)
        self.unselected.setGeometry(QtCore.QRect(30, 110, 161, 61))
        self.unselected.setObjectName("unselected")
        self.trainStat = QtWidgets.QPushButton(self.groupBox)
        self.trainStat.setGeometry(QtCore.QRect(275, 150, 200, 35))
        self.trainStat.setObjectName("trainStat")
        self.reportGenerate = QtWidgets.QPushButton(self.groupBox)
        self.reportGenerate.setGeometry(QtCore.QRect(275, 250, 200, 35))
        self.reportGenerate.setObjectName("reportGenerate")
        self.showTimeTable = QtWidgets.QPushButton(self.groupBox)
        self.showTimeTable.setGeometry(QtCore.QRect(275, 200, 200, 30))
        self.showTimeTable.setObjectName("showTimeTable")
        self.stringlineplot = QtWidgets.QPushButton(self.groupBox)
        self.stringlineplot.setGeometry(QtCore.QRect(275, 301, 93, 30))
        self.stringlineplot.setObjectName("stringlineplot")
        self.Routealtitude = QtWidgets.QCheckBox(self.groupBox)
        self.Routealtitude.setGeometry(QtCore.QRect(275, 30, 261, 30))
        self.Routealtitude.setObjectName("Routealtitude")
        self.Trainplots1 = QtWidgets.QCheckBox(self.groupBox)
        self.Trainplots1.setGeometry(QtCore.QRect(30, 70, 161, 30))
        self.Trainplots1.setObjectName("Trainplots1")
        self.Substationplots = QtWidgets.QCheckBox(self.groupBox)
        self.Substationplots.setGeometry(QtCore.QRect(30, 180, 261, 21))
        self.Substationplots.setObjectName("Substationplots")
        self.selected = QtWidgets.QListWidget(self.groupBox)
        self.selected.setGeometry(QtCore.QRect(30, 210, 161, 122))
        self.selected.setObjectName("selected")
        self.analysistab = QtWidgets.QTabWidget(self.groupBox_2)
        self.analysistab.setGeometry(QtCore.QRect(1140, 30, 550, 865))
        self.analysistab.setTabsClosable(False)
        self.analysistab.setObjectName("analysistab")
        self.tab = QtWidgets.QWidget()
        self.tab.setAutoFillBackground(True)
        self.tab.setObjectName("tab")
        self.line_41 = QtWidgets.QFrame(self.tab)
        self.line_41.setGeometry(QtCore.QRect(0, 40, 550, 10))
        self.line_41.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_41.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_41.setObjectName("line_41")
        self.IARadioOptions = QtWidgets.QButtonGroup(self.tab)
        self.IARadioOptions.setObjectName("IARadioOptions")
        self.IAButton = QtWidgets.QRadioButton(self.tab)
        self.IAButton.setGeometry(QtCore.QRect(10, 10, 260, 31))
        self.IAButton.setObjectName("IAButton")
        self.TAButton = QtWidgets.QRadioButton(self.tab)
        self.TAButton.setGeometry(QtCore.QRect(280, 10, 260, 31))
        self.TAButton.setObjectName("TAButton")
        self.lfaradiooptions = QtWidgets.QButtonGroup(self.tab)
        self.lfaradiooptions.setObjectName("lfaradiooptions")
        self.lfaradio = QtWidgets.QRadioButton(self.tab)
        self.lfaradio.setGeometry(QtCore.QRect(10, 50, 230, 31))
        self.lfaradio.setObjectName("lfaradio")
        self.scaradio = QtWidgets.QRadioButton(self.tab)
        self.scaradio.setGeometry(QtCore.QRect(10, 80, 250, 31))
        self.scaradio.setObjectName("scaradio")
        self.pqaradio = QtWidgets.QRadioButton(self.tab)
        self.pqaradio.setGeometry(QtCore.QRect(10, 110, 250, 31))
        self.pqaradio.setObjectName("pqaradio")
        self.lfaoptions = QtWidgets.QComboBox(self.tab)
        self.lfaoptions.setGeometry(QtCore.QRect(10, 150, 350, 30))
        self.lfaoptions.setObjectName("lfaoptions")
        self.lfaselect = QtWidgets.QPushButton(self.tab)
        self.lfaselect.setGeometry(QtCore.QRect(380, 150, 80, 30))
        self.lfaselect.setObjectName("lfaselect")
        self.pqa_scaoptions = QtWidgets.QComboBox(self.tab)
        self.pqa_scaoptions.setGeometry(QtCore.QRect(10, 185, 350, 30))
        self.pqa_scaoptions.setObjectName("pqa_scaoptions")
        self.pqa_sca_select = QtWidgets.QPushButton(self.tab)
        self.pqa_sca_select.setGeometry(QtCore.QRect(380, 185, 80, 30))
        self.pqa_sca_select.setObjectName("pqa_sca_select")
        self.ia_options = QtWidgets.QComboBox(self.tab)
        self.ia_options.setGeometry(QtCore.QRect(10, 220, 350, 30))
        self.ia_options.setObjectName("ia_options")
        self.ia_select = QtWidgets.QPushButton(self.tab)
        self.ia_select.setGeometry(QtCore.QRect(380, 220, 80, 30))
        self.ia_select.setObjectName("ia_select")
        self.pltlfa_pqa_sca = QtWidgets.QPushButton(self.tab)
        self.pltlfa_pqa_sca.setGeometry(QtCore.QRect(10, 750, 120, 40))
        self.pltlfa_pqa_sca.setObjectName("pltlfa_pqa_sca")
        self.subpltlfa_pqa_sca = QtWidgets.QPushButton(self.tab)
        self.subpltlfa_pqa_sca.setGeometry(QtCore.QRect(210, 750, 120, 40))
        self.subpltlfa_pqa_sca.setObjectName("subpltlfa_pqa_sca")
        self.mergepltlfa_pqa_sca = QtWidgets.QPushButton(self.tab)
        self.mergepltlfa_pqa_sca.setGeometry(QtCore.QRect(410, 750, 120, 40))
        self.mergepltlfa_pqa_sca.setObjectName("mergepltlfa_pqa_sca")
        self.timeoptions = QtWidgets.QComboBox(self.tab)
        self.timeoptions.setGeometry(QtCore.QRect(10, 270, 191, 30))
        self.timeoptions.setObjectName("timeoptions")
        self.timeoptions.addItem("")
        self.selectAllTime = QtWidgets.QPushButton(self.tab)
        self.selectAllTime.setGeometry(QtCore.QRect(10, 305, 161, 31))
        self.selectAllTime.setObjectName("selectAllTime")
        self.frequencyoptions = QtWidgets.QComboBox(self.tab)
        self.frequencyoptions.setGeometry(QtCore.QRect(10, 345, 191, 30))
        self.frequencyoptions.setObjectName("frequencyoptions")
        self.frequencyoptions.addItem("")
        self.selectAllFrequency = QtWidgets.QPushButton(self.tab)
        self.selectAllFrequency.setGeometry(QtCore.QRect(10, 380, 161, 31))
        self.selectAllFrequency.setObjectName("selectAllFrequency")
        self.timelist = QtWidgets.QListWidget(self.tab)
        self.timelist.setGeometry(QtCore.QRect(210, 270, 321, 41))
        self.timelist.setObjectName("timelist")
        self.frequencyList = QtWidgets.QListWidget(self.tab)
        self.frequencyList.setGeometry(QtCore.QRect(210, 345, 321, 41))
        self.frequencyList.setObjectName("frequencyList")
        self.timebuttons = QtWidgets.QButtonGroup(self.tab)
        self.timebuttons.setObjectName("timebuttons")
        self.time_2d = QtWidgets.QRadioButton(self.tab)
        self.time_2d.setGeometry(QtCore.QRect(210, 310, 141, 31))
        self.time_2d.setObjectName("time_2d")
        self.time_3d = QtWidgets.QRadioButton(self.tab)
        self.time_3d.setGeometry(QtCore.QRect(460, 310, 141, 31))
        self.time_3d.setObjectName("time_3d")
        self.frequencybuttons = QtWidgets.QButtonGroup(self.tab)
        self.frequencybuttons.setObjectName("frequencybuttons")
        self.frequency_2d = QtWidgets.QRadioButton(self.tab)
        self.frequency_2d.setGeometry(QtCore.QRect(210, 385, 141, 31))
        self.frequency_2d.setObjectName("frequency_2d")
        self.frequency_3d = QtWidgets.QRadioButton(self.tab)
        self.frequency_3d.setGeometry(QtCore.QRect(460, 385, 141, 31))
        self.frequency_3d.setObjectName("frequency_3d")
        self.conductorlist = QtWidgets.QListWidget(self.tab)
        self.conductorlist.setGeometry(QtCore.QRect(10, 430, 521, 250))
        self.conductorlist.setObjectName("conductorlist")
        self.voltCurrentbuttons = QtWidgets.QButtonGroup(self.tab)
        self.voltCurrentbuttons.setObjectName("voltCurrentbuttons")
        self.nodeVoltRadio = QtWidgets.QRadioButton(self.tab)
        self.nodeVoltRadio.setGeometry(QtCore.QRect(10, 690, 200, 30))
        self.nodeVoltRadio.setObjectName("nodeVoltRadio")
        self.branchCurrRadio = QtWidgets.QRadioButton(self.tab)
        self.branchCurrRadio.setGeometry(QtCore.QRect(340, 690, 200, 30))
        self.branchCurrRadio.setObjectName("branchCurrRadio")
        self.analysistab.addTab(self.tab, "")

        self.retranslateUi(Dialog)
        self.analysistab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.browse.setText(_translate("Dialog", "Browse Folder"))
        self.selectbtn.setText(_translate("Dialog", "Select"))
        self.groupBox_2.setTitle(_translate("Dialog", "Plots:"))
        self.groupBox_3.setTitle(_translate("Dialog", "Integrated MTMM-LFA"))
        self.Tractiveeffort.setText(_translate("Dialog", "Tractive effort"))
        self.label_5.setText(_translate("Dialog", "Y-axis"))
        self.Reactivepower.setText(_translate("Dialog", "Reactive power"))
        self.Activepower.setText(_translate("Dialog", "Active power"))
        self.Voltage.setText(_translate("Dialog", "Voltage"))
        self.Brakingeffort.setText(_translate("Dialog", "Braking effort"))
        self.velocity.setText(_translate("Dialog", "Velocity"))
        self.Current.setText(_translate("Dialog", "Current"))
        self.label_7.setText(_translate("Dialog", "X-axis"))
        self.mergeplotbtn.setText(_translate("Dialog", "Merge"))
        self.subplotbtn.setText(_translate("Dialog", "Sub Plot"))
        self.plotbtn.setText(_translate("Dialog", "Plot"))
        self.Trainplots.setText(_translate("Dialog", "Train Plots"))
        self.Time_radio.setText(_translate("Dialog", "Time"))
        self.Distance_radio.setText(_translate("Dialog", "Distance"))
        self.groupBox.setTitle(_translate("Dialog", "Default plots/Data:"))
        self.Stringline.setText(_translate("Dialog", "String line diagram"))
        self.trainStat.setText(_translate("Dialog", "Show Train Statistics"))
        self.reportGenerate.setText(_translate("Dialog", "Generate Report"))
        self.showTimeTable.setText(_translate("Dialog", "Show Time Table"))
        self.stringlineplot.setText(_translate("Dialog", "Plot"))
        self.Routealtitude.setText(_translate("Dialog", "Route altitude"))
        self.Trainplots1.setText(_translate("Dialog", "Train Plots"))
        self.Substationplots.setText(_translate("Dialog", "Substation Plots"))
        self.IAButton.setText(_translate("Dialog", "Interference Analysis"))
        self.TAButton.setText(_translate("Dialog", "Temperature Analysis"))
        self.lfaradio.setText(_translate("Dialog", "Load Flow Analysis"))
        self.scaradio.setText(_translate("Dialog", "Short Circuit Analysis"))
        self.pqaradio.setText(_translate("Dialog", "Power Quality Analysis"))
        self.lfaselect.setText(_translate("Dialog", "Select"))
        self.pqa_sca_select.setText(_translate("Dialog", "Select"))
        self.ia_select.setText(_translate("Dialog", "Select"))
        self.pltlfa_pqa_sca.setText(_translate("Dialog", "Single plot"))
        self.subpltlfa_pqa_sca.setText(_translate("Dialog", "Subplot"))
        self.mergepltlfa_pqa_sca.setText(_translate("Dialog", "Merge"))
        self.timeoptions.setItemText(0, _translate("Dialog", "Time Interval"))
        self.selectAllTime.setText(_translate("Dialog", "Select All"))
        self.frequencyoptions.setItemText(0, _translate("Dialog", "Frequency"))
        self.selectAllFrequency.setText(_translate("Dialog", "Select All"))
        self.time_2d.setText(_translate("Dialog", "2D"))
        self.time_3d.setText(_translate("Dialog", "3D"))
        self.frequency_2d.setText(_translate("Dialog", "2D"))
        self.frequency_3d.setText(_translate("Dialog", "3D"))
        self.nodeVoltRadio.setText(_translate("Dialog", "Node Voltage"))
        self.branchCurrRadio.setText(_translate("Dialog", "Branch Current"))
        self.analysistab.setTabText(self.analysistab.indexOf(self.tab), _translate("Dialog", "Tab 1"))
