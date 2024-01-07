import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class SystemMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 600, 400)
        self.label = QLabel("CPU Usage: ", self)
        self.label.move(20, 20)
        self.label.resize(200, 20)


