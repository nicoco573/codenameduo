import random

class KeyPlayer:
    def __init__(self, player:int):
        #Liste de mots qui sert de "dictionnaire" pour le jeux (liste donnée par chat gpt parce que ça serait trop long à la main de choisir autant de mots)
        self.all_words = [
                        # 🌍 Lieux
                        "plage", "forêt", "volcan", "désert", "château", "temple", "ville", "village",
                        "montagne", "océan", "lune", "école", "musée", "prison", "cirque", "cimetière",
                        "bibliothèque", "hôpital", "supermarché", "île", "ruine", "métro", "château-fort",
                        "paradis", "enfer", "bunker", "train", "aéroport", "toit", "cave", "pont",

                        # 🧍 Personnes / métiers
                        "pirate", "roi", "reine", "chevalier", "docteur", "professeur", "voleur", "magicien",
                        "espion", "ninja", "robot", "sorcière", "astronaute", "policier", "pompier", "cuisinier",
                        "scientifique", "rockstar", "zombie", "vampire", "fantôme", "clown", "samouraï",
                        "super-héros", "moine", "cowboy", "pharaon", "gladiateur", "artiste",

                        # 🦁 Animaux
                        "chat", "chien", "poule", "vache", "lion", "tigre", "singe", "poisson", "requin",
                        "narval", "serpent", "aigle", "hibou", "éléphant", "dauphin", "ours", "panda",
                        "grenouille", "tortue", "renard", "loup", "mouton", "pieuvre", "crabe", "kangourou",
                        "dragon", "licorne", "chameau", "raton-laveur", "fourmi",

                        # 🪩 Objets
                        "épée", "bouclier", "ordinateur", "voiture", "balle", "bouteille", "clé", "téléphone",
                        "livre", "lampe", "montre", "chaussure", "casque", "sac", "miroir", "crayon", "fusée",
                        "piano", "guitare", "bombe", "arc", "canapé", "table", "chaise", "épingle", "couronne",
                        "boussole", "caméra", "balai", "parapluie", "masque", "lunettes", "chocolat", "potion",

                        # ⚡ Concepts / idées / émotions
                        "amour", "haine", "colère", "joie", "tristesse", "courage", "espoir", "magie",
                        "temps", "ombre", "lumière", "silence", "rêve", "peur", "foudre", "orage", "tempête",
                        "destin", "gloire", "vengeance", "paix", "folie", "mystère", "mensonge", "vérité",
                        "trahison", "justice", "malédiction", "souvenir",

                        # 🍔 Nourriture
                        "pizza", "burger", "frites", "pomme", "banane", "glace", "chocolat", "croissant",
                        "fromage", "pain", "steak", "crêpe", "sushi", "tacos", "riz", "pâtes", "carotte",
                        "eau", "café", "jus", "thé", "citron", "piment", "sel", "poivre",

                        # 💥 Divers fun
                        "explosion", "danse", "internet", "robot", "jeu", "musique", "film", "magie", "portail",
                        "portail", "énergie", "pixel", "laser", "comète", "trou-noir", "arc-en-ciel", "ninja",
                        "pokémon", "zombie", "bataille", "supernova", "miroir", "illusion", "portail", "glitch",
                        "succès", "fail", "chaos", "cosmos", "fusion", "éclipse"
                    ]
        
        self.player = player
        
        self.agents :list[str] | None = None
        self.assassin :str | None = None
        
        self.loose :bool = False    #Joueur perdu ou non
        self.win :bool = False      #Joueur gagné ou non
        self.point :int = 0         #Points du joueur
    
    def choose_agents(self):
        """L'ordinateur choisit aléatoirement 4 agents et 1 assassin parmi la liste de mots, le jouer qui doit les trouver ne les voit pas"""
        self.agents = []
        already_choose = []
        while len(self.agents) != 4:
            choice = random.choice(self.all_words)
            if choice not in already_choose:
                self.agents.append(choice)
                already_choose.append(choice)
        
        while not self.assassin:
            choice = random.choice(self.all_words)
            if choice not in already_choose:
                self.assassin = choice

                already_choose.append(choice)
