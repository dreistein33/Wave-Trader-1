from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton
import sys
# I figured out the purpose of gui.
# So basically guy will be used to collect settings
# And with those settings I will run bot.py script with arguments using subprocess.


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('WaveTrader')
        self.line1 = self.create_textbox('SYMBOL (BTC/USDT)', 20, 20, 180, 20)
        self.line2 = self.create_textbox('BALANCE (200)', 20, 40, 180, 40)
        self.line3 = self.create_textbox('ENTRIES (5)', 20, 60, 180, 60)
        self.line4 = self.create_textbox('PROFIT PERCENTAGE (%)', 20, 80, 180, 80)
        self.line5 = self.create_textbox('LOSS PERCENTAGE (%)', 20, 100, 180, 100)
        self.line6 = self.create_textbox('ASSETS TO REALIZE (%)', 20, 120, 180, 120)
        self.button = QPushButton('OK', self)
        self.button.clicked.connect(self.on_click)
        self.button.move(60, 170)
        self.show()

    def create_textbox(self, label, x_pos_label, y_pos_label, x_pos_box, y_pos_box):
        textbox = QLineEdit(self)
        name_label = QLabel(self)
        name_label.setText(label)
        name_label.resize(140, 20)
        textbox.resize(200, 20)
        name_label.move(x_pos_label, y_pos_label)
        textbox.move(x_pos_box, y_pos_box)
        return textbox

    def on_click(self):
        symbol = float(self.line1.text())
        if isinstance(symbol, float):
            print("GIT")
        # TODO:
        # Convert inputs to floats
        # Convert percentages to multipliers
        # Make the button run proper loop script


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())