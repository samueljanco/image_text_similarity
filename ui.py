import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, \
    QFileDialog, QTextEdit
from PyQt5.QtGui import QPixmap

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.input_text = ""
        self.input_image_path = ""

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
        self.button = QPushButton('Button', self)

        # Set up the layout
        layout = QVBoxLayout(self)
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textfield)
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.image_label)
        v_layout.addWidget(self.image_button)
        h_layout.addLayout(v_layout)
        layout.addLayout(h_layout)
        layout.addWidget(self.button)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.xpm *.jpg *.bmp);;All Files (*)', options=options)
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.input_image_path = file_name


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
