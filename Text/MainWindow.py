from PyQt5 import QtCore
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from Text.TextSteganography import textSteganography
from TextGUI import Ui_Dialog

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
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'Text Files (*.txt)')
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
            combo = "markingLetters"
            if not self.ui.filename.text():
                print("No file selected.")
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
                if combo == "Uppercase Letters in Binary":
                    combo = "uppercaseBinaryLetters"
                elif combo == "Uppercase Letters":
                    combo = "uppercaseLetters"
                else:
                    combo = "markingLetters"

            my = textSteganography()
            # print(self.ui.filename.text() + " " + self.ui.textEdit.toPlainText() + " " + combo + " " + str(encRadio) + " " + str(stegRadio))
            stegRadio = not stegRadio
            if not my.engine(str(self.ui.filename.text()), str(self.ui.textEdit.toPlainText()), combo, encRadio, stegRadio):
                self.showMessageBox("Error", "There is a problem with your secret text. Most likely it is too long or contains letters that cover text does not have.")
            else:
                self.showMessageBox("Information","Operation was successful!")
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