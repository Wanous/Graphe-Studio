import configparser

class INI:
    def __init__(self,master,fichier):
        self.master=master
        self.fichier=fichier

    def lire(self):
        '''
        Méthode qui lis un fichier .ini mise en paramètre et retourne le contenu
        '''
        #La bibliothèque permet d'analyser le fichier comme s'il s'agissait d'un dictionnaire
        config = configparser.ConfigParser()
        config.read(self.fichier)
        return config
    
    def sauvegarder(self,preferences):
        '''
        Méthode qui applique des modifications au fichier mis en paramètre
        avec des données qui sont eux aussi un paramètre de la méthode
        
        paramètres :
            preferences(list) : liste des changements à sauvegarder
        '''
        with open(self.fichier, 'w') as configfile:
            preferences.write(configfile)
    
    def modifier(self,section,cle,valeur):
        '''
        Méthode qui va mettre en oeuvre la modifications du fichier en passant par d'autre méthodes
        '''
        preferences = self.lire()
        preferences[section][cle] = valeur
        self.sauvegarder(preferences)
    
    def charger(self):
        '''
        Méthode qui lis un fichier .ini mise en paramètre et charge le contenu
        pour être utilisées dans le logiciel 
        '''
        fichier=self.lire() #lis le fichier
        configuration={}
        
        for section in fichier :
            configuration[section]={}
            for element in fichier[section] :
                configuration[section][element]=fichier[section][element] 
        
        del configuration['DEFAULT']#indice 0 est destiné à une clé 'DEFAULT' qui ne sert à rien
        
        return configuration
             
        
    