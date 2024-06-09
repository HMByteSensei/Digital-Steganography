from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabBar, QStackedWidget
from Video.Video_Embedding_GUI import Video_Embedding_GUI
from Video.Video_Extract_GUI import Video_Extract_GUI

class Video_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Steganography Tool')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Tab bar with mod options
        self.tab_bar = QTabBar()
        self.tab_bar.addTab("Embedding")
        self.tab_bar.addTab("Extract")
        self.tab_bar.currentChanged.connect(self.changeMod)
        layout.addWidget(self.tab_bar)

        # Central widget for mod content
        self.central_widget = QStackedWidget()
        layout.addWidget(self.central_widget)

        # Add embedding GUI to central widget
        self.embedding_gui = Video_Embedding_GUI()
        self.central_widget.addWidget(self.embedding_gui)

        # Add extract GUI to central widget
        self.extract_gui = Video_Extract_GUI()
        self.central_widget.addWidget(self.extract_gui)

        self.setLayout(layout)

    def changeMod(self, index):
        self.central_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication([])
    video_gui = Video_GUI()
    video_gui.show()
    app.exec_()
