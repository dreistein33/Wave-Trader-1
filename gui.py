import json
import subprocess
import sys

from utils.mathutils import convert_percent_to_mul
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton, QWidget

# I figured out the purpose of gui.
# So basically guy will be used to collect settings
# And with those settings I will run bot.py script with arguments using subprocess.


class ApiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.line = self.create_textbox('PUBLIC KEY', 20, 30, 180, 30)
        self.line2 = self.create_textbox('PRIVATE KEY', 20, 50, 180, 50)
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('API SETTINGS')
        self.save_button = QPushButton('SAVE', self)
        self.save_button.move(150, 80)
        self.save_button.clicked.connect(self.save_api_keys)

    def create_textbox(self, label, x_pos_label, y_pos_label, x_pos_box, y_pos_box):
        textbox = QLineEdit(self)
        name_label = QLabel(self)
        name_label.setText(label)
        name_label.resize(140, 20)
        textbox.resize(200, 20)
        name_label.move(x_pos_label, y_pos_label)
        textbox.move(x_pos_box, y_pos_box)
        return textbox

    def save_api_keys(self):
        from utils.waveutils import ENV_PATH
        env_path = ENV_PATH
        PUBLICKEY = self.line.text()
        PRIVKEY = self.line2.text()
        with open(env_path, 'w') as f:
            f.write(f"PUBLICKEY={PUBLICKEY}\nPRIVKEY={PRIVKEY}")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('WaveTrader')
        self.w = ApiWindow()
        self.line1 = self.create_textbox('SYMBOL (BTC/USDT)', 20, 30, 180, 30)
        self.line2 = self.create_textbox('BALANCE (200)', 20, 50, 180, 50)
        self.line3 = self.create_textbox('ENTRIES (5)', 20, 70, 180, 70)
        self.line4 = self.create_textbox('STARTING PRICE (20000)', 20, 90, 180, 90)
        self.line5 = self.create_textbox('PROFIT PERCENTAGE (%)', 20, 110, 180, 110)
        self.line6 = self.create_textbox('LOSS PERCENTAGE (%)', 20, 130, 180, 130)
        self.line7 = self.create_textbox('ASSETS TO REALIZE (%)', 20, 150, 180, 150)
        self.run_button = QPushButton('OK', self)
        self.run_button.clicked.connect(self.save_settings)
        self.run_button.move(150, 170)
        self.api_button = QPushButton('SET API', self)
        self.api_button.clicked.connect(self.show_api_settings)
        self.api_button.move(150, 220)
        # self.statusBar()
        # self.menubar = self.menuBar()
        # self.file_menu = self.menubar.addMenu('SET API KEYS')
        # self.file_menu.addAction(self.show_api_settings)
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

    def save_settings(self):
        from utils.waveutils import CONFIG_PATH

        symbol = self.line1.text()
        data_to_dict = {'symbol': symbol}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data_to_dict, f)

        balance = float(self.line2.text())
        entries = int(self.line3.text())
        starting_price = float(self.line4.text())
        profit_mul = convert_percent_to_mul(float(self.line5.text()), loss=False)
        loss_mul = convert_percent_to_mul(float(self.line6.text()))
        sell_assets_mul = float(self.line7.text()) / 100
        args_dict = {
            '-sp': starting_price,
            '-b': balance,
            '-e': entries,
            '-pp': profit_mul,
            '-lp': loss_mul,
            '-sa': sell_assets_mul
        }

        run_cmd = 'python bot.py '
        for keys, values in args_dict.items():
            args_to_add = f'{keys} {values} '
            run_cmd += args_to_add
        subprocess.call(run_cmd, shell=True)
        # TODO:
        # Convert inputs to floats
        # Convert percentages to multipliers
        # Make the button run proper loop script

    def show_api_settings(self):
        self.w.show()


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())