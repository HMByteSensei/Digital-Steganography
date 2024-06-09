import os
import shutil

import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, \
    QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from VideoSteganographyLSB import lsb_embed, load_video, save_video

class Video_Embedding_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_file = ""
        self.output_file = ""
        self.position = 0
        self.playing = False

    def initUI(self):
        self.setWindowTitle('Video Steganography Tool')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Upload Button
        self.upload_btn = QPushButton('Upload Video File')
        self.upload_btn.clicked.connect(self.uploadFile)
        self.upload_btn.setFixedSize(250, 30)
        layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Secret Message Input
        self.secret_message_label = QLabel('Enter Secret Message:')
        self.secret_message_input = QLineEdit()
        layout.addWidget(self.secret_message_label)
        layout.addWidget(self.secret_message_input)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Transform Button
        self.transform_btn = QPushButton('Transform')
        self.transform_btn.clicked.connect(self.transformFile)
        self.transform_btn.setFixedSize(250, 30)
        layout.addWidget(self.transform_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Reset Button
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setFixedSize(250, 30)
        layout.addWidget(self.reset_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Output Video File Path
        self.output_label = QLabel('Output Video File:')
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_path)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Download Button
        self.download_btn = QPushButton('Download Video')
        self.download_btn.clicked.connect(self.downloadVideo)
        self.download_btn.setFixedSize(250, 30)
        layout.addWidget(self.download_btn, alignment=Qt.AlignCenter)

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

    def reset(self):
        self.input_file = ""
        self.output_file = ""
        self.output_path.clear()
        self.secret_message_input=""

    def uploadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Video Files (*.avi *.mp4);;All Files (*)", options=options)
        if fileName:
            self.input_file = fileName
            print(f'Uploaded file: {self.input_file}')

    def transformFile(self):
        if not self.input_file:
            print("No input file uploaded")
            return

        print("Transforming video...")

        # Load the video file
        frames = load_video(self.input_file)

        # Get the secret message from the input field
        secret_message = self.secret_message_input.text()

        # Embed the secret message
        modified_frames = lsb_embed(frames, secret_message)

        # Save the modified video file
        output_file_path = os.path.splitext(self.input_file)[0] + "_modified.avi"
        save_video(modified_frames, output_file_path, fps=30)

        # Update the output file path
        self.output_file = output_file_path
        self.output_path.setText(self.output_file)

        print(f'Transformed video saved as: {self.output_file}')

    def downloadVideo(self):
        if self.output_file:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.avi *.mp4)", options=options)
            if file_name:
                shutil.copyfile(self.output_file, file_name)
                print(f"Video saved as: {file_name}")
        else:
            print("No output video to save.")

if __name__ == '__main__':
    app = QApplication([])
    video_gui = Video_Embedding_GUI()
    video_gui.show()
    app.exec_()
