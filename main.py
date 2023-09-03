import sys

from PyQt5 import QtWidgets, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSound

from settings import *
from ui import *
import musicgen

class MainWindow(QMainWindow):
    def __init__(self):
        
        # Main setup
        super().__init__()
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        self.layout = QHBoxLayout(w)
        
        self.layoutSettings = QtWidgets.QVBoxLayout()
        self.layoutPNG = QtWidgets.QVBoxLayout()
        
        self.layout.addLayout(self.layoutSettings,1)
        self.layout.addLayout(self.layoutPNG,2)
        
        self.setWindowTitle("Rhythm Trainer")
        self.setGeometry(50,50,320,200)
        
        self.s = load_settings()
        self.s.playMetronome = False                                            # always start without metronome
        
        # Load settings section
        self.settings_window()
        
        # Load pdf viewer
        self.start_image_window()
        
    def settings_window(self):
        """ Creates buttons for all possible settings """
        saveButton = QPushButton("Save Settings")
        saveButton.clicked.connect(self.save_set)
        
        self.generateButton = QPushButton("Generate")
        self.generateButton.clicked.connect(self.start_generate_timer)
        self.generateButton.clicked.connect(self.generate_sheet)
        self.layoutSettings.addWidget(self.generateButton)
        self.layoutSettings.addWidget(saveButton)
        self.generate_timer = QTimer(self)
        self.generate_timer.timeout.connect(self.end_generate_timer)
        
        wholeNoteButton = QPushButton("Whole Notes")
        self.buttonSetToggle(wholeNoteButton, "hasWholeNote", self.s.hasWholeNote)
        self.layoutSettings.addWidget(wholeNoteButton)
        
        halfNoteButton = QPushButton("Half Notes")
        self.buttonSetToggle(halfNoteButton, "hasHalfNote", self.s.hasHalfNote)
        self.layoutSettings.addWidget(halfNoteButton)
        
        quarterNoteButton = QPushButton("Quarter Notes")
        self.buttonSetToggle(quarterNoteButton, "hasQuarterNote", self.s.hasQuarterNote)
        self.layoutSettings.addWidget(quarterNoteButton)
        
        eightNoteButton = QPushButton("Eight Notes")
        self.buttonSetToggle(eightNoteButton, "hasEightNote", self.s.hasEightNote)
        self.layoutSettings.addWidget(eightNoteButton)
        
        sixteenthNoteButton = QPushButton("Sixteenth Notes")
        self.buttonSetToggle(sixteenthNoteButton, "hasSixteenthNote", self.s.hasSixteenthNote)
        self.layoutSettings.addWidget(sixteenthNoteButton)
        
        thirtySecondButton = QPushButton("Thirty Second Notes")
        self.buttonSetToggle(thirtySecondButton, "hasThirtySecondNote", self.s.hasThirtySecondNote)
        self.layoutSettings.addWidget(thirtySecondButton)
        
        dottedNotesButton = QPushButton("Dotted Notes")
        self.buttonSetToggle(dottedNotesButton, "hasDottedNotes", self.s.hasDottedNotes)
        self.layoutSettings.addWidget(dottedNotesButton)
        
        tiesButton = QPushButton("Ties")
        self.buttonSetToggle(tiesButton, "hasTiedNotes", self.s.hasTiedNotes)
        self.layoutSettings.addWidget(tiesButton)
        
        TripletsButton = QPushButton("Triplets")
        self.buttonSetToggle(TripletsButton, "hasTriplets", self.s.hasTriplets)
        self.layoutSettings.addWidget(TripletsButton)
        
        self.divident = SideByTextLineEdit(self.s, "Dividend","dividend",str(self.s.dividend))
        self.layoutSettings.addWidget(self.divident)
        
        self.divisor = SideByTextLineEdit(self.s, "Divisor","divisor",str(self.s.divisor))
        self.layoutSettings.addWidget(self.divisor)
        
        self.subdiv = SideByTextLineEdit(self.s, "Subdivision","subdiv",str(self.s.subdiv))
        self.layoutSettings.addWidget(self.subdiv)
        
        self.tempo = SideByTextLineEdit(self.s, "Tempo","tempo",str(self.s.tempo))
        self.layoutSettings.addWidget(self.tempo)
        
        self.bars = SideByTextLineEdit(self.s, "Bars","bars",str(self.s.bars))
        self.layoutSettings.addWidget(self.bars)
        
        self.metronomeButton = QPushButton("Metronome")
        self.buttonSetToggle(self.metronomeButton, "playMetronome", self.s.playMetronome)
        self.layoutSettings.addWidget(self.metronomeButton)
        
        self.metronomeButton.clicked.connect(self.start_metronome_timer)
        self.metronome_timer = QTimer(self)
        self.metronome_timer.timeout.connect(self.end_metronome_timer)
        
    def buttonSetToggle(self, button, attribute_name, currentVal):
        def toggle_attribute():
            current_value = getattr(self.s, attribute_name)
            setattr(self.s, attribute_name, not current_value)
        
        button.clicked.connect(toggle_attribute)
        self.changeToggleColor(button, currentVal)
        button.clicked.connect(lambda: self.changeToggleColor(button, button.isChecked()))
        button.setCheckable(True)
        button.setChecked(currentVal)
        
    def changeToggleColor(self, button, isOn):
        if isOn:
            button.setStyleSheet("background-color : lightgreen")
        else:
            button.setStyleSheet("background-color : red")

    def save_set(self):
        save_settings(self.s)

    def generate_sheet(self):
        musicgen.generate_sheet(self.s)
        
    def start_generate_timer(self):
        self.generate_timer.start(2000)  # Start a 3-second timer
        self.generateButton.setEnabled(False)
        
    def end_generate_timer(self):
        self.generateButton.setEnabled(True)
        self.update_image_window()
        
    def start_metronome_timer(self):
        if(self.metronomeButton.isChecked()):
            self.metronome_timer.start(int((60000 / self.s.tempo) * (4/self.s.subdiv)))  # Start a 3-second timer
        
    def end_metronome_timer(self):
        if(self.metronomeButton.isChecked()):
            # play sound
            #print("playing metronome")
            QtMultimedia.QSound.play("./metronome.wav")
            
            self.start_metronome_timer()
            
        
    def update_image_window(self):
        pixmap = QPixmap('./output_sheet.cropped.png')
        self.sheetLabel.setPixmap(pixmap)
    
    def start_image_window(self):
        self.sheetLabel = QLabel(self)
        self.layoutPNG.addWidget(self.sheetLabel)
        
        self.update_image_window()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()