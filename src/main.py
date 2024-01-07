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

        self.cpu_label = QLabel("CPU Usage: ", self)
        self.cpu_label.move(20, 20)
        self.cpu_label.resize(200, 20)

        self.memory_label = QLabel("RAM Usage: ", self)
        self.memory_label.move(20, 50)
        self.memory_label.resize(200, 20)

        self.disk_label = QLabel("Disk Usage: ", self)
        self.disk_label.move(20, 80)
        self.disk_label.resize(200, 20)


class MainController:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = SystemMonitorWindow()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)

    def run(self):
        self.main_window.show()
        self.app.exec_()

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()
        memory_usage = memory_usage.percent
        disk_usage = psutil.disk_usage('/')
        disk_usage = disk_usage.percent

        self.main_window.cpu_label.setText(f"CPU usage: {cpu_usage}%")
        self.main_window.memory_label.setText(f"RAM usage: {memory_usage}%")
        self.main_window.disk_label.setText(f"Disk usage (system-partition): {disk_usage}%")


if __name__ == "__main__":
    controller = MainController()
    controller.run()
