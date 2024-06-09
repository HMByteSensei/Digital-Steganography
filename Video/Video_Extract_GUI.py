import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, \
    QSpacerItem, QFrame, QSizePolicy
from VideoSteganographyLSB import lsb_embed, load_video, save_video, lsb_extract

class Video_Extract_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video_file = ""
        self.extracted_message = ""

    def initUI(self):
        self.setWindowTitle('Video Secret Message Extractor')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Upload Button
        self.upload_btn = QPushButton('Upload Video File')
        self.upload_btn.clicked.connect(self.uploadFile)
        self.upload_btn.setFixedSize(250, 30)
        layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # Extract Button
        self.extract_btn = QPushButton('Extract Secret Message')
        self.extract_btn.clicked.connect(self.extractMessage)
        self.extract_btn.setFixedSize(250, 30)
        layout.addWidget(self.extract_btn, alignment=Qt.AlignCenter)

        # Secret Message Label
        self.message_label = QLabel('Secret Message:')
        layout.addWidget(self.message_label)

        # Secret Message Output Field
        self.message_output = QLineEdit()
        self.message_output.setReadOnly(True)
        layout.addWidget(self.message_output)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Horizontal line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        self.setLayout(layout)

    def uploadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Video Files (*.avi *.mp4);;All Files (*)", options=options)
        if fileName:
            self.video_file = fileName
            print(f'Uploaded file: {self.video_file}')

    def extractMessage(self):
        if not self.video_file:
            print("No video file uploaded")
            return

        frames = load_video(self.video_file)
        self.extracted_message = lsb_extract(frames)
        print("Extracted message:", self.extracted_message)
        self.message_output.setText(self.extracted_message)


if __name__ == '__main__':
    app = QApplication([])
    extract_gui = Video_Extract_GUI()
    extract_gui.show()
    app.exec_()