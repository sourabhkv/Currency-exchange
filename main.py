import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit
import requests

class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.amount_field = QLineEdit()
        layout.addWidget(self.amount_field)

        self.from_currency = QComboBox()
        layout.addWidget(self.from_currency)

        self.to_currency = QComboBox()
        layout.addWidget(self.to_currency)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        button = QPushButton('Convert')
        button.clicked.connect(self.perform_conversion)
        layout.addWidget(button)

        self.setLayout(layout)

        self.load_currencies()

    def load_currencies(self):
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()

        currencies = data['rates'].keys()
        self.from_currency.addItems(currencies)
        self.to_currency.addItems(currencies)

    def perform_conversion(self):
        from_curr = self.from_currency.currentText()
        to_curr = self.to_currency.currentText()
        amount = float(self.amount_field.text())

        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_curr}')
        data = response.json()

        rate = data['rates'][to_curr]
        result = rate * amount

        self.result_label.setText(f'{amount} {from_curr} = {result} {to_curr}')

def main():
    app = QApplication(sys.argv)

    converter = CurrencyConverter()
    converter.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
