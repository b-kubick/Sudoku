import pygame
import sudokuGUI
import tkinter
from tkinter import *
from tkinter import ttk


class OptionsWindow:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Sudoku")

        self.difficulty = 0
        self.font = pygame.font.Font(None, 36)
        self.diff_texts = ["Easy", "Medium", "Hard"]
        self.default_colors = [(50, 200, 50), (200, 200, 50), (200, 50, 50)]
        self.hover_colors = [(100, 255, 100), (255, 255, 100), (255, 100, 100)]
        self.button_rects = [pygame.Rect(150, 100 + i * 70, 100, 50) for i in range(3)]

        self.main_loop()

    def draw_text(self, text, pos, color, size):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.win.blit(text_surface, text_rect)

    def draw_buttons(self):
        for i, button_rect in enumerate(self.button_rects):
            button_color = self.default_colors[i]
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = self.hover_colors[i]

            pygame.draw.rect(self.win, button_color, button_rect)
            self.draw_text(self.diff_texts[i], button_rect.center, (0, 0, 0), 24)

    def main_loop(self):
        running = True
        while running:
            self.win.fill((255, 255, 255))  # Clear the screen

            title_pos = (200, 30)
            subtitle_pos = (200, 70)
            self.draw_text("Sudoku", title_pos, (0, 0, 0), 48)
            self.draw_text("Choose your difficulty", subtitle_pos, (100, 100, 100), 18)

            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button_rect in enumerate(self.button_rects):
                        if button_rect.collidepoint(mouse_pos):
                            self.difficulty = i
                            difficulty_str = ["Easy", "Medium", "Hard"][self.difficulty]
                            sudokuGUI.start_game(difficulty_str)  # Assuming this function starts the game
                            running = False  # Exit the loop to start the game

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    OptionsWindow().run()
