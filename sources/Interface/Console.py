import tkinter as tk
from tkinter import scrolledtext
from sources.Graphe.Operation import Operation_graphe

operation=[{'nom':'parcours en profondeur',
            'appelle':'parcours_profondeur',
            'commande':Operation_graphe.parcours_profondeur,
            'nb_parametre':1,
            'description':"parcours_profondeur(‘noeud’) : Permet d’afficher le parcours en longueur depuis un nœud."},
           
           {'nom':'parcours en largeur',
            'appelle':'parcours_largeur',
            'commande':Operation_graphe.parcours_chemin,
            'nb_parametre':1,
            'description':"parcours_largeur(‘noeud’) : Permet d’afficher le parcours en largeur depuis un nœud."},
           
           {'nom':'second parcours en largeur',
            'appelle':'parcours_largeur2',
            'commande':Operation_graphe.parcours_largeur,
            'nb_parametre':1,
            'description':'parcours_largeur2(‘noeud’) : Seconde commande qui Permet d’afficher le parcours en largeur depuis un nœud.'},
           
           {'nom':'Le plus court',
            'appelle':'court',
            'commande':Operation_graphe.chemins,
            'nb_parametre':2,
            'description':'court(‘début’,’fin’) : affiche le chemin le plus court entre deux noeuds'},
           
            {'nom':'matrice',
             'appelle':'matrice',
            'commande':Operation_graphe.matrice,
            'nb_parametre':0,
            'description':" matrice() : Permet de montrer la matrice d’adjacence associée au graphe "}]

class ConsoleCommande:
    """
    Classe qui s'occupe de crée et de s'occuper d'une fenêtre qui permet l'éxécution d'opérations 
    sur un graphe via des commandes .Entre autre elle permet l'intéraction entre l'utilisateur et le graphe/logiciel
    """
    def __init__(self, master):

        self.master = master
        self.operation=operation
        
        self.commandes=[]
        self.messages=[]
        self.up=0
        
        self.fenetre = tk.Toplevel(master) #fenêtre supérieur à la fenêtre principale 
        self.fenetre.title("Console de Graphe studio")
        self.widgets_console()             #initialisation des 'widget'
        self.affichage_console()           #affichage des 'widget'
        
    def widgets_console(self):
        """
        Méthode qui produit l'initialisation des widgets et événements de la console ,elle existe pour rendre le programme mieux structuré
        """
        self.zone_texte = scrolledtext.ScrolledText(self.fenetre,font=("Arial 11"),wrap=tk.WORD, width=57, height=28, background="black", foreground="white")
        self.zone_texte.config(state=tk.DISABLED)         #désactive le droit de l'utilisateur de modifier la zone de texte

        self.saisie = tk.Entry(self.fenetre,text="En attente d'une commande...", width=68)
        self.saisie.bind('<Return>',self.envoyer_commande)#Appuyez sur entrée envoie le message
        self.saisie.bind('<KeyRelease>',self.raccourci_clavier)  #événement Pour les raccourcies clavier

        self.bouton_envoyer = tk.Button(self.fenetre, text="Envoyer", command=self.envoyer_commande,width=10,height=2 ,anchor='nw') 
    
    def affichage_console(self):
        """
        Méthode qui gére le placement dans l'affichage des widgets ,elle existe pour rendre le programme mieux structuré
        """
        self.saisie.pack(side=tk.BOTTOM,fill='x',ipady=6) #champ de saisie
        self.zone_texte.pack(expand=True,fill=tk.BOTH)    #La console

    def envoyer_commande(self,event=None):
        """
        Cette méthode prend un événement Tkinter en entrée (mais ce n'est pas utile) et est éxécuté si la touche 'entrée'
        à été préssée .Elle permet de prendre en compte la saisie de l'utilisateur et de l'afficher sur la console
        avant de la traiter par la méthode 'decrypte'
        
        Paramètres:
        event (class): La touche préssée
        (ne sert pas vraiment mais Tkinter oblige l'inclusion d'un paramètre pour les fonction relier à un événement)
        """
        message = self.saisie.get()#si la saisie n'est pas vide
        if message:
            self.zone_texte.config(state=tk.NORMAL)
            self.zone_texte.insert(tk.END, f">>> {message}\n")
            
            self.commandes.append(message)   #c'est pour réutiliser les commande avec la fléche du haut et pour d'autres besoins
            self.decrypte()

            self.saisie.delete(0, tk.END)    #supprime le texte du champ de saisie pour laisser place à de nouvelles commandes
            self.zone_texte.config(state=tk.DISABLED)
            
            self.zone_texte.yview_moveto(1.0)#permet de descendre automatiquement la bar de scroll si la limite visible est dépassé
                                             #ça évite que l'utilisateur le fasse à chaque nouvelle commande/message
    
    def envoyer_message(self,message):
        """
        Cette méthode prend une chaîne de caractères en entrée et affiche le message dans 
        La console .
        
        Paramètres:
        message (str): Le message qui doit être affiché
        """
        self.zone_texte.config(state=tk.NORMAL)
        self.zone_texte.insert(tk.END, f"{message}\n")
        self.zone_texte.config(state=tk.DISABLED)
        self.zone_texte.yview_moveto(1.0)

    def raccourci_clavier(self,event):
        """
        Cette méthode prend un événement Tkinter en entrée et selon l'événement une action 
        est produite . 
        
        Paramètres:
        event (class): La touche préssée
        """
        
        #Fléche du haut pour réutiliser la commande précedante(peut s'accumulé)
        if event.keysym == 'Up' : 
            self.up+=1 #ceci permet d'éviter de dépasser la longueur de la liste 
            if self.up<=len(self.commandes):
                self.saisie.delete(0, tk.END)
                self.saisie.insert(tk.END,self.commandes[-self.up])
        else :
            self.up=0

        #Fléche droite pour supprimer le texte du champ de saisie
        if event.keysym == 'Down' : 
            self.saisie.delete(0, tk.END)

        #ferme automatiquement les parenthèses
        elif event.keysym == 'parenleft':
            self.saisie.insert(self.saisie.index(tk.INSERT),")") #insert la parenthèses la où se situe le curseur
            self.saisie.icursor(self.saisie.index(tk.INSERT)-1)    #remet le curseur à l'endroit initiale (car l'ajout le décal)

        #ferme automatiquement les guillemets
        elif event.keysym == 'quotedbl':
            self.saisie.insert(self.saisie.index(tk.INSERT),'"') #insert la guillemet la où se situe le curseur
            self.saisie.icursor(self.saisie.index(tk.INSERT)-1)   
        
    def decrypte(self):
        """
        Cette méthode permet d'éxécuter la commande saisie par l'utilisateur si elle est valide
        """
        commande='' #str qui contiendra la commande
        parametre=''#str qui contiendra les paramètres de la commande
        resultat='' #str qui contiendra le resultat
        index=0     #int qui contiendra l'identifiant de la commande

        #extraction de la commande et des paramètre 
        for c in range(len(self.commandes[-1])) :
            if self.commandes[-1][c] =='(':
                commande = self.commandes[-1][:c]
                parametre = self.commandes[-1][c+1:-1]
        #vérification que la commande est valide
        c=False
        for commandes in range (len(self.operation)) :
            if self.operation[commandes]['appelle'] == commande:
                index=commandes
                c=True

        if c == False :
            self.envoyer_message('commande invalide')
            return False
        
        parametre = parametre.split(',')
        if parametre == ['']: #Dans le cas où il n'y a pas de virgule
            parametre = []

        if len(parametre) != self.operation[index]['nb_parametre']:
            print(self.operation[index]['nb_parametre'])
            self.envoyer_message('nombre de paramètre invalide')
            return False
        
        #vérification que les paramètres sont valide et les extraits
        for c in range(len(parametre)):
            if len(parametre[c])>0:
                parametre[c]=parametre[c][1:-1]
            else:
                self.envoyer_message('paramètre invalide')
                return False
            
        #comme les opérations traite que des noeuds en paramètre
        #alors ont vérifie à l'avance qu'il esxiste bien avant de les envoyés
        #Ensuite dans le futur cette vérification sera produit que par les 
        #opérations qui gère que des noeuds .C'est mieux si on souhaite diversifié les paramètres
        for param in parametre:
            if param not in self.master.Graphe.graphe.keys() :
                self.envoyer_message('paramètre invalide')
                return False
        try:
            resultat=self.operation[index]['commande'](self.master.Graphe.graphe,*parametre)
            #Les classes sont valide ,si il y a une erreur c'est car dans le cas d'un graphe orientés
            #Un noeud peut aller vers un autre mais pas dans toujours dans l'autre sens donc un noeud paut-être isolé
            #Pareil dans les graphes non orientés donc si on souhaite le chemin le plus court entre 2 noeuds qui ne sont pas 
            #relier c'est cette erreur qui vient.
        except KeyError :
            self.envoyer_message("Commande valide mais elle n'a pas de résultat")
            return False

        if commande == 'matrice':
            for i in resultat:
                self.envoyer_message(i)
        else:
            self.envoyer_message(resultat)


        


