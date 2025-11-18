from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()                      #lance le jeux

    game.screen.window.mainloop()   #Boucle principale tkinter
