import random
import tkinter as tkint
from keyplayer import KeyPlayer

class GameBoard:
    def __init__(self, player1:KeyPlayer, player2:KeyPlayer, scene):
        self.player1 :KeyPlayer = player1
        self.player2 :KeyPlayer = player2
        
        self.scene = scene
        
        self.words_in_game :list[str] | None = None
        
        self.widgets :list = []
        
        self.cards :list[dict] = []
        
        # print("NOUVEAU GAMEBOARD CRÉÉ")
    
    def init_words_in_game(self):
        """Créer toutes les cartes(mots) nécessaires pour avoir un plateau de jeu complet"""
        self.player1.choose_agents()
        self.player2.choose_agents()
        
        required_words = []
        
        for i in range(4):
            required_words.append(self.player1.agents[i])
            required_words.append(self.player2.agents[i])
        
        required_words.append(self.player1.assassin)
        required_words.append(self.player2.assassin)
        
        while len(required_words) != 25:
            word = random.choice(self.player1.all_words)
            if word not in required_words:
                required_words.append(word)
        
            for i in range(len(required_words)):
                if required_words.count(required_words[i]) > 1:
                    required_words.remove(required_words[i])
            
        
        random.shuffle(required_words)
        self.words_in_game = required_words
        # print(self.words_in_game)
    
    def create_cards(self, canva:tkint.Canvas, player:int):
        """Créer les cartes(mots) du plateau de jeu"""
        if self.words_in_game is None:
            self.init_words_in_game()
        
        
        x = 50
        y = 50
        line = 0
        for i in range(0,len(self.words_in_game)):
            line += 1
            if i <= len(self.words_in_game):
                canva.create_window(
                                    (x,y),
                                    window=tkint.Button(
                                        canva,
                                        text=self.words_in_game[i],
                                        font=("Arial", 9),
                                        command=lambda w=self.words_in_game[i], idx=i: self.Click_Button(w, idx, player)
                                    ),
                                    anchor="nw",
                                    width=80,
                                    height=50
                                )
                
                if len(self.cards) < 25:
                    card = {
                        "word": self.words_in_game[i],
                        "found_by": []
                    }
                    self.cards.append(card)
                x += 95
                if line % 5 == 0:
                    y += 75
                    x = 50
        
        # print(cards)
    
    def display_key(self,player:int):
        """Affiche la clé du joueur demandé"""
        if player == 1:
            key_player = self.player1
        elif player == 2:
            key_player = self.player2
        
        # print(key_player.agents)
        # print(self.player1.agents)
        agents = tkint.Label(font=('Arial', 13), text=f"Agents à faire deviner:\n- {key_player.agents[0]}\n- {key_player.agents[1]}\n- {key_player.agents[2]}\n- {key_player.agents[3]}", background='lightgrey', fg='green', justify='left')
        self.widgets.append(agents)
        agents.place(x=50,y=100,anchor='nw')
        assassin = tkint.Label(font=('Arial', 13), text=f"Assassin:\n- {key_player.assassin}", background='lightgrey', fg='red', justify='left')
        self.widgets.append(assassin)
        assassin.place(x=300,y=100,anchor='nw')
    
    
    def destroy_widgets(self):
        """Détruit les widgets crées par le gameboard"""
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
    
    
    def Click_Button(self, word:str, index:int, player:int):
        """Gère le clic sur une carte(mot)"""
        # print(f"Carte cliquée: {word}")
        if player == 1:
            if self.player2.point == 4:
                self.player2.win = True
                self.scene.change_scene("game2")
            if 1 not in self.cards[index]["found_by"]:
                self.cards[index]["found_by"].append(1)
            else:
                self.scene.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info")
                self.scene.canva.create_text((320, 460), text="Carte déjà testée", font=("Arial", 15), fill="red", tag="info")
                # print("Carte déjà testée")
                return
            
            if word in self.player2.agents:
                self.scene.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info")
                self.scene.canva.create_text((320, 460), text="Bravo !", font=("Arial", 15,'bold'), fill="green", tag="info")
                self.player1.point += 1
                print(self.player1.point)
                
            
            elif word == self.player2.assassin:
                self.player1.loose = True
                # print("ASSASSIN")
                self.scene.change_scene("loose1")
            else:
                self.scene.change_scene("mistake1")
                
        elif player == 2:
            if self.player1.point == 4:
                self.player1.win = True
                self.scene.change_scene("game1")
            if 2 not in self.cards[index]["found_by"]:
                self.cards[index]["found_by"].append(2)
            else:
                self.scene.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info")
                self.scene.canva.create_text((320, 460), text="Carte déjà testée", font=("Arial", 15), fill="red", tag="info")
                # print("Carte déjà testée")
                return
            
            if word in self.player1.agents:
                self.scene.canva.create_rectangle((220,440),(420,480), fill="lightgrey", tag="info")
                self.scene.canva.create_text((320, 460), text="Bravo !", font=("Arial", 15,'bold'), fill="green", tag="info")
                self.player2.point += 1
                print(self.player2.point)
                
            
            elif word == self.player1.assassin:
                self.player2.loose = True
                # print("ASSASSIN")
                self.scene.change_scene("loose2")
            else:
                self.scene.change_scene("mistake2")
            
            # Conditions d'arrêt du jeux
            if self.player1.point == 4 and self.player2.point == 4:
                self.scene.change_scene("endgame")
            elif self.player1.loose and self.player2.loose:
                self.scene.change_scene("endgame")
