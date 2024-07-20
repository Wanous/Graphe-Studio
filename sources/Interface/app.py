#importations des bibliothèques utilisées par le logiciel
import tkinter as tk

#des soucis sont arriver avec cette bibliothèque qui a peu d'importance
#donc si ça ne marche pas une fenêtre d'erreur apparaîtra à la place du site d'aide 
try :
    from tkhtmlview import HTMLLabel
except ModuleNotFoundError:
    pass
    
from tkinter import messagebox,PhotoImage,colorchooser,ttk
from tkinter.filedialog import askopenfilename,asksaveasfilename

#importations des autres parties du logiciel
from sources.Interface.Canevas import ZoomCanevas
from sources.Interface.Console import ConsoleCommande,operation
from sources.Interface.Tableur import Table
from sources.Graphe.Graphe import Graphe
from sources.Outils.ConfigurationINI import INI
from sources.Outils.FormatGRAF import GRAF

class Application(tk.Tk):
    """
    Classe qui s'occupe de crée et d'organiser l'ensemble des différentes parties du logiciel 
    .Elle permet de centraliser l'affichage de tout les widgets de la fenêtre principales ,son
    redimensionnement et autres intéractions avec l'utilisateurs comme les raccourcis clavier 
    (toujours sur la fenêtre principale).
    Cette classe permet de facilement manipuler le logiciel et de lui apporter des modifications 
    sans pour autant pertuber les autres parties du logiciel qui son programmées dans d'autres
    programmes présent dans le même chemin que ce fichier.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Graphe Studio")
        self.ini=INI(self,"sources/Ressource/preferences.ini") #initialisation de l'outils pour les préférences
        self.configuration=self.ini.charger()              #chargement des préférences de l'utilisateurs dans le fichier 'preferences.ini'
        
        self.menu = Menu(self)                             #Initialisation de la classe menu
        self.Graphe=Graphe(self)                           #Création du Graphe(au départ vide)
        self.infos_operation=operation
        self.type_graphe={'Graphe non orienté':"GrapheNO",
                          'Graphe orienté':"GrapheO"}
        
        self.fichier=None                     #Pour contenir un fichier importer
        self.creer_widgets()                  #initialisation des widgets (sans les afficher au départ)
        
        self.geometry("300x200")
        
        self.iconbitmap("sources/Ressource/Icone/Icone.ico")
        self.after(100,self.menu_demarrage)   #un peu de temps avant le démarrage 
        
    def run(self):
        '''
        Méthode appelé une seule fois par main.py qui permet le démarrage de l'application
        en commençant par l'affichage du logo puis le début de la boucle Tkinter
        '''
        img = PhotoImage(file="sources/Ressource/Photos/Menu_Demarrage.png")
        self.label = tk.Label(self, image=img)
        self.label.place(x=-2,y=0)

        self.mainloop()
        
    def commencement_graphe(self):
        '''
        Méthode appelé par le boutton 'bouton_nouveau'  du menu de démarrage est qui initialise un type de graphe
        souhaité par l'utilisateur si il a bien sélectionné un type
        '''
        selected_item = self.combo_box.get()   #case selectionnée par l'utilisateur
        graphe={}
        if selected_item !='':                 #Si il à bien sélectionné une case
            graphe['type']=self.type_graphe[selected_item]
            self.Graphe.charger(graphe)        #chargement du graphe avec le type selectionné 
            self.menu_graphe()                 #passage au menu de modification du graphe
        
    def ouverture_fichier(self):
        '''Méthode lié au boutton 'bouton_ouvrir' sur le menu de démarrage et qui permet d'ouvrir un graphe'''
        ouvert = self.menu.ouvrir_graphe()
        if ouvert == None:
            self.menu_graphe()
            
    def menu_demarrage(self):
        '''Méthode qui crée un menu qui sert que au démarrage du logiciel est qui permet de créer ou ouvrir un graphe'''
        self.resizable(False, False)

        self.combo_box = ttk.Combobox(self, values= [typ for typ in self.type_graphe], state="readonly")
        self.combo_box.bind("<<ComboboxSelected>>")
        self.combo_box.place(x=85,y=110)
        
        self.bouton_ouvrir = tk.Button(self, text="Ouvrir un graphe",command=self.ouverture_fichier)
        self.bouton_ouvrir.place(x=85,y=145)
        
        self.bouton_nouveau = tk.Button(self, text="Créer",command=self.commencement_graphe)
        self.bouton_nouveau.place(x=35,y=110)
        
    
    def menu_graphe(self):
        self.combo_box.destroy();self.bouton_nouveau.destroy();self.bouton_ouvrir.destroy();self.label.destroy()
        self.minsize(600, 300)                #taille minimum permit par le logiciel 
        self.resizable(True, True)
        self.geometry("700x500")
        
        #affichage et initialisation des widgets 
        self.gestion_affichage()
        self.creer_menu()

        
        self.bind("<Configure>", self.resize) #gestion du redimensionnement si la fenêtre est éléargie par l'utilisateur
        self.mise_a_jour()
        
    def creer_menu(self):        
        '''
        Méthode pour la création du menu qui possède plusieurs choix et sous-menus et
        l'initialisation de la classe Menu qui prendra en charge toute les intéractions avec le menu
        et les sous-menus pour rendre le code plus lisible et facile de modification.
        '''
        #Menu : ____________________________________________________
        #   Fichier |  Doc  |  Console  |  Preferences  |  Projet  |
        #___________________________________________________________
        self.options = {                              #Options (case cochable) du menu
            'canevas':{"distance": tk.IntVar(),
                       "origine": tk.IntVar(),
                       "axes": tk.IntVar(),
                       "infos": tk.IntVar()},
            
            'tableur':{"couleur_noeud": tk.IntVar(),
                       "ordre_alphabetique": tk.IntVar()}   
            }
           
        menu_bar = tk.Menu(self)
        
        menu_file = tk.Menu(menu_bar, tearoff=0)      #menu numéro 1 : gestion de fichiers (sauvegarder,ouvrir...)
        self.bind_all("<Control-z>",self.menu.retour) #ctrl + z -->revenir en arrière
        menu_file.add_command(label="Retour", accelerator="Ctrl+Z" ,command=self.menu.retour)
        menu_file.add_command(label="Nouveau",accelerator="Ctrl+N" ,command=self.menu.nouveau_graphe)
        self.bind_all("<Control-n>", self.menu.nouveau_graphe)    #ctrl + n --> créer un nouveau graphe
        menu_file.add_command(label="Ouvrir...",accelerator="Ctrl+O",command=self.menu.ouvrir_graphe)
        self.bind_all("<Control-o>", self.menu.ouvrir_graphe)     #ctrl + o --> ouvrir un graphe
        menu_file.add_command(label="Sauvegarder...",accelerator="Ctrl+S", command=self.menu.sauvegarde_graphe)
        self.bind_all("<Control-s>", self.menu.sauvegarde_graphe) #ctrl + s -->sauvegarder un graphe
        menu_file.add_command(label="Sauvegarder photo...", command=self.menu.sauvegarde_photo)
        menu_file.add_separator()
        menu_file.add_command(label="Quitter", command=self.menu.quitter)
        menu_bar.add_cascade(label="Fichier", menu=menu_file)
        
        menu_file = tk.Menu(menu_bar, tearoff=0)     #menu numéro 2 : documentation des types de graphes et les possibilités lié à ces derniers
        submenu = tk.Menu(menu_file, tearoff=0)
        submenu.add_command(label='graphe quelconque comportant des nœuds reliés entre eux par des sommets.',state="disabled", background='#cccccc',activebackground='yellow')
        menu_file.add_cascade(label="Graphe non orienté", menu=submenu)
        submenu = tk.Menu(menu_file, tearoff=0)
        submenu.add_command(label='graphe quelconque semblable au non orienté, si l’on excepte le fait \n que ses arêtes ont des flèches signifiant le sens du lien.',state="disabled", background='#cccccc',activebackground='yellow')
        menu_file.add_cascade(label="Graphe orienté", menu=submenu)
        menu_file.add_command(label="Plus de détail...", command=self.menu.ouvrir_html)
        menu_bar.add_cascade(label="Doc", menu=menu_file)
        
        menu_file = tk.Menu(menu_bar, tearoff=0)     #menu numéro 3 : menu de démarrage pour la console et les informations des commandes lié à celui-ci
        menu_file.add_command(label="Démarrer", command=self.menu.console_demarrage)

        submenu = tk.Menu(menu_file, tearoff=1)
        for operation in self.infos_operation :
            submenu.add_command(label=operation['description'],state="disabled", background='#cccccc', foreground='black',activebackground='yellow')
            submenu.add_separator()

        menu_file.add_cascade(label="Commandes", menu=submenu)
        menu_bar.add_cascade(label="Console", menu=menu_file)
        
        menu_file = tk.Menu(menu_bar, tearoff=1)     #menu numéro 4 : preferences de l'utilisateurs (aussi c'est un menu détachable)
        menu_file.add_command(label="Couleur Tableur", command=self.menu.choix_couleur_tableur)
        menu_file.add_command(label="Couleur Canevas", command=self.menu.choix_couleur_canevas)
        menu_file.add_command(label="Couleur Distance", command=self.menu.choix_couleur_distance)

        #ajout des options
        for widget in self.options.keys():
            menu_file.add_separator()
            menu_file.add_command(label="Option pour le "+widget,state="disabled")
            for option, var in self.options[widget].items():
                  menu_file.add_checkbutton(label=option, variable=var,command=self.menu.case_cocher)
                  if self.configuration[widget][option]=='True':
                          self.options[widget][option].set(1)
                      
        menu_file.add_separator()
        menu_file.add_command(label="Sauvegarder les préférences", command=self.menu.sauvegarde_preferences)
        menu_bar.add_cascade(label="Preferences", menu=menu_file)
        
        menu_help = tk.Menu(menu_bar, tearoff=0)     #menu numéro 5 : Lien pour obtenir plus d'information sur le projet 
        menu_help.add_command(label="About", command=self.menu.texte_projet)
        menu_bar.add_cascade(label="Projet", menu=menu_help)
  
        self.config(menu=menu_bar)
             
    def creer_widgets(self):
        '''
        Méthode qui initialise les autres parties du logiciel qui correspondent 
        aux 'widgets' de la fenêtre principale .      
        '''
        self.canv = ZoomCanevas(self, width=500, height=500, bg=self.configuration['canevas']['couleur'],highlightbackground="black")   # création du canevas                         
        self.table = Table(self)                                                                           # création du tableur  
        
    def gestion_affichage(self):    
        """
        Méthode qui gére le placement et l'affichage de tout les widgets de la fenêtre principales ,
        efficace pour produire des modifiacations de manière simple .
        """
        
        
        #position des widgets constituant le canevas                                                                              Fenêtre :
        #Le canevas fait 70% de l'écran en longueur et sa largeur est égale à la largeur de la fenêtre du logiciel                #----------------------
        self.canv.place(x=0, y=0)                                                                                                 #             |       |
        self.canv.bouton_nozoom.place(x=self.canv.dimension['x']/2-50,y=self.winfo_height()-50)                                   #   Canevas   | tab   |
        self.canv.coord_label.place(x=self.canv.dimension['x']/2-75,y=5)                                                          #             | leur  |
                                                                                                                                  #-----70%--------30%---
        #position du widgets constituant le Tableur
        #Le tableur lui fait 30% de l'écran en longueur et sa largeur est égale à la largeur de la fenêtre du logiciel
        #(il n'y que le widget Frame à afficher car il contient le widget tableur)
        self.table.frame.place(x=self.winfo_width()*0.7,y=0,height=self.winfo_height(),width=self.winfo_width()*0.3)

    def resize(self,event):
        '''
        Méthode déclenché par l'événement 'la fenêtre est en train d'être redimensionné' et permet de 
        recalculer la position des widgets sur l'écran en prenant en compte les nouvelles dimensions
        de la fenêtre tout en redimensionnant ces derniers pour qu'il garde le même ratio 
        '''

        self.canv.config(width=self.winfo_width()*0.7,height=self.winfo_height())               #Le canevas fait 70% de l'écran en longueur et sa largeur est égale à la largeur de la fenêtre du logiciel
        dimension_canva=self.canv.dimension
        self.canv.dimension={'x':int(self.canv.cget('width')),'y':int(self.canv.cget('height'))}#enregistrement des nouvelle dimension du canevas (utilisée pour les affichées dans le canevas)
        self.canv.decalage={'x':abs(self.canv.dimension['x']-dimension_canva['x']),             #enregistrement du décalage entre les nouvelles dimension du canevas et celle de base
                                'y':abs(self.canv.dimension['y']-dimension_canva['y'])}
        self.canv.mise_a_jour() #mise à jour du canevas avec ces nouvelles dimensions
        self.gestion_affichage()#mise à jour de la position du canevas sur la fenêre avec ces nouvelles coordonnées

    def mise_a_jour(self):
        '''
        Méthode qui permet de mettre à jour les données des objets
        qui constitue le logiciel .Efficace lors d'ouverture d'un fichier par exemple'
        '''
        self.canv.mise_a_jour() #mise à jour canevas
        self.table.mise_a_jour()#mise à jour tableur

class Menu:
    '''
    Classe qui contient des méthodes qui sont les actions des différents sous-menus
    Elle permet de bien séparer le widget menu de la classe application et ainsi rendre 
    le code mieux structuré et comprhensible.
    '''
    def __init__(self,master):
        
        self.master=master
    
    def console_demarrage(self,action=None):
        '''Cette méthode permet d'initialiser une fenêtre supérieur qui sert de console de commande'''
        self.master.console=ConsoleCommande(self.master) #crée un objet console 
        
    def case_cocher(self):

        options=self.master.options
        for widget in options.keys():
            for option, var in options[widget].items():
                if var.get():
                    self.master.configuration[widget][option] = 'True'
                else:
                    self.master.configuration[widget][option] = 'False'
        self.master.mise_a_jour()
        
    def choix_couleur_tableur(self):
        '''
        Cette méthode permet d'ouvrir une fenêtre qui demande une couleur à l'utilisateur
        La couleur est ensuite appliqué aux noeuds du graphe du logiciel et le changement 
        et enregister dans l'attribut changement pour une éventuelle sauvegarde
        '''
        couleur = colorchooser.askcolor()[1]                      #Fait apparaître la fenêtre qui demande une couleur
        self.master.configuration['tableur']['couleur'] = couleur #applique la couleur
        self.master.table.mise_a_jour()                           #met à jour le tableur avec cette nouvelle couleur
        
    def choix_couleur_canevas(self):
        '''Cette méthode est similaire à 'choix_couleur_noeud' mais ici c'est la couleur du canevas qui est modifiée '''
        couleur = colorchooser.askcolor()[1]
        self.master.canv.config(bg=couleur) #applique directement la couleur sans passer par une mise à jour (comparé au tableur)
        self.master.configuration['canevas']['couleur'] = couleur
        
    def  choix_couleur_distance(self):
        '''Cette méthode est similaire à 'choix_couleur_noeud' mais ici c'est la couleur du texte qui affiche les distances entre 2 noeuds qui est modifié '''
        couleur = colorchooser.askcolor()[1]
        self.master.configuration['canevas']['couleur_distance'] = couleur
        self.master.canv.mise_a_jour() #met à jour le canevas avec cette nouvelle couleur
        
    def sauvegarde_preferences(self):
        '''
        Cette méthode permet d'ouvrir une fenêtre qui demande à l'utilisateur
        si il souhaite enregistrer les changements qu'il a produit dans les préférences
        '''
        message = tk.messagebox.askyesno("Sauvegarder", "Êtes-vous sûre ?")
        if message :
            configuration=self.master.configuration
            for section in configuration:
                for element in configuration[section]:
                    self.master.ini.modifier(section,element,configuration[section][element])
        
    def ouvrir_graphe(self,event=None):
        '''
        Cette méthode permet d'ouvrir une fenêtre qui demande à l'utilisateur
        si il souhaite ouvrir un fichier .graf et si l'utilisateur n'a pas sauvegarder le graphe
        sur lequel il travail alors un message de prévention apparaît.
        '''
        message=None
        if self.master.Graphe.graphe!={} or self.master.fichier != None: #Si le graphe n'est pas vide ou qu'il y a un fichier en cours de modifications
            message = tk.messagebox.askyesno("Ouvrir un autre Graphe",   #un message de prévention est envoyé
            """
            Êtes-vous sûre ?
            Toute données non sauvegardé sera perdues.
            """)
        if message == True or message == None:
            try :
                file = askopenfilename(title="choisissez un fichier à ouvrir",
                                           filetypes=[("fichier Graphe Studio ", ".graf")])
                
                 
                nouveau_graphe = GRAF.charger(file)            #chargement du graphe grâce à la classe GRAF qui gére les fichiers .graf
                self.master.Graphe.charger(nouveau_graphe)
                self.master.fichier=file                     #Le chemin du fichier est garder en mémoire par l'attribut fichier de la classe Application
                self.master.title("Graphe Studio"+" "+file)  #affiche le nom du chemin dans le titre de la fenêtre principale                  
                self.master.mise_a_jour()                    #mise à jour du logiciel pour faire apparaître le nouveau graphe
            except FileNotFoundError:                        #erreur qui arrive si l'utilisateur ferme la fenêtre au lieu de faire un choix 
                return False
        self.master.mise_a_jour()
 
    def sauvegarde_graphe(self,event=None):
        '''Cette méthode sauvegarde un graphe dans un fichier .graf '''
        #Si il n'y a pas de fichier importer alors le programme demande 
        #un répertoire pour le sauvegarder en .graf (format de Graphe Studio)
        if self.master.fichier == None:
            #il peut y avoir une erreur si l'utilisateur décide de quitter 
            try:
                chemin = asksaveasfilename(filetypes = [('Graphe Studio', '.graf')])
                if chemin !='':
                    graphe = self.master.Graphe.sauvegarde()
                    GRAF.sauvegarder(chemin+'.graf',graphe) #sauvegarde du graphe grâce à la classe GRAF qui gére les fichiers .graf
                    self.master.fichier = chemin+'.graf'                       #même commentaire que pour la méthode 'ouvrir_graphe'
                    self.master.title("Graphe Studio"+" "+chemin+'.graf')
            except FileNotFoundError:
                return None
        else:
            #Sinon les données sont juste sauvegarder sans faire de demande
            GRAF.sauvegarder(self.master.fichier,self.master.Graphe.sauvegarde())
            #message de validation(car sinon ça donne l'impression que ça n'a rien fait)
            messagebox.showinfo("Sauvegarde", "Sauvegarder avec succés")
            
    def nouveau_graphe(self,event=None):
        '''Cette méthode permet de initialiser un nouveau graphe via une fenêtre supérieur à la fenêtre principale'''
        #Si le graphe n'est pas vide cela veut dire qu'il y a 
        #des données et que donc elle risque d'être perdues...
        message=None
        if self.master.Graphe.graphe!={} or self.master.fichier != None:
            message = tk.messagebox.askyesno("Nouveau Graphe",
            """
            Êtes-vous sûre ?
            Toute données non sauvegardé sera perdues.
            """)
        #None--> Pas besoin de fenêtre de prévention car il n'y a pas de fichier ni d'éléments
        #True--> Il y a eu une fenêtre de prévention et l'utilisateur à répondu oui
        if message == True or message == None: 
                top = tk.Toplevel(width=500,height=500) #création de la fenêtre supérieur
                top.resizable (False,False)
                top.geometry ("200x100")
                tk.Label(top, text='Selectionnez un type de graphe :').pack()
                box_value = tk.StringVar()
                combo = ttk.Combobox(top, values= [typ for typ in self.master.type_graphe],textvariable=box_value, state="readonly")
                combo.pack()
                combo.bind('<<ComboboxSelected>>', lambda _: top.destroy())
                top.grab_set()
                top.wait_window(top)  
                if box_value.get() != '':
                    graphe={}
                    graphe['type']=self.master.type_graphe[box_value.get()]
                    self.master.Graphe.charger(graphe)        #chargement du graphe avec le type selectionné 
                    self.master.Graphe.retour=[]
                    self.master.fichier = None #Au cas où un fichier a été importé
                    self.master.title("Graphe Studio")
                    self.master.mise_a_jour()
                    
    def sauvegarde_photo(self):
        '''
        Cette méthode à pour rôle de sauvegarder une image du graphe en .png  produite grâce à la bibliothèque Pillow
        et la méthode 'sauvegarde_photo' de la classe graphe .
        Le chemin vers le dossier ou l'utilisateur souhaite sauvegarder la photo est demander à ce dernier 
        '''
        try:
                chemin = asksaveasfilename(filetypes = [('Image', '.png')])
                if chemin != '':                                                                                                  
                    self.master.Graphe.sauvegarde_photo(chemin+".png") #capture d'écran 

        except FileNotFoundError:               #erreur qui arrive si l'utilisateur ferme la fenêtre au lieu de faire un choix 
                return None
        
    def retour(self,btn=None):
        self.master.Graphe.retour_en_arriere()
            
    def do_something(self):
        print("Menu cliqué")

    def texte_projet(self):
        '''Cette méthode à pour rôle d'afficher une fenêtre d'information qui mène vers des informations sur le logiciel/projet '''
        messagebox.showinfo("Projet", "Ce projet a été produit pour le trophée NSI de 2024 ")

    def ouvrir_html(self):
        navigateur = tk.Toplevel(self.master) #fenêtre supérieur à la fenêtre principale 
        filepath = "sources/Ressource/Site/index.html"  # Chemin vers le fichier HTML à charger
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()
        try :
            html_label = HTMLLabel(navigateur, html=html_content)
            html_label.pack(fill="both", expand=True)
            html_label.set_html(html_content)
        except NameError :
            messagebox.showinfo("Erreur", "La bibliothèque n'a pas été bien installé .Pour plus d'infos sur les Graphes veuillez vous renseigner autres part  ")
            
    
    def quitter(self):
        '''
        Cette méthode à pour rôle de quitter l'application après avoir demandé à l'utilisateur
        si il souaihte vraiment quitter celle-ci via une fenêtre qui demande un choix entre oui et non 
        '''
        message = tk.messagebox.askyesno("Quitter", "Êtes-vous sûre de vouloir quitter?")
        if message:
            self.master.destroy() #Fait disparaître la fenêtre
            self.master.quit()    #Stop l'application
            
    
    
