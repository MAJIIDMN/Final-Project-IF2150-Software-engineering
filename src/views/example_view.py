from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from controllers.example_controller import ExampleController

class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ExampleController()

        self.setWindowTitle("Example App")

        self.label = QLabel("Counter: 0")
        self.button = QPushButton("Add")

        self.button.clicked.connect(self.handle_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def handle_click(self):
        new_value = self.controller.add_one()
        self.label.setText(f"Counter: {new_value}")
