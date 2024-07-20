#utilisation de la bibliothèque pickle pour sauvegarder et charger des données dans un fichier avec n'importe quelle extension
#L'extension du fichier n'a pas d'importance pour la bibliothèque pickle, car elle traite simplement les données 
#sous forme de flux de bytes.
import pickle

#c'est une classe avec peu de ligne mais le mettre dans un fichier à part est 
#intéressant pour que le logiciel soit bien structuré 
class GRAF :
    '''
    classe qui permet de crée et intéragire avec les fichiers de format .graf
    '''
    def sauvegarder (fichier,infos):
        '''
        méthode qui prend en paramètre un chemin vers un fichier et 
        permet de sauvegarder les informations de tout type mis en paramètres 
        dans un fichiers aux format .graf
        
        paramètres :
        fichier(str) : chemin absolu vers le fichier qui doit être sauvegardé
        infos(tout type) : informations qui seront sauvegarder dans le fichier
        
        '''
        with open(fichier, "wb") as fichier:
            pickle.dump(infos, fichier)

    def charger (fichier):
        '''
        méthode qui prend en paramètre un chemin vers un fichier 
        et a pour rôle de charger les données contenu dans des fichiers aux format .graf
        paramètres :
        fichier(str) : chemin absolu vers le fichier qui doit être chargé
        
        retourne :
            de tout type : les données du fichier
        '''
        with open(fichier, "rb") as fichier:
            donnees = pickle.load(fichier)
        
        return donnees 
