import tkinter as tkint

from screen import Screen


class Game:
    def __init__(self):
        self.running = True
        self.screen = Screen(640, 480)
    
    
    def close_window(self):
        """Ferme le programme"""
        self.running = False            #arrete la mise à jour de l'affichage
        self.screen.window.destroy()    #Ferme la fenêtre
    
    
    def run(self):
        """Lance le programme"""
        self.screen.window.protocol("WM_DELETE_WINDOW", self.close_window)  # Appelle la fonction quand on ferme la fenêtre
        if self.running:
            self.screen.update()    #Met à jour l'affichage
