import tkinter as tk
from tkinter import ttk

class Table:
    """
    Classe qui s'occupe de crée et de s'occuper d'un Tableur qui permet l'affichage des informations
    du graphe tel que le nom,les coordonnées ainsi que les adjacents d'un noeud voir plus...
    Elle permet un accés direct,simple et pratique aux informations pour l'utilisateur 
    """
    def __init__(self, master,**kwargs):
        self.master = master                                  #Fenêtre Principale
        self.graphe=self.master.Graphe.graphe                 #Extraction du graphe 
        self.configuration=self.master.configuration['tableur'] #configuration/preferences du tableur 
        self.is_open=False                                    #Ouvrir/Fermer tous les onglets
        
        
        self.frame = tk.Frame(self.master)                    #widget contenant le tableur
        self.tree = ttk.Treeview(self.frame,selectmode='none')#wdget tableur

        self.cree_tableur()                                   #mise en place des valeurs du tableau  
                              
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')          #barre de scroll du tableur (si il y a beaucoup de noeud)

        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(expand=True,fill=tk.BOTH)
        
        self.changer_couleur()
        self.tree.bind('<ButtonRelease-1>', self.montrer_tous) #case modifier pour qu'elle agisse comme un bouton (coorespond à la troisième ligne du tableur)

    def changer_couleur(self):
        """
        Cette méthode prend une chaîne de caractères est sa fonction est de changer la couleur des 
        éléments du tableur (généralement appelé dans app.py)
        
        Paramètres:
        couleur (str): Le code d'une couleur en hexadécimal 
        """
         
        noeuds=list(self.graphe.keys())
        if self.configuration['ordre_alphabetique']=='True':
            noeuds.sort()
        for n in range(len(self.graphe)):
                        couleur=self.graphe[noeuds[n]]['couleur']
                        tag=self.tree.item(n+1)["tags"][0]
                        if self.configuration['couleur_noeud']=='True':
                            self.tree.tag_configure(tag, background = couleur)
                        else :
                            self.tree.tag_configure(tag, background = self.configuration['couleur']) 
      
    def montrer_tous(self,event):
        """
        Cette méthode prend un événement Tkinter en entrée (ici c'est la souris) et vérifie si la seconde
        ligne du tableau d'indice 1 a été cliqué.Si oui elle affiche tout les détails de chaques noeuds présent dans le tableur 
        ou au contraire cache les détails si le 'bouton' (car ce n'est pas vraiment un bouton) a déjà été préssé d'où
        la présence de self.is_open
        
        Paramètres:
        event (class): Le bouton de la souris 
        (ne sert pas vraiment mais Tkinter oblige l'inclusion d'un paramètre pour les fonction relier à un événement)
        """
        iid =  self.tree.get_children()[1]
        if iid == self.tree.focus():
            if self.is_open == False :
                self.is_open=True
            else:
                self.is_open = False
                self.cellule=[False for i in range(len(self.graphe)+3)]
            self.mise_a_jour() #met à jour le tableur pour afficher/cacher les détails 

    def cree_tableur(self):
        """
        Méthode qui extrait les information d'un graphe pour les affiché dans le tableur sous la forme suivante :
               - NOM_DU_NOEUD N°1 :
                    CLEF N°1 : VALEUR CLEF N°1
                    CLEF N°2 : VALEUR CLEF N°2
                    ...
                    CLEF N°n : VALEUR CLEF N°n Avec n entier naturel qui correspond au nombre de clef d'un noeud
               - NOM_DU_NOEUD N°w :            Avec w entier naturel qui correspond au nombre de noeud d'un graphe 
                    ...
        Elle est souvent appelé pour mettre à jour le graphe 
        """
        graphe=self.master.Graphe
        self.tree.heading('#0', text='Noeuds') #Titre de la colonne                                                        
        self.tree.insert('', tk.END,text='Type : '+ 'Graphe orienté'  if graphe.type == "GrapheO" else 'Type : '+'Graphe non orienté', tags = ['type'])
        self.tree.tag_configure('type', background = '#1c1c1b' ,foreground='#ebe2d8')
        self.tree.insert('', tk.END,text='Tout montrer'  if self.is_open == False else 'Tout cacher', iid=0, tags = ['boutons'])
        self.tree.tag_configure('boutons', background = '#78f542' if self.is_open == False else '#eb432d')

        cles = list(graphe.graphe.keys()) 
        if self.configuration['ordre_alphabetique']=='True':
            cles.sort() #noeud dans l'ordre alphabétique (selon les préférences)
                                
        i=1
        for noeud in cles:
            self.tree.insert('', tk.END, text=noeud, iid=i, open=self.is_open, tags = ('Noeud'+str(i)))       #insertion des noeud comme lignes principales
            y=1
            for infos in graphe.graphe[noeud].keys():                                                  #insertion des clefs et valeurs comme lignes secondaire de la clef(noeud/lignes principales) lui correspondant
                cle=list(graphe.graphe[noeud].keys())[y-1]
                valeur=graphe.graphe[noeud][infos]
                if graphe.type == 'GrapheNO': #pour les graphes non orientés
                    self.tree.insert('', tk.END, text=f'{cle} : {valeur}', iid=noeud+cle, tags = ['infos'])#noeud+cle permet un id unique à chaque sous-lignes secondaire
                    self.tree.move(noeud+cle, i, y)                                                        #cela permet de ne pas avoir de soucis dans l'insertion des
                                                                                                           #informations pour les autres noeud par duplication des id qui est interdit par Tkinter
                else:
                    if cle == 'adjacent':    #pour les graphes orientés
                        self.tree.insert('', tk.END, text=f'degrée sortant : {valeur}', iid=noeud+cle, tags = ['infos'])
                        self.tree.move(noeud+cle, i, y)
                        liste =[]
                        for noeuds in graphe.graphe :
                             if noeud in graphe.graphe[noeuds]['adjacent'] :
                                  liste.append(noeuds)
                        self.tree.insert('', tk.END, text=f'degrée entrant : {liste}', iid=noeud+cle+'1', tags = ['infos'])
                        self.tree.move(noeud+cle+'1', i, y)     
                         
                    else:
                        self.tree.insert('', tk.END, text=f'{cle} : {valeur}', iid=noeud+cle, tags = ['infos'])
                        self.tree.move(noeud+cle, i, y)                               
                y+=1                                                                                       
            i+=1  
                                                                                      
        self.changer_couleur()             #applique la couleur

    def mise_a_jour(self):
        """
        Cette méthode met à jour le graphe en supprimant les lignes du tableur avant 
        de les recrée avec les nouvelles informations.
        (Elle sont supprimé et non modifié car il y a les identifiants qui pose probléme
         et les lignes du tableur sont difficilement modifiables)
        """
        self.graphe=self.master.Graphe.graphe #recharge le graphe car pour des raisons étranges il est pas mise à jour que dans cette classe 
        for fils in self.tree.get_children():
            self.tree.delete(fils)
        self.cree_tableur()


        

