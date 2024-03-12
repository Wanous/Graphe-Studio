from random import randint
graphe = { 'A': {'coords': (-220,220), 'next': {'B': 140, 'E': 200, 'F': 200}}, 
            'B': {'coords': (110,86), 'next': {'A': 140, 'C': 260, 'F': 140}}, 
            'C': {'coords': (-35,-51), 'next': {'B': 260, 'D': 360}}, 
            'D': {'coords': (-100,-150), 'next': {'C': 360, 'F': 280}}, 
            'E': {'coords': ( 260,-100), 'next': {'A': 200, 'F': 120}}, 
            'F': {'coords': (-15,115), 'next': {'A': 200, 'B': 140, 'D': 280, 'E': 120}} }



class Graphe :
    def __init__(self,master=None):
        self.master=master
        self.commandes=commande
        self.graphe={}
        self.type=None
    
    def initialisation(self,type_arbre):
        if type_arbre == 'Graphe_O':
            self.type = 'Graphe_O'
        elif type_arbre == 'Graphe_NO':
            self.type = 'Graphe_O'
        elif type_arbre == 'Arbre_B':
            self.type = 'Arbre_B'
        else:
            return False
        return True

    def ajouter_elements(self):
        self.graphe['G']={'coords': (60, 70), 'next': {'A': 200, 'B': 140, 'D': 280, 'E': 120}}
        return True

    def aleatoire(self):
        graphe={}
        nb_noeud=randint(10,20)
        if self.master!=None:limite=self.master.size/2
        else:limite=250
        for i in range(nb_noeud):
            graphe[f'{i}']={}
            graphe[f'{i}']['coords']=(randint(-250,250), randint(-250,250))
            graphe[f'{i}']['next']={str(0+randint(0,i)): None}
            
        self.graphe=graphe
        return True

class Graphe_Oriente:
    def CREER_SOMMET(graphe,nom):
        pass

commande={'Graphe_O':{'CREER_SOMMET':{'fonction':Graphe_Oriente.CREER_SOMMET,
                                      'parametre':[int,int,list],
                                      'message_réussite':"Sommet ajouté",
                                      'message_erreur':""},
                      'CREER_ARC':{}},
          'Graphe_NO':{'CREER_SOMMET':{},
                       'CREER_ARETE':{}},
          'Arbre_B':{'CREER_SOMMET':{}}}

#test:
# Graphe_O()
# CREER_SOMMET(24,35,['A','B','C'])

if __name__ == "__main__":
    graphe=Graphe()
    graphe.aleatoire()
    print(graphe.graphe)


