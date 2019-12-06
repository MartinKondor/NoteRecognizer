import winsound

import pygame
from pygame import locals as keys
import numpy as np

from src.note_recognizer import NoteRecognizer
from src.config import IS_FULLSCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, FPS


class Display:

    def __init__(self):
        self.note_recognizer = NoteRecognizer()
        self.octave = 4
        self.line_height = WINDOW_HEIGHT / 12
    
        font = pygame.font.SysFont('Arial', int(self.line_height / 2))
        color_constant = 255 / 12

        self.note_names = [
            'A', 'Bb / A#', 'B',
            'C', 'Db / C#', 'D',
            'Eb / D#', 'E', 'F',
            'Gb / F#', 'G', 'Ab / G#'
        ]
        self.note_texts = [font.render(n, False, (37, 37, 37)) for n in self.note_names]
        self.pitch_lines = [
            ((255, i * color_constant, 50,), (0, i * (self.line_height), WINDOW_WIDTH, self.line_height + 1)) for i in range(12)
            #((i * color_constant, i * color_constant, i * color_constant,), (0, i * (self.line_height), WINDOW_WIDTH, self.line_height + 1)) for i in range(12)
        ]
        
        # Reverse lines to not overlap each other
        # self.pitch_lines = self.pitch_lines[::-1]

    def display(self, screen):
        mouse_pos = pygame.mouse.get_pos()
    
        for i, (pitch_lines_color, pitch_line_coords,) in enumerate(self.pitch_lines):
            pygame.draw.rect(screen, pitch_lines_color, pitch_line_coords)

            if mouse_pos[0] > 0 and mouse_pos[1] > i * self.line_height and mouse_pos[0] < WINDOW_WIDTH and mouse_pos[1] < i * self.line_height + self.line_height and \
                    pygame.mouse.get_pressed()[0]:
                    
                pygame.draw.rect(screen, [c * 0.8 for c in pitch_lines_color], pitch_line_coords)
                freq = int(440 * 2 ** ((self.octave * 17.25 + i - 69) / 12))
                winsound.Beep(freq, 100)
                
            # Draw note name
            text_coords = (pitch_line_coords[0] + WINDOW_WIDTH / 2 - len(self.note_names[i]) * 3, pitch_line_coords[1],)
            screen.blit(self.note_texts[i], text_coords)

        try:
            hz = self.note_recognizer.update()
            octave = abs(int(np.log2(hz / 440)))
            note_index = int(12 * np.log2(hz / 440) / octave - 17.25 + 69)

            print(f'({self.note_names[note_index % 12]}) : {octave}')
        except OverflowError:
            pass
