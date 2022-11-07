from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
# I figured out the purpose of gui.
# So basically guy will be used to collect settings
# And with those settings I will run bot.py script with arguments using subprocess


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('WaveTrader')
        self.show()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())