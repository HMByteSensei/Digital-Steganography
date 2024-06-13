from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QWidget
import subprocess, os
class MyApplication(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Choose Steganography Technique')
        layout = QGridLayout()

        button1 = QPushButton('Text', self)
        button2 = QPushButton('Image', self)
        button3 = QPushButton('Audio', self)
        button4 = QPushButton('Video', self)

        button1.setSizePolicy(QPushButton().sizePolicy().horizontalPolicy(), QPushButton().sizePolicy().verticalPolicy())
        button2.setSizePolicy(QPushButton().sizePolicy().horizontalPolicy(), QPushButton().sizePolicy().verticalPolicy())
        button3.setSizePolicy(QPushButton().sizePolicy().horizontalPolicy(), QPushButton().sizePolicy().verticalPolicy())
        button4.setSizePolicy(QPushButton().sizePolicy().horizontalPolicy(), QPushButton().sizePolicy().verticalPolicy())
        button1.setMinimumSize(100, 50)
        button2.setMinimumSize(100, 50)
        button3.setMinimumSize(100, 50)
        button4.setMinimumSize(100, 50)
        button1.clicked.connect(lambda: self.runScript('Text/MainWindow.py'))
        button2.clicked.connect(lambda: self.runScript('Image/MainWindow.py'))
        button3.clicked.connect(lambda: self.runAudioScript('Audio/AudioGUI.py'))
        button4.clicked.connect(lambda: self.runScript('Video/VideoGUI.py'))
        # Audio_GUI()
        layout.addWidget(button1, 0, 0)
        layout.addWidget(button2, 0, 1)
        layout.addWidget(button3, 1, 0)
        layout.addWidget(button4, 1, 1)

        self.setLayout(layout)

    def runScript(self, script_name):
        try:
            subprocess.Popen(['python', script_name])
        except Exception as e:
            print(f"Error running script: {e}")

    def runAudioScript(self, script_name):
        try:
            audio_directory = os.path.dirname(script_name)
            subprocess.Popen(['python', os.path.basename(script_name)], cwd=audio_directory)
        except Exception as e:
            print(f"Error running audio script: {e}")

if __name__ == '__main__':
    app = QApplication([])
    window = MyApplication()
    window.setFixedWidth(500)
    window.setFixedHeight(200)
    window.show()
    app.exec_()
