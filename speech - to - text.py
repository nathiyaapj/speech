import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QComboBox, QHBoxLayout, QMessageBox, QApplication

import speech_recognition as sr
from PyQt5.QtGui import QClipboard

class SpeechToTextApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Speech to Text')
        self.setGeometry(100, 100, 400, 250)

        self.file_path_label = QLabel('Select an audio file:')
        self.transcription_label = QLabel('Transcription will be shown here.')
        self.language_label = QLabel('Select language:')
        self.language_combobox = QComboBox()
        self.language_combobox.addItems(['English', 'Tamil', 'Hindi'])

        self.select_file_button = QPushButton('Select File')
        self.select_file_button.clicked.connect(self.select_file)

        self.transcribe_button = QPushButton('Transcribe')
        self.transcribe_button.clicked.connect(self.transcribe_audio)

        self.copy_button = QPushButton('Copy')
        self.copy_button.clicked.connect(self.copy_text)
        self.copy_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.file_path_label)
        layout.addWidget(self.select_file_button)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combobox)
        layout.addWidget(self.transcription_label)
        layout.addWidget(self.transcribe_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.copy_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Audio File', '', 'Audio Files (*.wav *.mp3)')
        if file_path:
            self.file_path_label.setText(file_path)

    def transcribe_audio(self):
        file_path = self.file_path_label.text()
        if file_path:
            try:
                r = sr.Recognizer()
                with sr.AudioFile(file_path) as source:
                    audio_data = r.record(source)
                    selected_language = self.language_combobox.currentText()
                    if selected_language == 'English':
                        text = r.recognize_google(audio_data, language="en-US")
                    elif selected_language == 'Tamil':
                        text = r.recognize_google(audio_data, language="ta-IN")
                    elif selected_language == 'Hindi':
                        text = r.recognize_google(audio_data, language="hi-IN")
                    self.transcription_label.setText(text)
                    self.copy_button.setEnabled(True)
            except Exception as e:
                self.transcription_label.setText('Error: ' + str(e))
                self.copy_button.setEnabled(False)
        else:
            self.transcription_label.setText('Please select an audio file.')
            self.copy_button.setEnabled(False)

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.transcription_label.text())
        QMessageBox.information(self, 'Copied', 'Text copied to clipboard.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec_())
