from sources.Interface.app import Application
'''
Si main.py existe c'est car il s'occupe d'initialiser l'application.
Mais surtout ce fichier fait en sorte que chaque fichier part de
l'emplacement où se trouve celui-ci lorsqu'il cherche une ou des ressources
Permettant d'éviter de se troubler lors d'une recherche d'une ou des ressources 
puisque tout part d'ici.
'''
app = Application() 
app.run()   #démarre la boucle de Tkinter qui s'occuperra du reste