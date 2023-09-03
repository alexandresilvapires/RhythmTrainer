from settings import *
import subprocess
import random

# Generation parameters

class Note:
    def __init__(self, weight, followup_chance, notation, duration):
        self.weight = weight                                # Weight of each note -> Bigger weight = more chance to appear
        self.followup_chance = followup_chance              # Probability that, after the figure is used, the next figure is also the same
        self.notation = notation                            # How its written in Lilypond
        self.duration = duration
        
WholeNote = Note(0.5, 0, "c1", 4)
HalfNote = Note(2, 0.1, "c2", 2)
QuarterNote = Note(6, 0.3, "c4", 1)
EightNote = Note(4, 0.7, "c8", 1/2)
SixteenthNote = Note(2, 0.5, "c16", 1/4)
ThirtySecondNote = Note(1, 0.7, "c32", 1/8)

QuarterNoteTriplet = Note(0.75, 0, r"\tuplet 3/2 {c4 c c}", 2)
EightNoteTriplet = Note(1.25, 0.05, r"\tuplet 3/2 {c8 c c}", 1)

ChanceDottedNotes = 0.1
ChanceTiedNotes = 0.1
ChanceToBeRest = 0.125

def generate_notes(s: Settings):
    """ Generates the Lilypond text for the new rhythm """
    
    # Pick what notes are possible
    possibleNotes = []
    if s.hasWholeNote: possibleNotes.append(WholeNote)
    if s.hasHalfNote: possibleNotes.append(HalfNote)
    if s.hasQuarterNote: possibleNotes.append(QuarterNote)
    if s.hasEightNote: possibleNotes.append(EightNote)
    if s.hasSixteenthNote: possibleNotes.append(SixteenthNote)
    if s.hasThirtySecondNote: possibleNotes.append(ThirtySecondNote)
    if s.hasTriplets: 
        possibleNotes.append(QuarterNoteTriplet)
        possibleNotes.append(EightNoteTriplet)
        
    if len(possibleNotes) == 0:
        return "c1"
    
    # We start with 0 beats done, randomly select a note, and, if it fits, add it to the list
    currentBeats = 0
    totalBeats = s.dividend * s.bars
    
    currentNoteText = ""
    
    weights = []
    for note in possibleNotes:
        weights.append(note.weight)
        
    newNote = None
    
    while(currentBeats < totalBeats):
        print("Current beats: " + str(currentBeats) + " total: " + str(totalBeats))

        if(newNote != None and random.random() < newNote.followup_chance):
            print("following up last note!")
        
        else:
            # Pick new note
            newNote = random.choices(possibleNotes, weights=weights)[0]
            while(newNote.duration + currentBeats > totalBeats):
                print("testing new note" "Current beats: " + str(currentBeats) + " total: " + str(totalBeats))
                newNote = random.choices(possibleNotes, weights=weights)[0]
        
        # Maybe add rest instead
        if(random.random() < ChanceToBeRest):
            currentNoteText += "r" + newNote.notation[1:]
        else:
            currentNoteText += newNote.notation
        currentBeats += newNote.duration
        
        # Add dot mutation
        addedDot = False
        if(s.hasDottedNotes and currentBeats + newNote.duration*1.5 <= totalBeats):
            if(random.random() < ChanceDottedNotes):
                currentNoteText += "."
                addedDot = True
                currentBeats += newNote.duration * 0.5

        # Add tie mutation (if not rest)
        if(s.hasTiedNotes and currentBeats + newNote.duration * (1.5 if addedDot else 1) < totalBeats):
            if(random.random() < ChanceTiedNotes):
                currentNoteText += "~"
                
        currentNoteText += " "
    
    return currentNoteText

def generate_sheet_text(s, notesText):
    template = f'''
\\version "2.24.2"
\\new RhythmicStaff \\with {{
    \\remove "Note_heads_engraver"
    \\consists "Completion_heads_engraver"
    \\remove "Rest_engraver"
    \\consists "Completion_rest_engraver"
}}

\\relative {{
    \\time {s.dividend}/{s.divisor}
    \\tempo {s.subdiv} = {s.tempo}
    {notesText}
}}
'''


    sheet_text = template
    
    with open("output_sheet.txt", "w") as file:
        file.write(sheet_text)

def generate_sheet(s: Settings):
    
    # Make new text that contains the notes
    notesText = generate_notes(s)
    
    # Make new text file to generate pdf
    sheetText = generate_sheet_text(s, notesText)
    
    # Call LilyPond to generate the sheet music pdf
    try:
        subprocess.run(["./lilypond-2.24.2/bin/lilypond", "-fpng", "-dcrop", "output_sheet.txt"], check=True)
        print("Sheet generated successfully.")
    except subprocess.CalledProcessError as e:
        print("Error generating sheet:", e)