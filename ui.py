import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileDialog, QTextEdit, QMessageBox
from PyQt5.QtGui import QPixmap

import keras.models
from image_features import ImageEncoder
from text_features import TextEncoder
import numpy as np

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.image_path = ""

        self.text_enc = TextEncoder()
        self.image_enc = ImageEncoder()
        self.model = keras.models.load_model('similarity_model_2')


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
            print("Selected")

    def compere(self):
        plain_text = self.textfield.toPlainText()
        text = plain_text.replace('\n', ' ').replace('\r', '')
        if len(text) > 0 and len(self.image_path) > 0:

            text_features = np.array(self.text_enc.encode([text]))
            image_features = np.array(self.image_enc.encode([self.image_path]))
            score = self.model.predict([image_features[0].reshape(1,-1), text_features[0].reshape(1,-1)])
            self.popUpEvent(score)

    def popUpEvent(self, score):
        QMessageBox.information(self, 'Result', 'The image-text pair similarity is '+str(score)+' %', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
