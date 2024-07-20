from random import randint
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk,colorchooser
from math import sqrt
#Faire des copies du graphe sans problèmes (car il y a eu des problèmes avec .copy())
import copy 

class Graphe :
    def __init__(self,master):
        self.master=master
        self.type = None
        self.graphe = {}
        #dictiionnaire regroupant les méthodes de classe pour supprimer et ajouter des noeuds selon le type de graphe
        self.operation={'GrapheNO':{'ajouter_noeud':Graphe_non_oriente.ajouter_noeud,
                                    'supprimer_noeud':Graphe_non_oriente.supprimer_noeud},
                        'GrapheO':{'ajouter_noeud':Graphe_oriente.ajouter_noeud,
                                    'supprimer_noeud':Graphe_oriente.supprimer_noeud}}  
        
        self.retour=[] #Pile pour revenir à des versions antérieur du graphe

    def sauvegarde(self):
        '''méthode qui prépare le graphe pour une sauvegarde en lui remettant son type (retiré lors de l'initialisation
        pour simplifier les opérations sur le graphe)'''
        graphe=self.graphe.copy()
        graphe['type']=self.type
        return graphe
    
    def charger(self,graphe):
        '''méthode qui charge un graphe mis en paramètre (méthode utiliser dans l'importation de graphe')'''
        self.type=graphe['type']
        del graphe['type']
        self.graphe=graphe
        self.retour=[]
    
    def copie(self):
        '''méthode qui crée une copie du graphe'''
        self.retour.append(copy.deepcopy(self.graphe))
    
    def retour_en_arriere(self):
        '''méthode qui permet de revenir en arrière dans les versions du graphe'''
        if len(self.retour) > 0:
            self.graphe=copy.deepcopy(self.retour[-1])
            del self.retour[-1]
            self.master.mise_a_jour()
        
    def est_vide(self):
        '''méthode qui ranvoie vrai si le graphe est vide sinon faux'''
        if self.graphe == {}:
            return True
        return False
    
    def operation_execute(self,commande,**kwargs):
        self.operation[self.type][self.commande](self.graphe,**kwargs)
        
    
    def plus_loin_origine(self):
        '''
        méthode qui renvoie les coordonnées du noeud le plus loin de l'origine dans un tuple
        Retourne :
            loin(tuple): coordonnées du noeud le plus éloigner de l'origine'
        '''
        loin = (0,0)
        for noeud in self.graphe :
            coordonnees = self.graphe[noeud]['coordonnees']
            if sqrt((coordonnees[0])**2+(coordonnees[1])**2) > sqrt((loin[0])**2+(loin[1])**2) :
                loin = coordonnees
        return loin
        
    def sauvegarde_photo (self,chemin):
        '''Méthode qui reproduit le graphe sur une image crée avec la bibliothèque pillow dont les dimensions sont déterminées
           avec le point le plus éloigné de l'origine.La photo est sauvegardée en .png au chemin mis en paramètres.
           Certe Tkinter peut sauvegarder le graphe mais en .eps (trés dure à convertir avec python sans des bibliothèques qui demande une installation spécifique
           et non pas un simple 'pip install') et en plus de mauvaise qualité .Cette opération permet de faire une photo de bonne qualité pour l'utilisateur.
           
           paramètre :
               chemin(str) : chemin absolu du dossier ou sera sauvegardée la photo
        '''
        point=self.plus_loin_origine() #point le plus éloigné de l'origine
        rayon = 20                     #rayon des cercles qui représentent les noeuds sur la photo

        Longueur_fleche = 20
        Largeur_fleche = 10
        ditance_noeud=20
        #La distance entre l'origine et le point le plus éloigné de ce dernier est ce qui déterminera les dimensions de la photo
        maximum=int(sqrt((point[0])**2+(point[1])**2))*2 + rayon*2 #sans oublié la taille des noeuds à rajouter car sinon ça dépasse un peu
        taille_image = (maximum,maximum)
        background_color = "white"
        image = Image.new("RGB", taille_image, background_color)
        image.putalpha(0) #rendre le fond transparent
        draw = ImageDraw.Draw(image)

        #dessine les arêtes en tant que lignes entre les nœuds
        for noeud in self.graphe:
            for adjacent in self.graphe[noeud]['adjacent'] :
                #l'origine de la photo correspond au coin supérieur gauche donc il faut convertir les coordonnées des noeuds du graphe pour reproduire le graphe à l'identique
                depart = self.graphe[noeud]['coordonnees'][0]+taille_image[0]/2,-self.graphe[noeud]['coordonnees'][1]+taille_image[1]/2
                fin = self.graphe[adjacent]['coordonnees'][0]+taille_image[0]/2,-self.graphe[adjacent]['coordonnees'][1]+taille_image[1]/2
                if self.type == 'GrapheO':
                    draw.polygon([fin, (fin[0] - Largeur_fleche, fin[1] - Longueur_fleche / 2), (fin[0] - Largeur_fleche, fin[1] + Longueur_fleche / 2)], fill="black")
                    draw.line([depart, fin], fill="black", width=2)
                else:
                    draw.line([depart, fin], fill="black", width=2)
        #dessine les nœuds
        for noeud in self.graphe:
                x, y = self.graphe[noeud]['coordonnees'][0]+taille_image[0]/2,-self.graphe[noeud]['coordonnees'][1]+taille_image[1]/2
                draw.ellipse([x - rayon, y - rayon, x + rayon, y + rayon], fill=self.graphe[noeud]['couleur'])
                draw.text((x-rayon/4, y- rayon/4),noeud, fill=(0,0,0))
        #sauvegarde de la photo 
        image.save(chemin,"PNG")
        
    def nouveau_noeud(self):
        '''
        méthode qui crée une fenêtre pour ajouter un noeud dans le graphe
        avec pour valeurs celles misent par l'utilisateur
        '''

        top = tk.Toplevel(self.master)  #Fenêtre supérieur
        top.geometry('300x200')         #configuration de la fenêtre supérieur
        top.title('Création du noeud')
        top.resizable(False,False)
        
        self.couleur_noeud = '#FFFFFF'      #couleur par défaut pour un noeud
        co=tuple(self.master.canv.co_souris)#coordonnees où sera placé le noeud 
         
        def ajout_couleur():#fonction qui change la couleur du neoud
            '''fonction de la méthode qui demande une couleur à l'utilisateur
                et s'il en a une l'applique sur la canevas et sera la couleur 
                du noeud'''
            nouvelle_couleur = colorchooser.askcolor()[1] 
            if nouvelle_couleur != None :
                self.couleur_noeud = nouvelle_couleur
                color_canvas.configure(bg=self.couleur_noeud)
            
        def ajout_graphe():
            '''
            fonction de la méthode qui vérifie les informations misent par l'utilisateur
            et si elles sont valident alors le noeud est ajouté au graphe avec la méthode 
            de la classe correspondant à son type.
            '''
            nom = name_entry.get()                                          #récupération du nom du noeud
            selected_indices = listbox.curselection()                       #récupération des cases séléctionnées
            selected_items = [listbox.get(idx) for idx in selected_indices] #récupération des valeurs des cases séléctionnées 

            #vérification des informations saisies par l'utilisateur
            for noeud in self.graphe :
                if noeud == nom :
                    tk.messagebox.showerror("Erreur","Ce noeud existe déjà ,veuillez changer le nom du noeud")
                    top.destroy();return None
            if ' ' in nom or nom == '' :
                tk.messagebox.showerror("Erreur","Ce noeud à un nom invalide ,veuillez changer le nom du noeud")
                top.destroy();return None
            
            #Sauvegarde de la version du graphe pour un possible retour en arrière
            self.copie()
            
            #Création du noeud et mise à jour des informations avec le nouveau noeud
            self.operation[self.type]['ajouter_noeud'](self.graphe,nom,co,self.couleur_noeud,selected_items)
            self.master.mise_a_jour()
            top.destroy()
            
        #Interface du widget Toplevel
        #Canevas pour afficher la couleur sélectionnée
        color_canvas = tk.Canvas(top, width=50, height=50, bg=self.couleur_noeud)
        color_canvas.place(x=10,y=75)
        #bouton pour changer la couleur du noeud
        bouton_couleur = tk.Button(top, text="Couleur", command=ajout_couleur)
        bouton_couleur.place(x=10,y=150)
            
        
        name_label = tk.Label(top, text="Entrez un nom :")
        name_label.pack()
        
        name_entry = tk.Entry(top)
        name_entry.pack()
        
            
        option_label = tk.Label(top, text="Choisissez les adjacents de ce noeud:")
        option_label.pack()
        # Création de la Listbox avec barre de défilement
        scrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL)
        listbox = tk.Listbox(top, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set,height=5)

        for noeud in self.graphe:
            listbox.insert(tk.END,noeud)
        listbox.pack()
        
        save_button = tk.Button(top, text="Ajouter", command=ajout_graphe)
        save_button.place(x=90,y=165)
        
        boutton_annule = tk.Button(top, text="Annuler", command=top.destroy)
        boutton_annule.place(x=150,y=165)
        
        top.grab_set()
        top.wait_window(top) 
        
    def supprimer_noeud(self,noeud):
        '''
        méthode qui supprime un noeud du graphe 
        Paramètre :
            noeud(str) : une clé du graphe c'est-à-dire un noeud (celui qui sera supprimé)
        '''
        #Sauvegarde de la version du graphe pour un possible retour en arrière
        self.copie()
        #appelle de la méthode correspondant a son type
        self.operation[self.type]['supprimer_noeud'](self.graphe,noeud) 
        self.master.mise_a_jour()

    def editer_noeud(self,noeud):
        '''
        méthode qui crée une fenêtre pour modifier les différentes valeurs
        des différentes clés du dictionnaire du noeud mis en paramètre.
        Elle est similaire à la fenêtre crée par la méthode 'nouveau_noeud'
        mais agit différamment sur le graphe et rajoute la modification 
        des coordonnées.
        
        Paramètre :
            noeud(str) : une clé du graphe c'est-à-dire un noeud 
        '''

        top = tk.Toplevel(self.master)
        top.geometry('300x235')
        top.title('Edition du noeud')
        top.resizable(False,False)

        #reprise des informations du noeud pour les mettres dans les widget
        self.couleur_noeud = self.graphe[noeud]['couleur']
        co=self.graphe[noeud]['coordonnees']
         
        def ajout_couleur():
            '''fonction de la méthode qui demande une couleur à l'utilisateur
                et s'il en a une l'applique sur la canevas et sera la couleur 
                du noeud'''
            nouvelle_couleur = colorchooser.askcolor()[1] 
            if nouvelle_couleur != None :
                self.couleur_noeud = nouvelle_couleur
                color_canvas.configure(bg=self.couleur_noeud)
            
        def ajout_noeud():
            '''
            fonction de la méthode qui vérifie les informations misent par l'utilisateur
            et si elles sont valident alors le noeud est ajouté au graphe avec la méthode 
            de la classe correspondant à son type.
            '''
            nom = name_entry.get()
            indice_selectionne = listbox.curselection()
            items_selectionne = [listbox.get(idx) for idx in indice_selectionne]
            #vérification des informations saisies par l'utilisateur
            for noeuds in self.graphe :
                if noeuds == nom and noeuds != noeud:
                    tk.messagebox.showerror("Erreur","Ce noeud existe déjà ,veuillez changer le nom du noeud")
                    top.destroy();return None
            #ce n'est pas trés bon les espaces comme clé
            if ' ' in nom or nom == '' :
                tk.messagebox.showerror("Erreur","Ce noeud à un nom invalide ,veuillez changer le nom du noeud")
                top.destroy();return None
            try:
                x = int(entree_x.get())
                y = int(entree_y.get())
            except ValueError:
                tk.messagebox.showerror("Erreur", "Veuillez entrer des valeurs entières pour les coordonnées x et y.")
                top.destroy();return None
            
            #Sauvegarde de la version du graphe pour un possible retour en arrière
            self.copie()
            #Modification du noeud et mise à jour des informations avec le nouveau noeud
            self.operation[self.type]['supprimer_noeud'](self.graphe,noeud,True) #supprime le noeud
            self.operation[self.type]['ajouter_noeud'](self.graphe,nom,(x,y),self.couleur_noeud,items_selectionne,noeud )#met à jour le noeud
            
            self.master.mise_a_jour()
            top.destroy()
        
        # Interface du widget Toplevel   
        # Canevas pour afficher la couleur sélectionnée
        color_canvas = tk.Canvas(top, width=50, height=50, bg=self.couleur_noeud)
        color_canvas.place(x=10,y=75)

        bouton_couleur = tk.Button(top, text="Couleur", command=ajout_couleur)
        bouton_couleur.place(x=10,y=150)
            
        name_label = tk.Label(top, text="Entrez un nom :")
        name_label.pack()
        
        name_entry = tk.Entry(top)
        name_entry.pack()
        name_entry.insert(tk.END,noeud)

        
        
        option_label = tk.Label(top, text="Choisissez les adjacents de ce noeud:")
        option_label.pack()
        
        # Création de la Listbox avec barre de défilement
        scrollbar = ttk.Scrollbar(top, orient=tk.VERTICAL)
        listbox = tk.Listbox(top, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set,height=5)
        

        def listeformat(event):
            i=0
            listbox.delete(0, tk.END) 
            for noeuds in self.graphe:
                if noeuds != noeud or self.type == 'GrapheO':
                    if noeuds == noeud and noeud != name_entry.get():
                        listbox.insert(tk.END,name_entry.get())
                    else:
                        listbox.insert(tk.END,noeuds)
                if noeuds in self.graphe[noeud]['adjacent'] :
                    listbox.select_set(i) 
                i+=1
        listeformat(None)
        name_entry.bind('<KeyRelease>',listeformat)
        listbox.pack()
        
        #widget pour changer les coordonnées
        label_co = tk.Label(top, text="coordonnées :")
        label_co.pack()
        label_x = tk.Label(top, text="x :")
        label_x.place(x=80,y=175)
        entree_x = tk.Entry(top,width=5)
        entree_x.insert(tk.END,int(co[0]))
        entree_x.place(x=90,y=175)
        label_y = tk.Label(top, text="y :")
        label_y.place(x=160,y=175)
        entree_y = tk.Entry(top,width=5)
        entree_y.insert(tk.END,int(co[1]))
        entree_y.place(x=170,y=175)
        #bouton pour enragistrer les modifications apportées au noeud
        boutton_enregistre = tk.Button(top, text="Enregistrer", command=ajout_noeud)
        boutton_enregistre.place(x=80,y=200)
        #bouton pour annuler l'édition du noeud
        boutton_annule = tk.Button(top, text="Annuler", command=top.destroy)
        boutton_annule.place(x=150,y=200)
        
        #permet de ne pas intéragir avec la fenêtre principale tant que l'opération n'est pas terminé
        top.grab_set()
        top.wait_window(top) 

            
    def aleatoire(self):
        '''méthode qui crée un graphe aléatoire'''
        graphe={}
        nb_noeud=randint(10,20)
        if self.master!=None:limite=self.master.size/2
        else:limite=250
        for i in range(nb_noeud):
            graphe[f'{i}']={}
            graphe[f'{i}']['coordonnees']=(randint(-250,250), randint(-250,250))
            graphe[f'{i}']['adjacent']={str(0+randint(0,i)): None}
            
        self.graphe=graphe
        return True
    
class Graphe_non_oriente:  
    '''Classe qui permet l'ajout,la suppression et la modification des noeuds
        d'un graphe non orientés'''
    def ajouter_noeud(graphe,nom,co,couleur,adjacent,nom_depart=''):
        '''
        méthode qui ajoute un noeud dans un graphe non orienté

        paramètres :
            graphe(dict) : dictionnaire représentant le graphe
            nom(str) : nom de la clé ajouter dans le dictionnaire graphe
            co(tuple) : coordonnées x et y du noeud dans le canevas
            couleur(str) : code héxadécimal de la couleur
            adjacent(list) : liste des adjacents au noeud  
            nom_depart(str) : nom du noeud à la base 

        Retourne :
            graphe(dict) : le graphe avec les modifications appliquées

        '''
        #ajout du noeud dans le dictionnaire
        graphe[nom]={}
        graphe[nom]['coordonnees']=co
        graphe[nom]['couleur']=couleur
        graphe[nom]['adjacent']=adjacent
        #ajout du noeud dans la clé adjacent des adjacents au noeud
        for noeud in graphe:
            if noeud in adjacent and noeud != nom :
                graphe[noeud]['adjacent'].append(nom)
        return graphe
            
    
    def supprimer_noeud(graphe, noeud_supprime,modif = False,nom_depart=''):
        '''
        méthode qui supprime un noeud dans un graphe non orienté

        paramètres :
            graphe(dict) : dictionnaire représentant le graphe
            noeud_supprime(str) : nom de la clé à supprimer dans le dictionnaire graphe
            modif(bool) : signale si c'est une modification ou une suppression d'un noeud 
            nom_depart(str) : nom du noeud à la base 

        Retourne :
            graphe(dict) : le graphe avec les modifications appliquées
        '''
        #suppresion du noeud dans la clé adjacent des adjacents au noeud
        for noeud in graphe:
            if noeud_supprime in graphe[noeud]['adjacent'] :
                graphe[noeud]['adjacent'].remove(noeud_supprime)

        #suppression du noeud par la suppression de sa clé
        del graphe[noeud_supprime]
        return graphe

                    
class Graphe_oriente:
    '''Classe similaire à la classe 'Graphe_non_orientee' à la différence que cette classe 
       permet l'ajout,la suppression et la modification des noeuds d'un graphe orienté'''
    def ajouter_noeud(graphe,nom,co,couleur,adjacent,nom_depart=''):
        '''
        méthode qui ajoute un noeud dans un graphe orienté

        paramètres :
            graphe(dict) : dictionnaire représentant le graphe
            nom(str) : nom de la clé ajouter dans le dictionnaire graphe
            co(tuple) : coordonnées x et y du noeud dans le canevas
            couleur(str) : code héxadécimal de la couleur
            adjacent(list) : liste des adjacents au noeud    
            nom_depart(str) : noeud du noeud à la base 

        Retourne :
            graphe(dict) : le graphe avec les modifications appliquées

        '''
        #ajout du noeud dans le dictionnaire
        graphe[nom]={}
        graphe[nom]['coordonnees']=co
        graphe[nom]['couleur']=couleur
        graphe[nom]['adjacent']=adjacent
        for noeud in graphe:
            if nom_depart in graphe[noeud]['adjacent'] :
                index=graphe[noeud]['adjacent'].index(nom_depart)
                graphe[noeud]['adjacent'][index]=nom
        return graphe
            
    
    def supprimer_noeud(graphe, noeud_supprime,modif = False):
        '''
        méthode qui supprime un noeud dans un graphe orienté
        elle est aussi utilisée pour la modification d'un noeud
        si le paramètre 'modif' égale True

        paramètres :
            graphe(dict) : dictionnaire représentant le graphe
            noeud_supprime(str) : nom de la clé à supprimer dans le dictionnaire graphe
            modif(bool) : signale si c'est une modification ou une suppression d'un noeud

        Retourne :
            graphe(dict) : le graphe avec les modifications appliquées

        '''
        if modif == False :
            #suppresion du noeud dans la clé adjacent des adjacents au noeud
            for noeud in graphe:
                if noeud_supprime in graphe[noeud]['adjacent'] :
                    graphe[noeud]['adjacent'].remove(noeud_supprime)

        #suppression du noeud par la suppression de sa clé
        del graphe[noeud_supprime]
        return graphe
                        
if __name__ == "__main__":
    graphe=Graphe(None)
    graphe.aleatoire()
    print(graphe.graphe)


