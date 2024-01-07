import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class SystemMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("py_sysmon")
        self.setGeometry(100, 100, 600, 400)
        self.label = QLabel("CPU Usage: ", self)
        self.label.move(20, 20)
        self.label.resize(200, 20)


class MainController:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = SystemMonitorWindow()

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_cpu_usage)
        self.timer.start(1000)

    def run(self):
        self.main_window.show()
        self.app.exec_()

    def get_cpu_usage(self):
        cpu_usage = psutil.cpu_percent()

        self.main_window.label.setText(f"CPU usage: {cpu_usage}%")


if __name__ == "__main__":
    controller = MainController()
    controller.run()
