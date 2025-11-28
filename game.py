import tkinter as tkint

from scene import Scene


class Game:
    def __init__(self):
        self.running = True
        self.scene = Scene(640, 480)
    
    
    def close_window(self):
        """Ferme le programme"""
        self.running = False            #arrete la mise à jour de l'affichage
        self.scene.window.destroy()    #Ferme la fenêtre
    
    
    def run(self):
        """Lance le programme"""
        self.scene.window.protocol("WM_DELETE_WINDOW", self.close_window)  # Appelle la fonction quand on ferme la fenêtre
        if self.running:
            self.scene.update()    #Met à jour l'affichage

