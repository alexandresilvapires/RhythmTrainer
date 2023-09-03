from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QIntValidator

class SideByTextLineEdit(QWidget):
    def __init__(self, settings, label_text="", attribute_name="", input_text=""):
        super().__init__()

        self.layout = QHBoxLayout()
        
        self.s = settings

        self.label = QLabel(label_text)
        self.layout.addWidget(self.label)

        self.lineEdit = QLineEdit(input_text)
        
        self.attributeName = attribute_name
        
        # Create a QIntValidator to allow only integer input
        int_validator = QIntValidator()
        self.lineEdit.setValidator(int_validator)
        
        self.layout.addWidget(self.lineEdit)

        self.setLayout(self.layout)
        
        self.lineEdit.textChanged.connect(self.setNewAttributeValue)
        
    def getLineEdit(self) -> QLineEdit:
        return self.lineEdit
    
    def setNewAttributeValue(self):
        try:
            setattr(self.s, self.attributeName, int(self.lineEdit.text()))
        except:
            setattr(self.s, self.attributeName, 1)