from PyQt5.QtWidgets import QDialog, QMessageBox
from Image.ImageSteganography import imageSteganography
from PyQt5 import QtCore, QtWidgets
import os
from ImageGUI import Ui_Dialog
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
        self.ui.comboBox.currentIndexChanged.connect(self.handle_combo_change)

    def handle_combo_change(self, index):
        if index == 1:  # if "DCT" is selected
            # remove the label and line edit if "DCT" is not selected
            if hasattr(self, 'dct_number_label'):
                self.dct_number_label.hide()
            if hasattr(self, 'dct_number_spinbox'):
                self.dct_number_spinbox.hide()

            self.dct_number_label = QtWidgets.QLabel(Dialog)
            self.dct_number_label.setGeometry(QtCore.QRect(20, 150, 131, 22))
            self.dct_number_label.setObjectName("dct_number_label")
            self.dct_number_label.setText("Enter DCT Number:")
            self.dct_number_label.show()

            self.dct_number_spinbox = QtWidgets.QSpinBox(Dialog)
            self.dct_number_spinbox.setGeometry(QtCore.QRect(170, 150, 131, 22))
            self.dct_number_spinbox.setObjectName("dct_number_spinbox")
            self.dct_number_spinbox.setMaximum(9999)  # Set maximum value as required
            self.dct_number_spinbox.move(20, 180)
            self.dct_number_spinbox.show()
        else:
            # remove the label and spin box if "DCT" is not selected
            if hasattr(self, 'dct_number_label'):
                self.dct_number_label.hide()
            if hasattr(self, 'dct_number_spinbox'):
                self.dct_number_spinbox.hide()

    def browsefiles(self):
        try:
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.jfif)')
            if fname:
                self.ui.filename.setText(fname)
                directory = os.path.dirname(fname)
                base_name = QtCore.QFileInfo(fname).completeBaseName()
                extension = os.path.splitext(fname)[1]
                new_name = f"{base_name}Result{extension}"
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
            combo = "LSB"
            dct_number = -1
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

            if self.ui.comboBox.currentIndex() != -1:
                combo = self.ui.comboBox.currentText()
                if combo == "DCT":
                    combo = "DCT"
                    if hasattr(self, 'dct_number_spinbox'):
                        dct_number = self.dct_number_spinbox.value()
                else:
                    combo = "LSB"

            # print (combo)
            my = imageSteganography()
            print("DCT num: " + str(dct_number) +"\ttext len: " + str(len(self.ui.textEdit.toPlainText())))
            # print(self.ui.filename.text() + " " + self.ui.textEdit.toPlainText() + " " + combo + " " + str(encRadio) + " " + str(stegRadio))
            stegRadio = not stegRadio
            if dct_number == -1 or combo == "LSB":
                if my.engine(self.ui.filename.text(), self.ui.textEdit.toPlainText(), combo, encRadio, stegRadio) is True:
                    self.showMessageBox("Information", "Operation was successful!")
            else:
                if my.engine(self.ui.filename.text(), self.ui.textEdit.toPlainText(), combo, encRadio, stegRadio, dct_number) is True:
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