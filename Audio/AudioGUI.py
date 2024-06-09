from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabBar, QStackedWidget
from Audio.Audio_Embedding_GUI import Audio_Embedding_GUI
from Audio.Audio_ExtractDetect_GUI import AudioExtractDetectGUI

class Audio_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Steganography Tool')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Tab bar with mod options
        self.tab_bar = QTabBar()
        self.tab_bar.addTab("Text")
        self.tab_bar.addTab("Image")
        audio_index = self.tab_bar.addTab("Audio")
        self.tab_bar.addTab("Video")
        self.tab_bar.currentChanged.connect(self.changeMod)
        self.tab_bar.setCurrentIndex(audio_index)
        layout.addWidget(self.tab_bar)

        # Tab bar with mod options
        self.tab_bar = QTabBar()
        self.tab_bar.addTab("Embedding")
        self.tab_bar.addTab("Extract & Detect")
        layout.addWidget(self.tab_bar)

        # Central widget for mod content
        self.central_widget = QStackedWidget()
        layout.addWidget(self.central_widget)

        # Add embedding GUI to central widget
        self.embedding_gui = Audio_Embedding_GUI()
        self.central_widget.addWidget(self.embedding_gui)

        # Add extract and detect GUI to central widget
        self.extract_detect_gui = AudioExtractDetectGUI()
        self.central_widget.addWidget(self.extract_detect_gui)

        self.tab_bar.currentChanged.connect(self.changeMod)

        self.setLayout(layout)

    def changeMod(self, index):
        self.central_widget.setCurrentIndex(index)

    def switchToEmbedding(self):
        self.tab_bar.setCurrentIndex(0)

    def switchToExtractDetect(self):
        self.tab_bar.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication([])
    audio_gui = Audio_GUI()
    audio_gui.show()
    app.exec_()