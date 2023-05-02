import sys
from file_utils import read_file_and_split, count_tokens
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Summarization')

        layout = QVBoxLayout()

        self.file_path_label = QLabel('No file selected')
        layout.addWidget(self.file_path_label)

        self.browse_button = QPushButton('Browse...')
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.setLayout(layout)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select file", "", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt);;DOCX Files (*.docx);;EPUB Files (*.epub)", options=options)
        if file_name:
            self.file_path_label.setText(file_name)
            chunks = read_file_and_split(file_name)
            print(f"File split into {len(chunks)} chunks")



def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
