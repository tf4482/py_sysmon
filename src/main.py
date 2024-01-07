import sqlite3

import matplotlib.pyplot as plt
import psutil
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def get_network_activity():
    net_io = psutil.net_io_counters()
    sent_bytes = net_io.bytes_sent / 1024 / 1024
    received_bytes = net_io.bytes_recv / 1024 / 1024
    return sent_bytes, received_bytes


class SystemMonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.close_button = None
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

        self.network_label_sent = QLabel("Network sent: ", self)
        self.network_label_sent.move(20, 110)
        self.network_label_sent.resize(300, 20)

        self.network_label_received = QLabel("Network received: ", self)
        self.network_label_received.move(20, 140)
        self.network_label_received.resize(300, 20)

        self.close_button = QPushButton("OK", self)
        self.close_button.resize(80, 40)
        self.close_button.clicked.connect(self.close)

        self.show_diagram_button = QPushButton("Show Diagram", self)
        self.show_diagram_button.move(20, 170)
        self.show_diagram_button.clicked.connect(self.show_diagram)

        self.update_button_position()

    def show_diagram(self):
        self.diagram_window = DiagramWindow(self)

    def resizeEvent(self, event):
        self.update_button_position()
        super().resizeEvent(event)

    def update_button_position(self):
        margin = 10
        button_width = self.close_button.width()
        button_height = self.close_button.height()
        button_x = self.width() - button_width - margin
        button_y = self.height() - button_height - margin
        self.close_button.move(button_x, button_y)


class DiagramWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        self.animation = FuncAnimation(self.figure, self.update_plot, interval=1000, cache_frame_data=False)
        self.show()

    def update_plot(self, frame):
        self.ax.clear()


class MainController:
    def __init__(self):
        self.app = QApplication([])
        self.main_window = SystemMonitorWindow()
        self.init_db()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)

    def init_db(self):
        self.conn = sqlite3.connect('py_sysmon_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cpu_usage (usage REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory_usage (usage REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS disk_usage (usage REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sent_mb (usage REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS received_mb (usage REAL)''')

    def run(self):
        self.main_window.show()
        self.app.exec_()

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()
        memory_usage = memory_usage.percent
        disk_usage = psutil.disk_usage('/')
        disk_usage = disk_usage.percent
        sent_mb, received_mb = get_network_activity()

        self.main_window.cpu_label.setText(f"CPU usage: {cpu_usage}%")
        self.main_window.memory_label.setText(f"RAM usage: {memory_usage}%")
        self.main_window.disk_label.setText(f"Disk usage (system-partition): {disk_usage}%")
        self.main_window.network_label_sent.setText(f"Network sent (session): {sent_mb:.2f} MB")
        self.main_window.network_label_received.setText(f"Network received (session): {received_mb: .2f} MB")

        self.insert_into_db('cpu_usage', cpu_usage)
        self.insert_into_db('memory_usage', memory_usage)
        self.insert_into_db('disk_usage', disk_usage)
        self.insert_into_db('sent_mb', sent_mb)
        self.insert_into_db('received_mb', received_mb)

    def insert_into_db(self, table, value):
        self.cursor.execute(f'INSERT INTO {table} (usage) VALUES (?)', (value,))
        self.cursor.execute(f'DELETE FROM {table} WHERE rowid NOT IN (SELECT rowid FROM {table} ORDER BY rowid DESC LIMIT 1000)')

        self.conn.commit()

    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)


if __name__ == "__main__":
    controller = MainController()
    controller.run()
