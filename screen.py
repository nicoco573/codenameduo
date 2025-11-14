import tkinter as tkint

from scene import Scene

class Screen:
    def __init__(self, width:int, height:int):
        self.witdh = width
        self.height = height
        
        self.window = tkint.Tk(className="CodeName")    #initialisation de la fenêtre tkinter
        self.window.geometry(f"{width}x{height}")       #taille de la fenêtre
        
        self.canva :tkint.Canvas = tkint.Canvas(self.window, width=width, height=height, background="ivory")
        self.canva.pack()   #affiche le canva
        
        self.current_scene :Scene = Scene(self.canva, self, "menu") #scène acctuelle, celle qui s'affiche
    
    def update(self):
        """Met à jour l'affichage, efface/redessine affin d'afficher les bonnes choses"""
        self.canva.delete("all")    #efface tous les éléments présents sur le canva
        self.current_scene.draw()   #dessine les nouveaux éléments