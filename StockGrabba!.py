import sys
import yfinance as yf
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QCalendarWidget,
    QCheckBox,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QDesktopWidget,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve

class StockDataGrabber(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stock Data Grabber")
        self.setWindowSize()
        self.createWidgets()
        self.layoutWidgets()
        self.connectSignals()
        self.setupAnimations()

    def setWindowSize(self):
        desktop_geometry = QDesktopWidget().availableGeometry()
        width = int(desktop_geometry.width() * 0.4)
        height = int(desktop_geometry.height() * 0.6)
        self.setGeometry(
            int(desktop_geometry.width() * 0.3),
            int(desktop_geometry.height() * 0.2),
            width,
            height,
        )

    def createWidgets(self):
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter ticker symbol (e.g., AMZN)")
        self.ticker_layout = QHBoxLayout()
        self.ticker_layout.addWidget(self.ticker_input)
        self.start_date_input = QLineEdit()
        self.end_date_input = QLineEdit()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.use_calendar = QCheckBox("Use Calendar")
        self.use_calendar.setChecked(True)
        self.start_calendar = QCalendarWidget()
        self.start_calendar.setGridVisible(True)
        self.start_calendar.setVisible(True)
        self.end_calendar = QCalendarWidget()
        self.end_calendar.setGridVisible(True)
        self.end_calendar.setVisible(True)
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["1d", "1wk", "1mo"])
        self.save_button = QPushButton("Save Data")
        self.scrape_button = QPushButton("Scrape")

    def layoutWidgets(self):
        input_layout = QHBoxLayout()
        for widget in [
            QLabel("Ticker Symbol:"),
            self.ticker_layout,
            QLabel("Start Date (YYYY-MM-DD):"),
            self.start_date_input,
            QLabel("End Date (YYYY-MM-DD):"),
            self.end_date_input,
            self.use_calendar,
            QLabel("Interval:"),
            self.interval_combo,
        ]:
            if isinstance(widget, QHBoxLayout):
                input_layout.addLayout(widget)
            else:
                input_layout.addWidget(widget)

        date_layout = QHBoxLayout()
        date_layout.addWidget(self.start_calendar)
        date_layout.addWidget(self.end_calendar)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.scrape_button)

        output_scroll_area = QScrollArea()
        output_scroll_area.setWidgetResizable(True)
        output_scroll_area.setWidget(self.output_text)

        main_layout = QVBoxLayout()
        for layout in [input_layout, date_layout, button_layout, output_scroll_area]:
            main_layout.addLayout(layout) if isinstance(layout, QHBoxLayout) else main_layout.addWidget(layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def connectSignals(self):
        self.ticker_input.returnPressed.connect(self.fetch_data)
        self.use_calendar.stateChanged.connect(self.toggle_calendar)
        self.start_calendar.selectionChanged.connect(self.update_start_date)
        self.end_calendar.selectionChanged.connect(self.update_end_date)
        self.save_button.clicked.connect(self.save_data)
        self.scrape_button.clicked.connect(self.fetch_data)

    def setupAnimations(self):
        self.fade_animation = QPropertyAnimation(self.output_text, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def toggle_calendar(self, state):
        self.start_date_input.setEnabled(not state)
        self.end_date_input.setEnabled(not state)
        self.start_calendar.setVisible(state)
        self.end_calendar.setVisible(state)

    def update_start_date(self):
        self.start_date_input.setText(
            self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        )

    def update_end_date(self):
        self.end_date_input.setText(
            self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        )

    def fetch_data(self):
        ticker_symbol = self.ticker_input.text().upper()

        start_date = self.start_date_input.text() if not self.use_calendar.isChecked() else self.start_calendar.selectedDate().toPyDate()
        end_date = self.end_date_input.text() if not self.use_calendar.isChecked() else self.end_calendar.selectedDate().toPyDate()
        interval = self.interval_combo.currentText()

        self.output_text.clear()

        try:
            if self.use_calendar.isChecked():
                data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
            else:
                if start_date and end_date:
                    data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
                else:
                    self.output_text.append(f"Error fetching data for {ticker_symbol}: Invalid date format.\n")
                    return

            if data.empty:
                self.output_text.append(f"No data available for {ticker_symbol} in the given date range.\n")
            else:
                self.output_text.append(f"Close prices for {ticker_symbol} ({interval}):\n")
                for date, close in zip(data.index, data["Close"]):
                    if close:
                        self.output_text.append(f"{date.strftime('%Y-%m-%d')}: {close:.2f}")
                    else:
                        self.output_text.append(f"{date.strftime('%Y-%m-%d')}: Close price not available")
                self.output_text.append("\n")
        except Exception as e:
            self.output_text.append(f"Error fetching data for {ticker_symbol}: {str(e)}\n")

        self.fade_animation.start()

    def save_data(self):
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix(".txt")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if file_dialog.exec_() == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            try:
                with open(file_path, "w") as file:
                    file.write(self.output_text.toPlainText())
                QMessageBox.information(self, "Success", "Data saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error saving data: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    grabber = StockDataGrabber()
    grabber.show()
    sys.exit(app.exec_())
