import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtGui import QPixmap
from similarity_score import SimilarityScore

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = ""
        self.similarity_score = SimilarityScore()

        # Create a textfield
        self.textfield = QTextEdit(self)
        self.textfield.setFixedSize(400, 400)

        # Create an image input field
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setScaledContents(True)
        self.image_button = QPushButton('Select Image', self)
        self.image_button.clicked.connect(self.select_image)

        # Create a button
        self.compere_button = QPushButton('Compare', self)
        self.compere_button.clicked.connect(self.compere)

        # Set up the layout
        layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textfield)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.image_button)
        h_layout.addLayout(v_layout)
        layout.addLayout(h_layout)
        layout.addWidget(self.compere_button)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.xpm *.jpg *.bmp);;All Files (*)', options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.image_path = file_name


    def compere(self):
        plain_text = self.textfield.toPlainText()
        if len(plain_text) > 0 and len(self.image_path) > 0:
            result = self.similarity_score.compare(self.image_path, plain_text)
            self.popUpEvent(result)

    def popUpEvent(self, score):
        QMessageBox.information(self, 'Result', 'The image-text pair similarity is '+str(score)+' %', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = App()
    widget.setWindowTitle("Image-Text Similarity")
    widget.show()
    sys.exit(app.exec_())
