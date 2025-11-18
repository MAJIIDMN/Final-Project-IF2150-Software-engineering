from PyQt5.QtWidgets import QApplication
import sys

from views.example_view import ExampleWindow

def main():
    app = QApplication(sys.argv)
    
    window = ExampleWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
