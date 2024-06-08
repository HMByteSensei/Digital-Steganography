from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from Image.imageSteganography import imageSteganography


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(521, 446)
        self.filename = QtWidgets.QLineEdit(Dialog)
        self.filename.setEnabled(False)
        self.filename.setGeometry(QtCore.QRect(20, 50, 321, 20))
        self.filename.setObjectName("filename")
        self.searchFile = QtWidgets.QPushButton(Dialog)
        self.searchFile.setGeometry(QtCore.QRect(360, 50, 141, 23))
        self.searchFile.setObjectName("searchFile")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 110, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.outputFileLabel = QtWidgets.QLabel(Dialog)
        self.outputFileLabel.setGeometry(QtCore.QRect(30, 230, 461, 21))
        self.outputFileLabel.setObjectName("outputFileLabel")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 109, 141, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.encryptionTrue = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.encryptionTrue.setObjectName("encryptionTrue")
        self.verticalLayout.addWidget(self.encryptionTrue)
        self.encryptionFalse = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.encryptionFalse.setObjectName("encryptionFalse")
        self.verticalLayout.addWidget(self.encryptionFalse)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(350, 110, 160, 81))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.stegTrue = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.stegTrue.setObjectName("stegTrue")
        self.verticalLayout_2.addWidget(self.stegTrue)
        self.stegFalse = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
        self.stegFalse.setObjectName("stegFalse")
        self.verticalLayout_2.addWidget(self.stegFalse)
        self.encryptionFalse.setChecked(True)
        self.stegTrue.setChecked(True)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(430, 400, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(20, 270, 491, 121))
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.searchFile.setText(_translate("Dialog", "Search"))
        self.comboBox.setItemText(0, _translate("Dialog", "LSB"))
        self.outputFileLabel.setText(_translate("Dialog", "OutputFile.txt"))
        self.label_2.setText(_translate("Dialog", "Encryption"))
        self.encryptionTrue.setText(_translate("Dialog", "True"))
        self.encryptionFalse.setText(_translate("Dialog", "False"))
        self.label_3.setText(_translate("Dialog", "Steganography"))
        self.stegTrue.setText(_translate("Dialog", "True"))
        self.stegFalse.setText(_translate("Dialog", "False"))
        self.pushButton.setText(_translate("Dialog", "Done"))

class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.searchFile.clicked.connect(self.browsefiles)
        self.ui.encryptionTrue.toggled.connect(self.handleRadioButton)
        self.ui.encryptionFalse.toggled.connect(self.handleRadioButton)
        self.ui.stegTrue.toggled.connect(self.handleRadioButton)
        self.ui.stegFalse.toggled.connect(self.handleRadioButton)
        self.ui.comboBox.currentIndexChanged.connect(self.handleComboBox)
        self.ui.pushButton.clicked.connect(self.handleButtonClick)

    def browsefiles(self):
        try:
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)')
            if fname:
                self.ui.filename.setText(fname)
                directory = os.path.dirname(fname)
                base_name = QtCore.QFileInfo(fname).completeBaseName()
                extension = QtCore.QFileInfo(fname).suffix()
                new_name = f"{base_name}Result.{extension}"
                full_path = os.path.join(directory, new_name).replace("\\", "/")
                self.ui.outputFileLabel.setText(full_path)
                print(full_path)
            else:
                print("No file selected.")
        except Exception as e:
            print(f"Error while selecting file: {e}")

    def handleRadioButton(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print(f"Selected Radio Button: {radioButton.text()}")

    def handleComboBox(self):
        comboBox = self.sender()
        currentText = comboBox.currentText()

    def handleButtonClick(self):
        try:
            encRadio = False
            stegRadio = True
            if not self.ui.filename.text():
                self.showMessageBox("Error", "No file selected.")
                return

            if self.ui.encryptionTrue.isChecked():
                encRadio = True
            elif self.ui.encryptionFalse.isChecked():
                encRadio = False

            if self.ui.stegTrue.isChecked():
                stegRadio = True
            elif self.ui.stegFalse.isChecked():
                stegRadio = False

            my = imageSteganography()
            # print(self.ui.filename.text() + " " + self.ui.textEdit.toPlainText() + " " + combo + " " + str(encRadio) + " " + str(stegRadio))
            stegRadio = not stegRadio
            if my.engine(self.ui.filename.text(), self.ui.textEdit.toPlainText(), encRadio, stegRadio) is True:
                self.showMessageBox("Information", "Operation was successful!")
        except Exception as e:
            print(f"Error in handleButtonClick: {e}")

    def showMessageBox(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = MainWindow()
    Dialog.setFixedWidth(520)
    Dialog.setFixedHeight(440)
    Dialog.show()
    sys.exit(app.exec_())
