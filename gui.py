from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('WaveTrader')
        self.show()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())