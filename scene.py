import tkinter as tkint

from keyplayer import KeyPlayer
from gameboard import GameBoard


class Scene:
    
    def __init__(self, canva:tkint.Canvas, name:str, width:int, height:int, clue=None):
        self.canva :tkint.Canvas = canva       
        self.gameboard :GameBoard = GameBoard(KeyPlayer(1),KeyPlayer(2))    # initialisation du gameboard
        self.gameboard.scene = self                                         # scene du gameboard
        
        # -- Paramètres de la fenêtre --
        self.witdh = width
        self.height = height
        
        self.window = tkint.Tk(className="CodeName")    #initialisation de la fenêtre tkinter
        self.window.geometry(f"{width}x{height}")       #taille de la fenêtre
        
        self.canva :tkint.Canvas = tkint.Canvas(self.window, width=width, height=height, background="ivory")    # création du canva
        self.canva.pack()   # affiche le canva
        
        # -- Scène actuelle, celle qui s'affiche --
        self.current_scene :Scene = Scene(self.canva, self, "menu") # Scène acctuelle et initialisation de la scene. (Commence au menu)
        
        self.name = name                                            # Nom de la scène
        
        self.clue :str | None = clue                                # Indice donné par le joueur actif


    def update(self):
        """Met à jour l'affichage, efface/redessine affin d'afficher les bonnes choses"""
        self.canva.delete("all")    #efface tous les éléments présents sur le canva

        self.current_scene.draw()   #dessine les nouveaux éléments
    
    def draw(self):
        """Dessine la scène"""
        elements = self.scene_elements()#récupère chaques élément de la scène sous forme de liste
        for draw in elements:           #parcour des éléments de la scène
            draw                        #dessine chaque éléments
    
    def change_scene(self, new_name:str):
        """change le nom de la scène"""
        print(new_name)
        self.name = new_name                #change le nom de la scene
        self.gameboard.destroy_widgets()    #détruit les widgets du gameboard
        self.update_current_scene(new_name)         #initialise self.current_scene dans la classe screen
        self.screen.update()                #Dessine la nouvelle scene
    
    def update_current_scene(self, name:str):
        """Met à jour la scène acctuelle"""
        self.current_scene = name
    
    def scene_elements(self):
        """Contient les éléments de chaques scènes à afficher
        
        Returns:
            list: liste des éléments à afficher
        """
        # -- MENU --
        if self.name == "menu": #Scène menu
            return [
                self.canva.create_rectangle(0, 0, 640, 480, fill="lightblue"),
                self.canva.create_text((320,210), text="CodeName Duo", font=("Lucida Handwriting", 30), anchor="center"),
                self.canva.create_window((320,380), window=tkint.Button(self.canva, text="Jouer",font=("Arial", 20,"bold"),command=lambda: self.change_scene("regles")), anchor="n"),
            ]
        
        # -- REGLES --
        elif self.name == "regles": #Scène expliquant les rêgles
            return [
                self.canva.create_rectangle(0, 0, 640, 480, fill="lightblue"),
                self.canva.create_text(20,20, fill="red",font=("Arial",20,"bold"), text="Comment jouer ?", anchor="nw"),
                self.canva.create_text(
                                    (20,210), 
                                    fill="darkblue", 
                                    text= "Les deux joueurs voient la même grille de 25 mots,\nchacun a sa propre clé secrète indiquant quels mots il doit faire deviner.\nÀ ton tour de donner un indice:\nclique sur « Voir ma clé » pendant que ton partenaire détourne les yeux,\nchoisis un seul mot pour l'aider à trouver tes agents.\nL'autre joueur clique sur les mots qu'il pense corrects : attention aux assassins !\nEnsuite, échangez les rôles et continuez jusqu'à avoir trouvé tous les agents \navant la fin du nombre de tours imposés.\nLe tour se termine lorsque une erreur est commise et la partie est perdue si l'assassin est choisi.",
                                    font=("Arial", 10), 
                                    anchor="sw"
                                ),
                self.canva.create_window((320,380), window=tkint.Button(self.canva, text="Suivant",font=("Arial", 20, 'bold'),command=lambda: self.change_scene("game1")), anchor="n"),
            ]
        
        
        # -- GAME 1 --
        elif self.name == "game1": #Scène du jeu : joueur 1
            # print(self.gameboard.player1.loose)
            print(self.gameboard.player2.win)
            
            # -- PERTE DU JOUEUR 2 --
            if self.gameboard.player2.loose:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_text((300, 300), text="Vous avez perdu !\nC'est au joueur 1 de jouer.\nFaite le deviner !", font=("Arial", 27, "bold"), fill="red", anchor="s"),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 2: clé", font=("Arial", 10), command=lambda: self.change_scene("key2")))
                ]
            
            # -- VICTOIRE DU JOUEUR 2 --
            elif self.gameboard.player2.win:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_text((300, 300), text="Vous avez trouvé tous vos agents !\nC'est au joueur 1 de jouer.\nFaite le deviner !", font=("Arial", 27, "bold"), fill="green", anchor="s"),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 2: clé", font=("Arial", 10), command=lambda: self.change_scene("key2")))
                ]
            
            # -- TRUC DE BASE --
            else:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.gameboard.create_cards(self.canva, 2),
                    self.canva.create_text((20, 430), text="Joueur 2, devine !", font=("Arial", 12), anchor="sw", fill='green'),
                    self.canva.create_text((20, 455), text=f"Indice : {self.clue if self.clue else 'Aucun Indice, regardez la clé !'}", font=("Arial", 15,'bold'), anchor="sw", fill='blue'),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 2: clé", font=("Arial", 10), command=lambda: self.change_scene("key2"))),
                ]
        
        # -- CLE DU JOUEUR 1 --
        elif self.name == "key1": #Scène de la clé du joueur 1
            entree_indice = tkint.Entry(self.canva, font=("Arial", 12), width=20)
            self.gameboard.widgets.append(entree_indice)
            return [
                self.canva.create_rectangle((0,0),(640,480), fill="lightgrey"),
                self.canva.create_text((320,30), text="Clé du Joueur 1", font=("Arial", 20, "bold"), anchor="n"),
                self.gameboard.display_key(1),
                entree_indice.place(x= 320, y= 410, anchor="s"),
                self.canva.create_window((320,450), anchor="s", window=tkint.Button(self.canva, text="Valider", font=("Arial", 10), command= lambda: self.get_entry(entree_indice))),
                self.canva.create_text((320, 380), text="Entrez votre indice: ", font=("Arial", 11), anchor="s", fill='blue', justify="left")
            ]
        
        
        # -- GAME 2 --
        elif self.name == "game2": #Scène du jeu : joueur 2
            print(self.gameboard.player1.win)
            
            # -- PERTE DU JOUEUR 1 --
            if self.gameboard.player1.loose:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_text((300, 300), text="Vous avez perdu !\nC'est au joueur 2 de jouer.\nFaite le deviner !", font=("Arial", 27, "bold"), fill="red", anchor="s"),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 1: clé", font=("Arial", 10), command=lambda: self.change_scene("key1")))
                ]
            
            # -- VICTOIRE DU JOUEUR 1 --
            elif self.gameboard.player1.win:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_text((300, 300), text="Vous avez trouvé tous vos agents !\nC'est au joueur 2 de jouer.\nFaite le deviner !", font=("Arial", 27, "bold"), fill="green", anchor="s"),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 1: clé", font=("Arial", 10), command=lambda: self.change_scene("key1")))
                ]
                
            # -- TRUC DE BASE --
            else:
                return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.gameboard.create_cards(self.canva, 1),
                    self.canva.create_text((20, 430), text="Joueur 1, devine !", font=("Arial", 12), anchor="sw", fill='green'),
                    self.canva.create_text((20, 455), text=f"Indice : {self.clue if self.clue else 'Aucun Indice, regardez la clé !'}", font=("Arial", 15,'bold'), anchor="sw", fill='blue'),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 1: clé", font=("Arial", 10), command=lambda: self.change_scene("key1"))),
                ]
        
        
        
        # -- CLE DU JOUEUR 2 --
        elif self.name == "key2": #Scène de la clé du joueur 2
            entree_indice = tkint.Entry(self.canva, font=("Arial", 12), width=20)
            self.gameboard.widgets.append(entree_indice)
            return [
                self.canva.create_rectangle((0,0),(640,480), fill="lightgrey"),
                self.canva.create_text((320,30), text="Clé du Joueur 2", font=("Arial", 20, "bold"), anchor="n"),
                self.gameboard.display_key(2),
                entree_indice.place(x= 320, y= 410, anchor="s"),
                self.canva.create_window((320,450), anchor="s", window=tkint.Button(self.canva, text="Valider", font=("Arial", 10), command= lambda: self.get_entry(entree_indice))),
                self.canva.create_text((320, 380), text="Entrez votre indice: ", font=("Arial", 11), anchor="s", justify="left", fill='blue')
            ]
        
        
        # -- ERREUR COMMISE PAR LE JOUEUR 1 --
        elif self.name == "mistake1":
            return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 1: clé", font=("Arial", 10), command=lambda: self.change_scene("key1"))),
                    self.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info"),
                    self.canva.create_text((320, 460), text="Tu t'es trompé !\nFin de ton tour.", font=("Arial", 15), fill="red", tag="info")
                ]
        
        
        # -- ERREUR COMMISE PAR LE JOUEUR 2 --
        elif self.name == "mistake2":
            return [
                    self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                    self.canva.create_text((20, 455), text=f"Indice : {self.clue if self.clue else 'Aucun Indice, regardez la clé !'}", font=("Arial", 15,'bold'), anchor="sw", fill='blue'),
                    self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 2: clé", font=("Arial", 10), command=lambda: self.change_scene("key2"))),
                    self.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info"),
                    self.canva.create_text((320, 460), text="Tu t'es trompé !\nFin de ton tour.", font=("Arial", 15), fill="red", tag="info")
                ]
        
        # -- PERTE DU JOUEUR 1 --
        elif self.name == "loose1":
            return [
                self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                self.canva.create_text((300, 300), text="Vous avez perdu !\nL'assassin à été choisi", font=("Arial", 27, "bold"), fill="red", anchor="s"),
                self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 1: clé", font=("Arial", 10), command=lambda: self.change_scene("key1")))
            ]
        
        # -- PERTE DU JOUEUR 2 --
        elif self.name == "loose2":
            return [
                self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                self.canva.create_text((300, 300), text="Vous avez perdu !\nL'assassin à été choisi", font=("Arial", 27, "bold"), fill="red", anchor="s"),
                self.canva.create_window((620, 440), anchor="se", window=tkint.Button(self.canva, text="Joueur 2: clé", font=("Arial", 10), command=lambda: self.change_scene("key2")))
            ]
        
        elif self.name == "endgame":
            if self.gameboard.player1.point == 4 and self.gameboard.player2.point == 4:
                message = "Félicitations !\nVous avez tout deux gagné la partie !"
            elif self.gameboard.player1.loose == True and self.gameboard.player2.loose == True:
                message = "Les 2 joueurs ont perdu !\Vous ferez mieux la prochaine fois !"
            
            return [
                self.canva.create_rectangle((0,0),(640,480), fill="lightblue"),
                self.canva.create_text((320, 240), text=f"{message}", font=("Arial", 27, "bold"), fill="green", anchor="center"),
            ]
        else:
            return []
    
    
    def get_entry(self, entry:tkint.Entry):
        """Récupère le texte entré dans l'Entry et change de scène"""
        
        # Limite la triche, malheureusement ne l'empêche pas.
        self.clue = entry.get()
        for word in self.gameboard.words_in_game:
            if self.clue in word or len(self.clue) > 15 or " " in self.clue:
                self.canva.create_text((410, 450), text="Indice non valide veuillez changer", font=("Arial", 10), fill="red", anchor="sw")
                return  # quitte la fonction, attend que l'utilisateur clique à nouveau
        if self.name == "key1":
            self.change_scene("game1")
        
        elif self.name == "key2":
            self.change_scene("game2")


