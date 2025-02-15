import json
import subprocess
import sys

from utils.mathutils import convert_percent_to_mul
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton, QCheckBox

# I figured out the purpose of gui.
# So basically guy will be used to collect settings
# And with those settings I will run bot.py script with arguments using subprocess.


def generate_static_buy_thresholds(starting_price, entries, multiplier):
    # multiplier will need to be just a normal fraction without converting
    thresholds = list()
    for i in range(entries):
        # Multiply starting price by percentage multiplier represented in decimal form e.g. (5% = 5 / 100 = 0.05)
        # Then increase the multiplier by 100% with every iteration.
        # Example:
        # 1st iteration: multiplier = 0.05 * 1 = 0.05
        # 2nd iteration: multiplier = 0.05 * 2 = 0.10
        # 3rd iteration: multiplier = 0.05 * 3 = 0.15
        multiplied_price = starting_price*(1-multiplier*i)
        thresholds.append(multiplied_price)
    return sorted(thresholds, reverse=True)


def generate_dynamic_buy_thresholds(starting_price, entries, multiplier):
    """
    The difference between static and dynamic thresholds are that static thresholds are generated by multiplying only
    the starting price where in dynamic thresholds the last threshold is multiplied.
    Example:
        starting price = $20000 -> 1st entry
        $20000 * 0.95 =  $19000 -> 2nd entry
        $19000 * 0.95 =  $18050 -> 3rd entry
    And so on
    So with every iteration the next buy threshold is slightly higher than in static threshold generator
    """
    thresholds = list()
    thresholds.append(starting_price)
    for i in range(entries-1):
        thresholds.append(thresholds[-1]*(1-multiplier))
    return sorted(thresholds, reverse=True)


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
        self.line7 = self.create_textbox('NEW THRESHOLD (%)', 20, 150, 180, 150)
        self.run_button = QPushButton('SAVE', self)
        self.run_button.clicked.connect(self.save_settings)
        self.run_button.move(150, 200)
        self.api_button = QPushButton('SET API', self)
        self.api_button.clicked.connect(self.show_api_settings)
        self.api_button.move(150, 250)
        self.install_pkgs_button = QPushButton('RESET ORDERS', self)
        self.install_pkgs_button.clicked.connect(self.reset_orders)
        self.install_pkgs_button.resize(120, 35)
        self.install_pkgs_button.move(140, 300)
        self.dynamic_thresholds_cb = QCheckBox('Dynamic thresholds', self)
        self.dynamic_thresholds_cb.resize(120, 30)
        self.dynamic_thresholds_cb.move(20, 170)
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
        balance = float(self.line2.text())
        entries = int(self.line3.text())
        starting_price = float(self.line4.text())
        profit_mul = float(self.line5.text()) / 100
        loss_mul = float(self.line6.text()) / 100
        new_threshold = float(self.line7.text()) / 100
        if self.dynamic_thresholds_cb.isChecked():
            buy_thresholds = generate_dynamic_buy_thresholds(starting_price, entries, loss_mul)
        else:
            buy_thresholds = generate_static_buy_thresholds(starting_price, entries, loss_mul)
        args_dict = {
            'symbol': symbol.replace('/', ''),
            'starting_price': starting_price,
            'balance': balance,
            'entries': entries,
            'profit_mul': profit_mul,
            'loss_mul': loss_mul,
            'buy_thresholds': buy_thresholds,
            'new_threshold': new_threshold
        }

        with open(CONFIG_PATH, 'w') as f:
            json.dump(args_dict, f, indent=2)

    def show_api_settings(self):
        self.w.show()

    def reset_orders(self):
        from utils.waveutils import ORDERS_PATH
        with open(ORDERS_PATH, 'w') as f:
            pass


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
