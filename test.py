import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWondow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Add a title
        self.setWindowTitle('My First App')

        # set the layout
        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        # Add a label
        label = qtw.QLabel('Hello World!')

        # change the font
        font = qtg.QFont('Helvetica', 20)
        label.setFont(font)

        # Add the label to the layout
        layout.addWidget(label)

        self.show()

app = qtw.QApplication([])
mw = MainWondow()

# Run the application
app.exec_()