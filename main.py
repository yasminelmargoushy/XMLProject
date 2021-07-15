# IMPORT PYQT5 CLASSES:
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

# IMPORTS FUNCTIONS FROM FILES:
from Consistency_Formatting import Formatting,ErrorDetection,Parsing,is_consistent,ErrorCorrection
from JSONConversion_Minifying import PrintJSONFile, PrintMinifiedFile
from Compression import PrintCompressedFile, PrintDecompressedFile, Node


# GLOBAL VARIABLES:
Input_String = ""
Output_String = ""
Output_Type = ""
Input_Type = ""
File_Path = ""
File_Name = ""
Tree = ""

# GUI CLASS:
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1540, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Browse Button
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(1170, 10, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.browse.setFont(font)
        self.browse.setObjectName("browse")

        # Input Scroll Area
        self.input = QtWidgets.QScrollArea(self.centralwidget)
        self.input.setGeometry(QtCore.QRect(30, 100, 631, 701))
        self.input.setWidgetResizable(True)
        self.input.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.input.setObjectName("input")
        self.input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(20, 0, 629, 699))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        # Input Label
        self.input_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.input_lbl.setGeometry(QtCore.QRect(30, 10, 611, 681))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.input_lbl.setFont(font)
        self.input_lbl.setText("")
        self.input_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.input_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.input_lbl.setObjectName("input_lbl")
        self.verticalLayout.addWidget(self.input_lbl)
        self.input.setWidget(self.scrollAreaWidgetContents)

        # Output Scroll Area
        self.output = QtWidgets.QScrollArea(self.centralwidget)
        self.output.setGeometry(QtCore.QRect(690, 100, 631, 701))
        self.output.setWidgetResizable(True)
        self.output.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.output.setObjectName("output")
        self.output.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 629, 699))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Output Label
        self.output_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.output_lbl.setGeometry(QtCore.QRect(10, 10, 611, 681))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.output_lbl.setFont(font)
        self.output_lbl.setText("")
        self.output_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.output_lbl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.output_lbl.setObjectName("output_lbl")
        self.verticalLayout_2.addWidget(self.output_lbl)
        self.output.setWidget(self.scrollAreaWidgetContents_2)

        # Browse Line Edit
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 10, 1131, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        # Consistancy Button
        self.Consistant = QtWidgets.QPushButton(self.centralwidget)
        self.Consistant.setGeometry(QtCore.QRect(1340, 100, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Consistant.setFont(font)
        self.Consistant.setObjectName("Consistant")

        # Error Detection Button
        self.ErrorDetect = QtWidgets.QPushButton(self.centralwidget)
        self.ErrorDetect.setGeometry(QtCore.QRect(1340, 175, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.ErrorDetect.setFont(font)
        self.ErrorDetect.setObjectName("ErrorDetect")

        # Error Correction Button
        self.ErrorCorrection = QtWidgets.QPushButton(self.centralwidget)
        self.ErrorCorrection.setGeometry(QtCore.QRect(1340, 250, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.ErrorCorrection.setFont(font)
        self.ErrorCorrection.setObjectName("ErrorCorrection")

        # Formating Button
        self.Formatting = QtWidgets.QPushButton(self.centralwidget)
        self.Formatting.setGeometry(QtCore.QRect(1340, 325, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Formatting.setFont(font)
        self.Formatting.setObjectName("Formatting")

        # JSON Conversion Button
        self.JsonConversion = QtWidgets.QPushButton(self.centralwidget)
        self.JsonConversion.setGeometry(QtCore.QRect(1340, 400, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.JsonConversion.setFont(font)
        self.JsonConversion.setObjectName("JsonConversion")

        # Minify Button
        self.Minify = QtWidgets.QPushButton(self.centralwidget)
        self.Minify.setGeometry(QtCore.QRect(1340, 475, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Minify.setFont(font)
        self.Minify.setObjectName("Minify")

        # Compress Button
        self.Compress = QtWidgets.QPushButton(self.centralwidget)
        self.Compress.setGeometry(QtCore.QRect(1340, 550, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Compress.setFont(font)
        self.Compress.setObjectName("Compress")

        # Decompress Button
        self.Decompress = QtWidgets.QPushButton(self.centralwidget)
        self.Decompress.setGeometry(QtCore.QRect(1340, 625, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Decompress.setFont(font)
        self.Decompress.setObjectName("Decompress")

        # Label Pointing to Input
        self.InputPointing_lbl = QtWidgets.QLabel(self.centralwidget)
        self.InputPointing_lbl.setGeometry(QtCore.QRect(10, 810, 621, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.InputPointing_lbl.setFont(font)
        self.InputPointing_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.InputPointing_lbl.setObjectName("InputPointing_lbl")

        # Label Pointing to Output
        self.OutputPointing_lbl = QtWidgets.QLabel(self.centralwidget)
        self.OutputPointing_lbl.setGeometry(QtCore.QRect(680, 810, 631, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.OutputPointing_lbl.setFont(font)
        self.OutputPointing_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.OutputPointing_lbl.setObjectName("OutputPointing_lbl")

        # Save Button
        self.Save = QtWidgets.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(1340, 740, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Save.setFont(font)
        self.Save.setObjectName("Save")

        # Switch Button
        self.Switch = QtWidgets.QPushButton(self.centralwidget)
        self.Switch.setGeometry(QtCore.QRect(600, 810, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.Switch.setFont(font)
        self.Switch.setObjectName("Switch")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1549, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browse.setText(_translate("MainWindow", "Browse"))
        self.Consistant.setText(_translate("MainWindow", "Is Consistant?"))
        self.ErrorDetect.setText(_translate("MainWindow", "Detect Error"))
        self.ErrorCorrection.setText(_translate("MainWindow", "Error Correction"))
        self.JsonConversion.setText(_translate("MainWindow", "JSON"))
        self.Minify.setText(_translate("MainWindow", "Minify"))
        self.Compress.setText(_translate("MainWindow", "Compress & Save"))
        self.Decompress.setText(_translate("MainWindow", "Decompress"))
        self.Formatting.setText(_translate("MainWindow", "Formatting"))
        self.InputPointing_lbl.setText(_translate("MainWindow", "Input"))
        self.OutputPointing_lbl.setText(_translate("MainWindow", "Output"))
        self.Save.setText(_translate("MainWindow", "Save"))
        self.Switch.setText(_translate("MainWindow", "<<<<"))
        self.browse.clicked.connect(self.browse_handler)
        self.Consistant.clicked.connect(self.consistant_handler)
        self.ErrorDetect.clicked.connect(self.errordetect_handler)
        self.ErrorCorrection.clicked.connect(self.errorcorrection_handler)
        self.Formatting.clicked.connect(self.formatting_handler)
        self.JsonConversion.clicked.connect(self.json_handler)
        self.Minify.clicked.connect(self.minify_handler)
        self.Compress.clicked.connect(self.compress_handler)
        self.Decompress.clicked.connect(self.decompress_handler)
        self.Save.clicked.connect(self.save_handler)
        self.Switch.clicked.connect(self.switch_handler)

    def consistant_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            tag = Parsing(Input_String)
            output = is_consistent(tag)
            if output:
                # Message Box
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information")
                msg.setInformativeText("XML is Consistent")
                msg.setWindowTitle("Information")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            else:
                # Message Box
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("XML isn't Consistent")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def errordetect_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output = ErrorDetection(Input_String)
            if Output != "NO Error":
                # Message Box
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText(Output)
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            else:
                # Message Box
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information")
                msg.setInformativeText("XML Has No Error")
                msg.setWindowTitle("Information")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def errorcorrection_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output = ErrorCorrection(Input_String)
            if Output != "sorry can`t be corrected":
                Output_String = Output
                self.input_lbl.setText(Output_String)
            else:
                # Message Box
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error Couldn't be Corrected")
                msg.setInformativeText(Output)
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def formatting_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output_Type = "formatted xml"
            Output_String = Formatting(Input_String)
            self.output_lbl.setText(Output_String)

    def json_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output_Type = "json"
            Output_String = PrintJSONFile(Input_String)
            self.output_lbl.setText(Output_String)

    def minify_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output_Type = "minified xml"
            Output_String = PrintMinifiedFile(Input_String)
            self.output_lbl.setText(Output_String)

    def compress_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        global Tree
        if Input_Type != "formatted xml" and Input_Type != "minified xml" and Input_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Output_Type = "compressed"
            Output = PrintCompressedFile(Input_String)
            Output_String = Output[0]
            Tree = Output[2]
            self.output_lbl.setText("Output Can't be viewed Here, as it's in byte Format.\n" + Output[1])
            self.save_handler()

    def decompress_handler(self):
        global File_Path
        global File_Name
        global Output_String
        global Output_Type
        global Input_Type
        global Tree
        if Input_Type != "compressed":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be huff")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            PrintDecompressedFile(f"{File_Path}{File_Name}", f"{File_Path}Decompressed_{File_Name}.xml", Tree)
            with open(f"{File_Path}Decompressed_{File_Name}.xml", "r") as f:
                Output_String = f.read()
                self.output_lbl.setText(Output_String)

    def save_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global File_Path
        global File_Name
        if Output_Type == "":
            file = open(f"{File_Path}{File_Name}Empty.txt", "w")
            file.write("")
            file.close()
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved")
            msg.setInformativeText(f"An Empty File Is Saved in '{File_Path}' \nIt's name is {File_Name}Empty.txt")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif Output_Type == "formatted xml":
            file = open(f"{File_Path}Formatted_{File_Name}.xml", "w")
            file.write(Output_String)
            file.close()
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved")
            msg.setInformativeText(f"The Formatted File is Saved in '{File_Path}' \nIt's Name is Formatted_{File_Name}.xml")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif Output_Type == "json":
            file = open(f"{File_Path}JSON_{File_Name}.json", "w")
            file.write(Output_String)
            file.close()
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved")
            msg.setInformativeText(f"The JSON File is Saved in '{File_Path}' \nIt's Name is JSON_{File_Name}.json")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif Output_Type == "minified xml":
            file = open(f"{File_Path}Minified_{File_Name}.xml", "w")
            file.write(Output_String)
            file.close()
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved")
            msg.setInformativeText(f"The Minified File is Saved in '{File_Path}' \nIt's Name is Minified_{File_Name}.xml")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif Output_Type == "compressed":
            with open(f"{File_Path}Compressed_{File_Name}.huff", "wb") as Out_File:
                Out_File.write(Output_String)
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Saved")
            msg.setInformativeText(f"The Compressed File is Saved in '{File_Path}' \nIt's Name is Compressed_{File_Name}.huff")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def switch_handler(self):
        global Input_String
        global Output_String
        global Output_Type
        global Input_Type
        if Output_Type != "formatted xml" and Output_Type  != "minified xml" and Output_Type != "xml":
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Wrong Format")
            msg.setInformativeText("The Format needs to be xml")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            Input_String = Output_String
            Input_Type = Output_Type
            self.input_lbl.setText(Input_String)
            self.output_lbl.setText("")

    def browse_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        global Input_String
        global Input_Type
        global File_Path
        global File_Name
        File_Path = ""
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.output_lbl.setText("")
        self.input_lbl.setText("")
        if path.split(".")[-1] == "xml":
            Input_Type = "xml"
            self.lineEdit.setText(path)
            with open(path, "r") as f:
                Input_String = f.read()
                self.input_lbl.setText(Input_String)
                Split_Path = path.split('/')
                File_Name = Split_Path[-1]
                for i in range(len(Split_Path) - 1):
                    File_Path = File_Path + Split_Path[i] + "/"
        elif path.split(".")[-1] == "huff":
            Input_Type = "compressed"
            self.lineEdit.setText(path)
            self.input_lbl.setText("Output Can't be viewed Here, as it's in byte Format.\n")
            Split_Path = path.split('/')
            File_Name = Split_Path[-1]
            for i in range(len(Split_Path) - 1):
                File_Path = File_Path + Split_Path[i] + "/"
        else:
            # Message Box
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Unknown File Type")
            msg.setInformativeText("Please Choose a .xml file or an .huff file")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return


# MAIN:
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
