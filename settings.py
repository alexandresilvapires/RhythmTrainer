import pickle

path = "settings.data"

class Settings:
    def __init__(self):
        
        # Musical note settings
        self.hasWholeNote = True
        self.hasHalfNote = True
        self.hasQuarterNote = True
        self.hasEightNote = False
        self.hasSixteenthNote = False
        self.hasThirtySecondNote = False
        
        self.hasDottedNotes = False
        self.hasTiedNotes = False
        self.hasTriplets = False
        
        # Rhythm settings
        self.dividend = 4
        self.divisor = 4
        self.subdiv = 4
        self.tempo = 80
        self.bars = 12
        
        # Playback settings
        self.playMetronome = False
        
def save_settings(settings: Settings) -> None:
    with open(path, 'wb') as file:
        pickle.dump(settings, file)
        
def load_settings() -> Settings:
    try:
        with open(path, 'rb') as file:
            return pickle.load(file)
    except:
        return Settings()
