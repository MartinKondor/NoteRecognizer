import pygame as pg

from threading import Thread
from src.config import *
from src.note_recognizer import NoteRecognizer


class Display:
    
    def __init__(self):
        self.note_rec = NoteRecognizer()
        self.line_height = WINDOW_HEIGHT / 12
        self.octave = 1
        self.sound_thread = None
        font = pg.font.SysFont('Arial', int(self.line_height / 2))
        color_constant = 255 / 12
        
        self.note_texts = [font.render(n, False, (249, 249, 249)) for n in self.note_rec.note_names]
        self.pitch_lines = [
            ((37, 37, 255 - i * color_constant,), (0, i * (self.line_height), WINDOW_WIDTH, self.line_height + 1)) for i in range(12)
            #((i * color_constant, i * color_constant, i * color_constant,), (0, i * (self.line_height), WINDOW_WIDTH, self.line_height + 1)) for i in range(12)
        ]

    def display(self, screen):
        mouse_pos = pg.mouse.get_pos()

        for i, (pitch_lines_color, pitch_line_coords,) in enumerate(self.pitch_lines):
            pg.draw.rect(screen, pitch_lines_color, pitch_line_coords)

            if mouse_pos[0] > 0 and mouse_pos[1] > i * self.line_height and mouse_pos[0] < WINDOW_WIDTH and \
                mouse_pos[1] < i * self.line_height + self.line_height and pg.mouse.get_pressed()[0]:

                pg.draw.rect(screen, [c * 0.8 for c in pitch_lines_color], pitch_line_coords)
                # freq = int(440 * 2 ** ((self.octave * 17.25 + i - 69) / 12))

                # Middle C: 261.625565
                # Middle B: 493.88
                # freq = i * (493.88 - 261.625565) / 12
                # print(freq)

            text_coords = (pitch_line_coords[0] + WINDOW_WIDTH / 2 - len(self.note_rec.note_names[i]) * 3, pitch_line_coords[1],)
            screen.blit(self.note_texts[i], text_coords)

        # Get and display current freqvency
        freq = self.note_rec.update()

        if freq != 0:
            # print(freq)
            pass

    def close(self):
        self.note_rec.close()
