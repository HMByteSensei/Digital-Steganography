import os
import sys
import numpy as np
import scipy.fftpack as fft
from scipy.io import wavfile
from pydub import AudioSegment
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, \
    QFileDialog, QLineEdit, QSpacerItem, QSizePolicy, QCheckBox, QToolBar, QStackedWidget, QTabBar, QFrame
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer
import pyqtgraph as pg
from Audio.AudioSteganographyLSB import lsb_embed
from Audio.AudioSteganographyDFT import dft_embed
from Audio.AudioSteganographyDCT import dct_embed
from Cryptography.TextCrypto import TextTransformer

class Audio_Embedding_GUI(QWidget):

    @staticmethod
    def lsb_embed(samples, sample_rate, secret_message):
        return lsb_embed(samples, sample_rate, secret_message)

    @staticmethod
    def dft_embed(samples, secret_message):
        return dft_embed(samples, secret_message)

    @staticmethod
    def dct_embed(samples, secret_message):
        return dct_embed(samples, secret_message)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_mod = "Audio"  # Default mod is "Audio"
        self.input_file = ""
        self.output_file = ""
        self.player = QMediaPlayer()
        self.timer = QTimer()
        self.timer.setInterval(100)  # Update every 100 ms
        self.timer.timeout.connect(self.update_plot)
        self.playing = False
        self.position = 0  # To store the current position when paused
        self.secret_message = "" # Add secret message
        self.text_crypto = TextTransformer()  # Add TextTransformer

    def initUI(self):
        self.setWindowTitle('Steganography Tool')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Central widget for mod content
        self.central_widget = QStackedWidget()
        layout.addWidget(self.central_widget)

        # Vertical layout for method selection and message input
        method_layout = QVBoxLayout()

        # Dropdown menu for selecting method
        self.method_label = QLabel('Select Method:')
        self.method_combo = QComboBox()
        self.method_combo.addItems(['LSB', 'DFT', 'DCT'])
        self.method_label.setFixedSize(100, 30)
        self.method_combo.setFixedSize(150, 30)
        method_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        method_layout.addWidget(self.method_label)
        method_layout.addWidget(self.method_combo)
        method_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Text input for secret message
        self.message_label = QLabel('Secret Message:')
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText('Enter your secret message here')  # Set placeholder text
        method_layout.addWidget(self.message_label)
        method_layout.addWidget(self.message_input)

        layout.addLayout(method_layout)

        # Checkbox for encryption
        self.encrypt_checkbox = QCheckBox('Enable Encryption')
        self.encrypt_checkbox.setChecked(False)  # By default, encryption is disabled

        # Reset button
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset)
        self.reset_btn.setFixedSize(100, 30)  # Set fixed size for the button

        # Checkbox for encryption
        self.encrypt_checkbox = QCheckBox('Enable Encryption')
        self.encrypt_checkbox.setChecked(False)  # By default, encryption is disabled

        reset_layout = QHBoxLayout()
        reset_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Add spacer to center align
        reset_layout.addWidget(self.reset_btn)
        reset_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding,
                        QSizePolicy.Minimum))  # Add spacer for space between button and checkbox
        reset_layout.addWidget(self.encrypt_checkbox)  # Add the checkbox to the layout
        reset_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Add spacer to center align
        layout.addLayout(reset_layout)

        # File upload button
        self.upload_btn = QPushButton('Upload Audio File')
        self.upload_btn.clicked.connect(self.uploadFile)
        self.upload_btn.setFixedSize(150, 30)  # Set fixed size for the button
        upload_layout = QHBoxLayout()
        upload_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Empty space with flexibile ordering
        upload_layout.addWidget(self.upload_btn)
        upload_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Empty space with flexibile ordering
        layout.addLayout(upload_layout)

        # Transform button
        self.transform_btn = QPushButton('Transform')
        self.transform_btn.clicked.connect(self.transformFile)
        self.transform_btn.setFixedSize(100, 30)  # Set fixed size for the button
        transform_layout = QHBoxLayout()
        transform_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Empty space with flexibile ordering
        transform_layout.addWidget(self.transform_btn)
        transform_layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Empty space with flexibile ordering
        layout.addLayout(transform_layout)

        # Output file section
        self.output_label = QLabel('Output Audio File:')
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        self.download_btn = QPushButton('Download')
        self.download_btn.clicked.connect(self.downloadFile)
        self.download_btn.setFixedSize(100, 30)  # Set fixed size for the button
        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.download_btn)
        layout.addLayout(output_layout)

        # Audio player controls
        self.play_pause_btn = QPushButton('Play')
        self.play_pause_btn.clicked.connect(self.playPauseFile)
        self.play_pause_btn.setFixedSize(100, 30)  # Set fixed size for the button
        player_layout = QHBoxLayout()
        player_layout.addWidget(self.play_pause_btn)
        layout.addLayout(player_layout)

        # Audio signal display
        self.plot_widget = pg.PlotWidget(title="Audio Signal")
        self.plot_widget.setFixedHeight(200)  # Set fixed height to make it smaller
        self.plot_data_item = self.plot_widget.plot()
        self.v_line = pg.InfiniteLine(angle=90, movable=False, pen='r')
        self.plot_widget.addItem(self.v_line)
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

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

    def changeMod(self, index):
        mod = self.tab_bar.tabText(index)
        if mod != self.current_mod:
            self.current_mod = mod
            print(f"Switched to {mod} mod")

    def reset(self):
        self.input_file = ""
        self.output_file = ""
        self.output_path.clear()
        self.plot_data_item.clear()
        self.play_pause_btn.setText('Play')
        self.position = 0
        self.playing = False
        self.player.stop()
        self.message_input.clear()  # Clear the secret message input field
        self.encrypt_checkbox.setChecked(False)  # Uncheck the encryption checkbox
        self.method_combo.setCurrentIndex(0)  # Reset the method combo box to the first item
        print("Application reset")

    def uploadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
        if fileName:
            self.input_file = fileName
            print(f'Uploaded file: {self.input_file}')
            # No need to display the audio signal for input file here
            # self.displayAudioSignal(self.input_file)

    def transformFile(self):
        method = self.method_combo.currentText()
        self.secret_message = self.message_input.text()

        if not self.secret_message:
            print("Please enter a secret message")
            return

        if not self.input_file:
            print("No input file uploaded")
            return

        print(f'Transforming file using {method} method')
        samples, sample_rate = self.load_audio(self.input_file)

        # Define the base directory
        base_directory = os.path.join(os.path.dirname(__file__), 'Generisani Audio File-ovi')

        # Ensure the base directory exists
        if not os.path.exists(base_directory):
            os.makedirs(base_directory)

        # Generate unique output file name based on the method
        base_output_file = f'{method.lower()}_audio_file.wav'
        output_file = os.path.join(base_directory, base_output_file)

        if self.encrypt_checkbox.isChecked():
            self.secret_message = self.text_crypto.txt_encrypt(self.secret_message)

        if method == 'LSB':
            modified_samples = self.lsb_embed(samples, sample_rate, self.secret_message)
        elif method == 'DFT':
            modified_samples = self.dft_embed(samples, self.secret_message)
        elif method == 'DCT':
            modified_samples = self.dct_embed(samples, self.secret_message)

        counter = 1
        while os.path.exists(output_file):
            output_file = os.path.join(base_directory, f'{os.path.splitext(base_output_file)[0]}_{counter}.wav')
            counter += 1

        self.output_file = output_file
        self.save_audio(modified_samples, sample_rate, self.output_file)
        self.output_path.setText(self.output_file)
        print(f'Transformed file saved as: {self.output_file}')
        self.displayAudioSignal(self.output_file)

    def downloadFile(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                   "Audio Files (*.wav);;All Files (*)", options=options)
        if save_path:
            if self.output_file:
                samples, sample_rate = self.load_audio(self.output_file)
                self.save_audio(samples, sample_rate, save_path)
                print(f'File saved to: {save_path}')

    def playPauseFile(self):
        if self.playing:
            self.position = self.player.position()
            self.player.pause()
            self.play_pause_btn.setText('Play')
            self.timer.stop()
        else:
            if self.output_file:
                if self.player.mediaStatus() != QMediaPlayer.NoMedia:
                    self.player.setPosition(self.position)
                    self.player.play()
                else:
                    url = QUrl.fromLocalFile(self.output_file)
                    content = QMediaContent(url)
                    self.player.setMedia(content)
                    self.player.setPosition(self.position)
                    self.player.play()
                self.play_pause_btn.setText('Pause')
                self.timer.start()
        self.playing = not self.playing

    def update_plot(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            position = self.player.position()  # Get current position in milliseconds
            self.v_line.setPos(position / 1000.0)  # Update the position of the vertical line
        else:
            self.timer.stop()

    def displayAudioSignal(self, file_path):
        samples, sample_rate = self.load_audio(file_path)
        time = np.linspace(0, len(samples) / sample_rate, num=len(samples))
        self.plot_data_item.setData(time, samples)
        print(f'Displaying audio signal for file: {file_path}')

    def load_audio(self, file_path):
        audio = AudioSegment.from_wav(file_path)
        audio = audio.set_channels(1)  # Convert to mono
        sample_rate = audio.frame_rate
        samples = np.array(audio.get_array_of_samples())
        print(f"Loaded audio file: {file_path}, Sampling rate: {sample_rate}, Number of samples: {len(samples)}")
        return samples, sample_rate

    def save_audio(self, samples, sample_rate, output_path):
        audio_segment = AudioSegment(
            samples.tobytes(),
            frame_rate=sample_rate,
            sample_width=samples.dtype.itemsize,
            channels=1
        )
        audio_segment.export(output_path, format="wav")
        print(f"Saved modified audio file: {output_path}")

    def string_to_binary(self, string):
        binary = ''.join(format(ord(char), '08b') for char in string)
        print(f"String to binary: '{string}' -> {binary}")
        return binary

    def binary_to_string(self, binary):
        if len(binary) % 8 != 0:
            raise ValueError("Length of binary string is not a multiple of 8")

        binary_values = [binary[i:i + 8] for i in range(0, len(binary), 8)]
        ascii_characters = [chr(int(binary_value, 2)) for binary_value in binary_values]
        result = ''.join(ascii_characters)
        print(f"Binary to string: {binary} -> '{result}'")
        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Audio_Embedding_GUI()
    ex.show()
    sys.exit(app.exec_())
