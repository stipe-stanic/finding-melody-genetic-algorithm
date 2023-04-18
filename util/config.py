from typing import List, Dict, Tuple

import musicalbeeps

from entities.Note import Note

POPULATION_SIZE = 10  # number of possible solutions
NUMBER_OF_NOTES = 12  # melody size
NUMBER_OF_POSSIBLE_NOTES = 36
CROSSOVER_RATE = 0.70  # recombination
MUTATION_RATE = 0.25  # mutation
REPRODUCTION_RATE = 0.40
MAX_NUMBER_OF_GENERATIONS = 25000  # limit in case it takes too many iterations

POSSIBLE_NOTES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
POSSIBLE_OCTAVES = [3, 4, 5, 6]
POSSIBLE_ACCIDENTALS = ['#', 'b', None] # b(flat), #(sharp)
POSSIBLE_DURATIONS = [0.25, 0.5, 1.0, 2.0]


LIST_OF_POSSIBLE_NOTES = ['A4-0.5', 'B4-0.5', 'C4-0.5', 'D4-0.5', 'E4-0.5', 'F4-0.5', 'G4-0.5',
                          'A4b-0.5', 'B4b-0.5', 'D4b-0.5', 'E4b-0.5', 'G4b-0.5',
                          'A4#-0.5', 'C4#-0.5', 'D4#-0.5', 'F4#-0.5', 'G4#-0.5',
                          'A3-0.5', 'B3-0.5', 'C3-0.5', 'D3-0.5', 'E3-0.5', 'F3-0.5', 'G3-0.5',
                          'A5-0.5', 'B5-0.5', 'C5-0.5', 'D5-0.5', 'E5-0.5', 'F5-0.5', 'G5-0.5']

LIST_OF_MELODY_SPECIFIC_NOTES = ['F4-0.25', 'G5b-0.5', 'A3b-0.3', 'F4-0.3', 'G5b-0.3']
LIST_OF_POSSIBLE_NOTES.extend(LIST_OF_MELODY_SPECIFIC_NOTES)
assert len(LIST_OF_POSSIBLE_NOTES) == NUMBER_OF_POSSIBLE_NOTES

# 4/4 time signature, 120 beats per minute, key -> E major or B major
# first verse
lista = [Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.5), Note('E', 5, None, 0.5), Note('E', 5, None, 0.5),
         Note('F', 5, '#', 1.0), Note('D', 5, '#', 0.25), Note('C', 5, '#', 0.25), Note('B', 4, None, 1.5),

         Note('C', 5, '#', 0.5), Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.5), Note('E', 5, None, 0.5),
         Note('C', 5, '#', 0.5), Note('B', 4, None, 0.25), Note('B', 5, None, 0.5), Note('B', 5, None, 0.5),
         Note('F', 5, '#', 1.5),

         Note('C', 5, '#', 0.5), Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.5), Note('E', 5, None, 0.5),
         Note('C', 5, '#', 0.5), Note('E', 5, None, 0.25), Note('F', 5, '#', 0.5), Note('D', 5, '#', 0.5),
         Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.25), Note('C', 5, '#', 0.25), Note('B', 4, None, 1.5),

         Note('C', 5, '#', 0.5), Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.5), Note('E', 5, None, 0.5),
         Note('C', 5, '#', 0.5), Note('B', 4, None, 0.5), Note('F', 5, '#', 0.25), Note('F', 5, '#', 0.25),
         Note('F', 5, '#', 0.25), Note('G', 5, '#', 0.25), Note('F', 5, '#', 1.0),



         # Note('C', 5, '#', 0.5), Note('C', 5, '#', 0.5), Note('D', 5, '#', 0.5), Note('E', 5, None, 0.5),
         # Note('C', 5, '#', 0.5), Note('B', 4, None, 0.5), Note('B', 5, None, 0.5), Note('B', 5, None, 0.5),
         # Note('F', 5, '#', 0.5),
         ]

player = musicalbeeps.Player(volume=0.15, mute_output=False)
for note in lista:
    note_to_play = ""
    if note.accidental:
        note_to_play = note.note + str(note.octave) + note.accidental
    elif note.octave:
        note_to_play = note.note + str(note.octave)
    else:
        note_to_play = "pause"

    duration = note.duration
    player.play_note(note_to_play, duration)


# never gonna give you up...
target_note: List[str] = ['F4-0.25', 'F4-0.25', 'G5b-0.5', 'G5b-0.5',
                          'A3b-0.3', 'G5b-0.5', 'G5b-0.5', 'F4-0.3',
                          'F4-0.3', 'G5b-0.3', 'G5b-0.3', 'F4-0.5']
assert len(target_note) == NUMBER_OF_NOTES

# get key-value pairs from list with value as a number of occurrences
target_dict: Dict[Tuple | str, int] = {}
for note in target_note:
    target_dict[note] = target_dict.get(note, 0) + 1

target_dict: Dict[str, int] = dict(sorted(target_dict.items()))  # sort by key value alphabetically

# print(target_note, target_dict, "----> target_note")

# number of notes * 10 + number of different notes * 5
MAX_FITNESS_VALUE = NUMBER_OF_NOTES * 10 + len(target_dict.keys()) * 5


