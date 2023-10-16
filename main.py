import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton


class ProfitCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profit Calculator")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.num_ads_label = QLabel("Input Number of total Ads:")
        self.num_ads_input = QLineEdit()
        self.submit_button = QPushButton("Submit")

        self.layout.addWidget(self.num_ads_label)
        self.layout.addWidget(self.num_ads_input)
        self.layout.addWidget(self.submit_button)

        self.submit_button.clicked.connect(self.handle_submit)
        self.num_ads_input.returnPressed.connect(self.handle_submit)  # Connect Enter key press event

    def handle_submit(self):
        try:
            total_num_ads = int(self.num_ads_input.text())
            self.layout.removeWidget(self.submit_button)
            self.submit_button.deleteLater()

            self.ad_inputs = []
            self.ads_spent_each = []
            for i in range(total_num_ads):
                ad_layout = QHBoxLayout()
                ad_label = QLabel(f"Enter dollar spent Ads {i + 1}:")
                ad_input = QLineEdit()
                ad_input.returnPressed.connect(self.move_to_next_ad)  # Connect Enter key press event
                self.ad_inputs.append(ad_input)
                self.ads_spent_each.append(ad_input)
                ad_layout.addWidget(ad_label)
                ad_layout.addWidget(ad_input)
                self.layout.addLayout(ad_layout)

            self.total_orders_label = QLabel("Total Orders:")
            self.total_orders_input = QLineEdit()
            self.layout.addWidget(self.total_orders_label)
            self.layout.addWidget(self.total_orders_input)
            self.total_orders_input.returnPressed.connect(self.move_to_dollar_rate)

            self.dollar_rate_label = QLabel("Dollar Rate:")
            self.dollar_rate_input = QLineEdit()
            self.layout.addWidget(self.dollar_rate_label)
            self.layout.addWidget(self.dollar_rate_input)
            self.dollar_rate_input.returnPressed.connect(self.move_to_calculate)

            self.calculate_button = QPushButton("Calculate")
            self.layout.addWidget(self.calculate_button)
            self.calculate_button.clicked.connect(self.calculate_profit)

            self.output_label = QLabel()
            self.layout.addWidget(self.output_label)

            # Set focus to the first ads input field
            self.ad_inputs[0].setFocus()

        except ValueError:
            pass

    def move_to_next_ad(self):
        current_index = self.ad_inputs.index(self.sender())
        if current_index < len(self.ad_inputs) - 1:
            self.ad_inputs[current_index + 1].setFocus()
        elif current_index == len(self.ad_inputs) - 1:
            self.total_orders_input.setFocus()

    def move_to_dollar_rate(self):
        self.dollar_rate_input.setFocus()

    def move_to_calculate(self):
        self.calculate_button.setFocus()

    def calculate_profit(self):
        try:
            ads_spent_total = sum(float(ad.text()) for ad in self.ads_spent_each)
            total_orders = float(self.total_orders_input.text())
            dollar_rate = float(self.dollar_rate_input.text())
            dollar_rate_total = ads_spent_total * dollar_rate
            cost = dollar_rate_total / total_orders
            total_cost = cost + 220
            profit_per_product = 450 - total_cost
            total_profit = profit_per_product * total_orders

            self.output_label.setText(f"Total profit is: ${total_profit:.2f}")
        except ValueError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProfitCalculatorApp()
    window.show()
    sys.exit(app.exec_())
