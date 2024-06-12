import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, \
    QLineEdit, QSpacerItem, QSizePolicy, QFrame, QTabBar, QCheckBox, QComboBox, QStackedWidget

from Audio.AudioSteganographyDCT import dct_extract
from Audio.AudioSteganographyDFT import dft_extract
from Audio.AudioSteganographyDetection import load_audio, extract_author_code, compare_codes
from Cryptography.TextCrypto import TextTransformer


class AudioExtractDetectGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.text_crypto = TextTransformer()

    def initUI(self):
        self.setWindowTitle('Steganography Tool')
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)  # Disable resizing

        layout = QVBoxLayout()

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Upload section
        upload_layout1 = QHBoxLayout()
        self.upload_btn1 = QPushButton('Upload Audio File')
        self.upload_btn1.clicked.connect(self.uploadFile1)
        self.upload_btn1.setFixedSize(150, 30)
        self.upload_btn1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        upload_layout1.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        upload_layout1.addWidget(self.upload_btn1)
        upload_layout1.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.file_label1 = QLabel('')
        upload_layout1.addWidget(self.file_label1)
        layout.addLayout(upload_layout1)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Extraction method selection
        method_layout = QHBoxLayout()
        self.method_label = QLabel('Extraction Method:')
        self.method_combo = QComboBox()
        self.method_combo.addItems(['LSB', 'DCT', 'DFT'])
        self.method_label.setFixedSize(100, 30)
        self.method_combo.setFixedSize(150, 30)
        method_layout.addWidget(self.method_label)
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Input section for message length
        length_layout = QHBoxLayout()
        self.length_label = QLabel('Enter Message Length:')
        self.length_input = QLineEdit()
        length_layout.addWidget(self.length_label)
        length_layout.addWidget(self.length_input)
        layout.addLayout(length_layout)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Encryption checkbox
        self.encrypt_checkbox1 = QCheckBox('Enable Encryption')
        self.encrypt_checkbox1.setChecked(False)  # By default, encryption is disabled
        self.encrypt_checkbox1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        encrypt_layout = QHBoxLayout()
        encrypt_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        encrypt_layout.addWidget(self.encrypt_checkbox1)
        encrypt_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(encrypt_layout)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Extraction section
        extract_layout = QHBoxLayout()
        self.extract_btn = QPushButton('Extract Secret Message')
        self.extract_btn.setFixedSize(250, 30)
        self.extract_btn.clicked.connect(self.extractMessage)
        extract_layout.addWidget(self.extract_btn)
        layout.addLayout(extract_layout)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Reset button for Extraction
        self.reset_extract_btn = QPushButton('Reset Extraction')
        self.reset_extract_btn.clicked.connect(self.resetExtraction)
        self.reset_extract_btn.setFixedSize(250, 30)
        layout.addWidget(self.reset_extract_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Extracted message display
        self.extracted_label = QLabel('Extracted message will appear here.')
        self.extracted_label.setWordWrap(True)  # Enable text wrapping
        layout.addWidget(self.extracted_label)

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

        # Upload section
        upload_layout2 = QHBoxLayout()
        self.upload_btn2 = QPushButton('Upload Audio File')
        self.upload_btn2.clicked.connect(self.uploadFile2)
        self.upload_btn2.setFixedSize(150, 30)
        self.upload_btn2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        upload_layout2.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        upload_layout2.addWidget(self.upload_btn2)
        upload_layout2.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.file_label2 = QLabel('')
        upload_layout2.addWidget(self.file_label2)
        layout.addLayout(upload_layout2)

        # Text field for secret word input
        self.secret_word_label = QLabel('Enter Secret Word:')
        layout.addWidget(self.secret_word_label)
        self.secret_word_input = QLineEdit()
        layout.addWidget(self.secret_word_input)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Encryption checkbox
        self.encrypt_checkbox2 = QCheckBox('Enable Encryption')
        self.encrypt_checkbox2.setChecked(False)  # By default, encryption is disabled
        self.encrypt_checkbox2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        encrypt_layout = QHBoxLayout()
        encrypt_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        encrypt_layout.addWidget(self.encrypt_checkbox2)
        encrypt_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(encrypt_layout)

        # Button for detection
        self.detect_btn = QPushButton('Detection')
        self.detect_btn.clicked.connect(self.detectSteganography)
        self.detect_btn.setFixedSize(250, 30)
        layout.addWidget(self.detect_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Reset button for detection
        self.reset_detect_btn = QPushButton('Reset Detection')
        self.reset_detect_btn.clicked.connect(self.resetDetection)
        self.reset_detect_btn.setFixedSize(250, 30)
        layout.addWidget(self.reset_detect_btn, alignment=Qt.AlignCenter)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Label for detection result
        self.detection_result_label = QLabel('Detection message will appear here.')
        self.detection_result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.detection_result_label)

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Button layout
        button_layout = QHBoxLayout()

        # Add spacer item for spacing
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

        # Horizontal line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Kreiranje QStackedWidget-a
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

        # Add button layout to main layout
        layout.addLayout(button_layout)

    def resetExtraction(self):
        # Reset all fields and checkboxes related to extraction
        self.detection_result_label.setText('Extraction message will appear here.')
        self.encrypt_checkbox1.setChecked(False)
        self.length_input.clear()
    def resetDetection(self):
        # Reset all fields and checkboxes related to detection
        self.detection_result_label.setText('Detection message will appear here.')
        self.encrypt_checkbox2.setChecked(False)
        self.secret_word_input.clear()

    def changeMod(self, index):
        mod = self.tab_bar.tabText(index)
        print(f"Switched to {mod} mod")

    def uploadFile1(self):
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
            if fileName:
                self.input_file = fileName
                self.file_label1.setText(fileName)
                print(f'Uploaded file: {self.input_file}')
        except Exception as e:
            print(f"Error during file upload: {e}")

    def uploadFile2(self):
        try:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
            if fileName:
                self.input_file = fileName
                self.file_label2.setText(fileName)
                print(f'Uploaded file: {self.input_file}')
        except Exception as e:
            print(f"Error during file upload: {e}")

    def extractMessage(self):
        try:
            if not hasattr(self, 'input_file'):
                print("No audio file uploaded")
                self.extracted_label.setText("No audio file uploaded")
                return

            if not self.length_input.text():
                print("Message length not provided")
                self.extracted_label.setText("Message length not provided")
                return

            try:
                length = int(self.length_input.text())
            except ValueError:
                print("Invalid message length")
                self.extracted_label.setText("Invalid message length")
                return

            samples, sample_rate = load_audio(self.input_file)

            method = self.method_combo.currentText()
            if method == 'LSB':
                extracted_code = extract_author_code(samples, length)
            elif method == 'DCT':
                extracted_code = dct_extract(samples, length)
            elif method == 'DFT':
                extracted_code = dft_extract(samples, length)
            else:
                print("Invalid extraction method")
                self.extracted_label.setText("Invalid extraction method")
                return

            if self.encrypt_checkbox1.isChecked():
                extracted_code = self.text_crypto.txt_decrypt(extracted_code)

            self.extracted_label.setText(f'Extracted Message: {extracted_code}')
            print(f'Extracted Message: {extracted_code}')
        except Exception as e:
            print(f"Error during message extraction: {e}")
            self.extracted_label.setText(f"Error during message extraction: {e}")

    def extractMethod(self, length):
        samples, sample_rate = load_audio(self.input_file)

        method = self.method_combo.currentText()
        if method == 'LSB':
            extracted_code = extract_author_code(samples, length)
        elif method == 'DCT':
            extracted_code = dct_extract(samples, length)
        elif method == 'DFT':
            extracted_code = dft_extract(samples, length)
        else:
            print("Invalid extraction method")
            self.detection_result_label.setText("Invalid extraction method")
            return None  # Return None if the extraction method is invalid
        return extracted_code  # Return the extracted code

    def detectSteganography(self):
        if not hasattr(self, 'input_file'):
            print("No audio file uploaded")
            return

        if not self.secret_word_input.text():
            print("Secret word not provided")
            return

        try:
            original_code = self.secret_word_input.text()
            extracted_code = self.extractMethod(len(original_code))
            if self.encrypt_checkbox2.isChecked():
                extracted_code = self.text_crypto.txt_decrypt(extracted_code)

            # Perform steganography detection
            result = compare_codes(original_code, extracted_code)
            if result:
                self.detection_result_label.setText('Steganography detected!')
            else:
                self.detection_result_label.setText('No steganography detected.')

        except Exception as e:
            print(f"Error during steganography detection: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioExtractDetectGUI()
    ex.show()
    sys.exit(app.exec_())