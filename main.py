import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QStackedWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import paramiko


class SSHClientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ssh_client = None
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.ssh_connect_widget = self.create_ssh_connect_widget()
        self.install_python_widget = InstallPythonWidget()

        self.stacked_widget.addWidget(self.ssh_connect_widget)
        self.stacked_widget.addWidget(self.install_python_widget)

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('SSH Client')
        self.setGeometry(100, 100, 300, 200)
        self.setWindowIcon(QIcon('icon.png'))  # Add an appropriate icon file

        # Add minimize, maximize, and close buttons
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        # Set stylesheet for attractive design
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QMessageBox {
                background-color: white;
            }
        """)

    def create_ssh_connect_widget(self):
        widget = QWidget()
        vbox = QVBoxLayout()
        hbox_user = QHBoxLayout()
        hbox_ip = QHBoxLayout()
        hbox_password = QHBoxLayout()
        hbox_buttons = QHBoxLayout()

        self.user_label = QLabel('Username:')
        self.user_input = QLineEdit()
        hbox_user.addWidget(self.user_label)
        hbox_user.addWidget(self.user_input)

        self.ip_label = QLabel('IP Address:')
        self.ip_input = QLineEdit()
        hbox_ip.addWidget(self.ip_label)
        hbox_ip.addWidget(self.ip_input)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        hbox_password.addWidget(self.password_label)
        hbox_password.addWidget(self.password_input)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_ssh)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        hbox_buttons.addWidget(self.connect_button)
        hbox_buttons.addWidget(self.cancel_button)
        vbox.addLayout(hbox_user)
        vbox.addLayout(hbox_ip)
        vbox.addLayout(hbox_password)
        vbox.addLayout(hbox_buttons)

        widget.setLayout(vbox)
        return widget

    def connect_ssh(self):
        username = self.user_input.text()
        ip_address = self.ip_input.text()
        password = self.password_input.text()

        if not username or not ip_address or not password:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')
            return

        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(ip_address, username=username, password=password)

            QMessageBox.information(self, 'Success', f'Successfully connected to {ip_address}')
            self.install_python_widget.set_ssh_client(self.ssh_client)
            self.stacked_widget.setCurrentWidget(self.install_python_widget)
        except Exception as e:
            QMessageBox.critical(self, 'Connection Failed', str(e))


class InstallPythonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ssh_client = None
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        hbox_version = QHBoxLayout()
        hbox_directory = QHBoxLayout()
        hbox_buttons = QHBoxLayout()

        self.version_label = QLabel('Python Version:')
        self.version_input = QLineEdit()
        hbox_version.addWidget(self.version_label)
        hbox_version.addWidget(self.version_input)

        self.directory_label = QLabel('Install Directory:')
        self.directory_input = QLineEdit()
        hbox_directory.addWidget(self.directory_label)
        hbox_directory.addWidget(self.directory_input)

        self.install_button = QPushButton('Install Python')
        self.install_button.clicked.connect(self.install_python)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        hbox_buttons.addWidget(self.install_button)
        hbox_buttons.addWidget(self.cancel_button)
        vbox.addLayout(hbox_version)
        vbox.addLayout(hbox_directory)
        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

        self.setWindowTitle('Install Python')
        self.setGeometry(150, 150, 400, 200)
        self.setWindowIcon(QIcon('icon.png'))

        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QMessageBox {
                background-color: white;
            }
        """)

    def set_ssh_client(self, ssh_client):
        self.ssh_client = ssh_client

    def install_python(self):
        python_version = self.version_input.text()
        install_directory = self.directory_input.text()

        if not python_version or not install_directory:
            QMessageBox.warning(self, 'Input Error', 'All fields are required')
            return

        if not python_version.startswith('3'):
            QMessageBox.warning(self, 'Input Error', 'Python version must be 3.x')
            return

        try:
            # Check if the directory exists and create it if it doesn't
            stdin, stdout, stderr = self.ssh_client.exec_command(f"mkdir -p {install_directory}")
            stdout.channel.recv_exit_status()

            # Navigate to the directory and install Python
            commands = [
                f"cd {install_directory}",
                f"wget https://www.python.org/ftp/python/{python_version}/Python-{python_version}.tgz",
                f"tar -xvf Python-{python_version}.tgz",
                f"cd Python-{python_version}",
                "./configure",
                "make",
                "sudo make install"
            ]

            for command in commands:
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                exit_status = stdout.channel.recv_exit_status()
                if exit_status != 0:
                    raise Exception(stderr.read().decode())

            QMessageBox.information(self, 'Success', f'Python {python_version} installed successfully in {install_directory}')
        except Exception as e:
            QMessageBox.critical(self, 'Installation Failed', str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SSHClientApp()
    ex.show()
    sys.exit(app.exec_())
