import tkinter as tk
import tkinter.font as tkFont
from math import sqrt,cos,sin,atan2,pi

class ZoomCanevas(tk.Canvas):
    """
    Classe qui s'occupe de crée et d'organiser un canevas dans lequelle 
    il est possible de zoomer et dessiner des graphes à l'aide de ses méthodes
    tout en ayant son propre menu et widget .
    """
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.master=master
        self.taille={'sommet':20,'ligne':2,'texte':10,'boucle':50} #Configuration des dimension des formes et du texte sur le canevas
        self.label_info=tk.Label(self.master)          #label qui affichera certaines infos du canevas
        self.scale_factor = 1.0          #variable qui contient le facteur de zoom du canevas
        
        self.dimension={'x':500,'y':500} #pour stocker la taille du canevas car elle est appelé souvent donc c'est plus lisible
        self.decalage={'x':500,'y':500}  #stock le décalage entre la taille de base et la taille aprés un redimensionnement
        
        #attributs destinés au canevas ET au graphe
        self.co_souris=[0,0]             #coordonnees de la souris sur le canevas
        self.noeud_selection=None        #garde en mémoire un noeud sélectionner par clique gauche
        self.bord = None                 #garde en mémoire un noeud sélectionner par clique droit 

        self.configuration=self.master.configuration['canevas'] #Informations qui seront affichés ou non selon les choix de preferences de l'utilisateur
        self.menu_graphe={'GrapheNO':['Modifier','Supprimer'],                          #Menu du caneva pour intéragir avec le graphe de manière direct
                          'GrapheO':['Modifier','Supprimer'],
                          'ArbreB':['Modifier','Supprimer']}
        #création des outils pour le canevas 
        self.widgets_canvas()
        self.evenements_souris()
        self.menu_canevas()
        self.draw_map()
        self.reperes()

    def widgets_canvas(self):
        '''méthode qui initialise et gére la position des différents widgets qui compléte le canevas'''
        self.bouton_nozoom = tk.Button(self, text="Reinitialiser le zoom",command=self.reset_zoom) # boutons pour réinitialiser le zoom en x1
        
        self.coord_label = tk.Label(self.master, text=f"Coordonnées : (0,0)")                      # label qui contient les Coordonnées de la souris sur le canevas
        #widget d'information sur le graphe 
        self.axe_X = self.create_line(5,10,self.dimension['x']-10,10)                              #axe des abscisses
        self.axe_Y = self.create_line(10,5,10,self.dimension['y']-10)                              #axe des ordonnées
        #Formation de la croix pour l'origine
        self.origine_X = self.create_line(self.dimension['x']/2,self.dimension['y']/2+10,self.dimension['x']/2,self.dimension['y']/2-10)   #1er trait pour l'origine                          
        self.origine_Y = self.create_line(self.dimension['x']/2+10,self.dimension['y']/2,self.dimension['x']/2-10,self.dimension['y']/2)   #2eme trait pour l'origine  
        
        self.info_axe = self.create_text((70,25),text=f'taille : ({self.dimension["x"]*self.scale_factor},{self.dimension["y"]*self.scale_factor})') #texte qui affiche les dimensions des 2 axes
        self.info_zoom = self.create_text((50,25),text=f'zoom : x{self.scale_factor}')#texte qui affiche le facteur de zoom 
        
    def evenements_souris(self):
        '''méthode qui initialise les intéractions entre la souris et le canevas'''
        # Événements de la souris avec le canevas
        self.bind("<Motion>", self.maj_coordinates)     #Coordonnées de la souris rafraîchie sur le canevas quand elle bouge
        self.bind("<MouseWheel>", self.maj_coordinates) #Coordonnées de la souris rafraîchie sur le canevas quand la molette est bouger
        self.bind("<Motion>", self.info,add="+")        #vérifie si la souris est sur un noeud quand la souris bouge
        self.bind("<MouseWheel>", self.info,add="+")    #vérifie si la souris est sur un noeud quand la molette est bouger
        self.bind("<MouseWheel>", self.on_mousewheel,add="+") #zoom produit si la molette est bouger
        self.bind("<Motion>", self.bouge_noeud,add="+") #permet de déplacer un noeud

        
        self.bind("<Button-3>", self.afficher_menu)     # Clique droit pour activer le menu
        self.bind("<Button-1>", self.select_noeud)      #permet de sélectionner un noeud
        
    def select_noeud(self,event):
        '''
        méthode déclenché par l'événement "clique gauche" mis en paramètre et qui sélectionne ou désélectionne un noeud
        pour commencer ou stopper sont déplacement
        ''' 
        bord = self.gettags("current")     
        if len(bord) >= 2 and bord != ():  
            if self.noeud_selection == None :
                self.noeud_selection = bord[0]
                self.master.Graphe.copie()
            else:
                self.noeud_selection = None
                          
    def bouge_noeud(self,event):      
        '''
        méthode déclenché par l'événement  "La souris se déplace" mis en paramètre et qui déplace un noueud sur le canevas 
        si l'utilisateur en a sélectionner un .
        ''' 
        if self.noeud_selection != None :
            self.master.Graphe.graphe[self.noeud_selection]['coordonnees']=(self.co_souris[0],self.co_souris[1])
            self.master.mise_a_jour()
            
    def menu_canevas(self):
        '''
        méthode qui initialise et gére le menu qui permet à l'utilisateur 
        d'intéragire avec le graphe
        '''
        #Menu
        self.menu_noeud = tk.Menu(self.master, tearoff=0) #menu pour les noeuds
        self.menu_canevas= tk.Menu(self.master, tearoff=0)#menu le canevas
        
        #Sous menus
        self.menu_noeud.add_command(label="Editer",command=lambda:self.master.Graphe.editer_noeud(self.bord[0]))  
        self.menu_noeud.add_command(label="Supprimer",command=lambda:self.master.Graphe.supprimer_noeud(self.bord[0]))  
        self.menu_canevas.add_command(label="Ajouter un noeud",command=self.master.Graphe.nouveau_noeud)
        
    def afficher_menu(self,event):
        '''
        méthode déclenché par l'événement "clique droit" mis en paramètre et qui affiche un menu diférent selon l'endroit 
        où a été effectué le clique .
        ''' 

        bord = self.gettags("current")
        if self.noeud_selection == None : #Si un noeud n'est pas en cours de déplacement 
            if len(bord) >= 2 and bord != (): 
                #si le clique droit est fait sur un noeud alors le menu pour les noeud apparaît
                self.menu_noeud.tk_popup(event.x_root, event.y_root, 0)
                self.bord=bord #garde le noeud en mémoire au cas où une intéraction se prépare
            else :
                #sinon cela veut dire que le clique droit est fait hord d'un noeud alors le menu pour le canevas apparaît
                self.menu_canevas.tk_popup(event.x_root, event.y_root, 0)
                

    def mise_a_jour(self): 
        '''méthode qui rafraîchie les informarions contenu dans le canevas''' 
        self.draw_map() #rafraîchissement du graphe
        self.reperes()  #rafraîchissement des information(repère,zoom,origine...)

    def maj_coordinates(self, event): 
        '''méthode déclenché par l'événement "La souris se déplace" ou "la molette bouge" mis en paramètre et qui met à jour les coordonnées affichées''' 
        # Ajustement des coordonnées pour quelle soit par rapport au centre du canevas et non le coin supérieur gauche 
        x, y = event.x -self.dimension['x']/2, self.dimension['y']/2 - event.y  
        self.co_souris=[x//self.scale_factor,y//self.scale_factor]
        self.coord_label.config(text=f"Coordonnées : ({self.co_souris[0]}, {self.co_souris[1]})") #affichage dees coordonnées via un widget label
        
    
    def reperes(self,event=None):
        '''
        méthode déclenché par l'événement "la molette bouge" mis en paramètre et qui met à jour les informations du canevas 
        et calcul les nouvelle coordonnées des axes/informations du canevas en prenant en compte le nouveau facteur de zoom
        ''' 
        self.delete(self.axe_X,self.axe_Y,self.info_axe,self.info_zoom,self.origine_X,self.origine_Y) #supprime ceux qui sont plus d'actualité car le zoom à été modifier

        #mise à jour du repère rapportant le repère au nouveau niveau de zoom
        if self.configuration['axes']=='True':
            self.axe_X = self.create_line(5,10,self.dimension['x']-10,10)
            self.axe_Y = self.create_line(10,5,10,self.dimension['y']-10)
        
        #origine
        if self.configuration['origine']=='True':
            self.origine_X = self.create_line(self.dimension['x']/2,self.dimension['y']/2+5,self.dimension['x']/2,self.dimension['y']/2-5)                            
            self.origine_Y = self.create_line(self.dimension['x']/2+5,self.dimension['y']/2,self.dimension['x']/2-5,self.dimension['y']/2)  
                
        #le décalage permet de garder le même positionnement des informations sur le canevas  
        if self.configuration['infos']=='True':
            self.info_axe = self.create_text((80,25+self.decalage['y']),text=f'dimension : ({round(self.dimension["x"]/self.scale_factor,2)},{round(self.dimension["y"]/self.scale_factor,2)})')
            self.info_zoom = self.create_text((50,50+self.decalage['y']),text=f'zoom : x{round(self.scale_factor,2)}')           

    def info(self,event):
        '''
        méthode déclenché par l'événement "La souris se déplace" mis en paramètre et qui affiche les 
        informations d'un noeud si l'utilisateur passe la souris dessus
        ''' 
        bord = self.gettags("current")     #obtention du tag de l'objet présent à la position de la souris
        if len(bord) >= 2 and bord != ():  #si il a bien un objet avec des informations contenu dans le tag
            self.label_info['text']="sommet :",bord[0],"adjacent(s) :",bord[1]
            self.label_info.place(x=event.x-40-len(self.label_info['text']),y=event.y-30) #affichage du widget au-dessus de la souris
        else:
            self.label_info.place_forget()#sinon il affiche rien voir retire l'affichage du widget si il l'a été
        

    def on_mousewheel(self, event):
        '''
        méthode déclenché par l'événement "la molette bouge" mis en paramètre et qui permet de déterminer
        l'orientation de la rotation de la molette
        ''' 
        if event.delta >0:#La molette est tournée vers le haut
            self.zoom(1.1,self.dimension['x']/2, self.dimension['y']/2) #application du zoom avant par la méthode 'zoom'
        elif event.delta <0:#La molette est tournée vers le bas
            self.zoom(0.9,self.dimension['x']/2, self.dimension['y']/2) #application du zoom arrière par la méthode 'zoom'
        self.reperes()#mise à jour du repere avec le nouveau niveau de zoom

    def zoom(self, facteur, x, y):
        '''
        méthode qui prend en paramètre un facteur (0.9 ou 1.1) est le multiplie au niveau de zoom actuelle du canevas
        Le zoom est centré sur les coordonnées x et y mis en paramètres.
        
        Paramètres :
            facteur(float) : facteur multipliant le niveau de zoom du canevas 
            x(int) : coordonnées en abscisse du centrage du zoom
            y(int) : coordonnées en ordonnée du centrage du zoom
        ''' 
        self.scale_factor *= facteur
        self.scale("all", x, y, facteur, facteur)

    def reset_zoom(self): 
        '''méthode qui remet le facteur de zoom a 1 (facteur originel à la création du canevas) et l'applique'''  
        self.reset()           # Supprime les éléments dessinés sur le canevas
        self.scale_factor = 1.0# remet à 1 le facteur de zoom 
        self.scale("all", self.dimension['x']/2, self.dimension['y']/2, self.scale_factor, self.scale_factor) # applique le zoom
        self.mise_a_jour()     # rafrîchie le canevas avec le facteur de zoom remis en x1
    
    def reset(self):
        '''méthode qui Supprime tout les éléments dessinés sur le canevas''' 
        self.delete('all')
    
    def recadrer(self):
        '''méthode qui permet de revenir au centre du canevas 
        (non utilisée mais intéressant pour de futur ajout sur le déplacement dans la canevas)''' 
        origX = self.xview()[0]
        origY = self.yview()[0]
        self.xview_moveto(origX)
        self.yview_moveto(origY)
    def distance_noeud(self,x,x1,y,y1):
        '''
        méthode qui prend en paramètres les coordonnées de 2 noeuds du graphes (x,y) (x1,y1)
        et renvoie la distance entre les 2 en utilisant la formule : v/(x2-x1)**2 + (y2-y1)**2 (théorème de pythagore)
        tout les paramètres sont des entiers relatifs (int).
        ''' 
        return sqrt((x-x1)**2+(y-y1)**2)
        
    def ajout_element(self, Element, x, y, width=1, height=1, **kwargs):
        '''
        méthode qui prend en paramètres des coordonnées et les dimensions (selon l'élément mis en paramètre) 
        d'une forme ou texte à dessiner sur le canevas en passant par la 
        convertion de ses coordonnées pour le canevas afin d'appliquer le niveau de zoom et le recadrage pour que celui-ci soit placer par rapport au 
        centre du canevas et non le coin supérieur gauche de celui-ci (car pour le canevas ce coin c'est l'origine (0,0) donc il appliquée un décalage
        pour que l'origine soit plutôt le centre du canevas).                                                             
        tout ceci est possible grâce à la formule : coordonnée*zoom+Taille canevas/2 
        que l'on peut inverser par la formule : (coordonnée - Taille canevas/2 ) // zoom
        
        Paramètres :
            Element(str) : nom de l'élément (rectangle,oval...) 
            x(int) : abscisse de l'élément 
            y(int) : ordonnée de l'élément 
            width(int) : longueur de l'élément
            height(int) : largeur de l'élément
            **kwargs(tout type) : informations suplémentaires pour une forme comme par exemple une couleur
            
        Retourne :
            element(object) : forme passé sous Tkinter qui sera ajouter au canevas par la méthode 'draw_map'
        ''' 
        x1 = x * self.scale_factor + self.dimension['x']/2
        y1 = y * self.scale_factor + self.dimension['y']/2
        x2 = (x + width) * self.scale_factor + self.dimension['x']/2
        y2 = (y + height) * self.scale_factor + self.dimension['y']/2

        # Ajout de l'élément dans le canevas
        if Element == "rectangle": 
            element = self.create_rectangle(x1, y1, x2, y2, **kwargs)
        elif Element == "cercle_arc":
            element = self.create_oval(x1,y1,x2,y2,**kwargs)
        elif Element == "ligne":
            element = self.create_line(x1,y1,x2,y2, **kwargs)
        elif Element == "fleche":
            element = self.create_line(x1, y1, x2, y2,**kwargs)
        elif Element == "texte":
            element = self.create_text((x1, y1),  **kwargs)
        return element
    
    def draw_map(self):
        '''
        méthode qui permet de dessiner le graphe graçe aux information du graphe extraites depuis l'application 
        qui possède le graphe .Elle place et respecte les propriétés de chaque éléments du graphe comme la couleur d'un noeud et
        met un tag à chaque noeud contenant ses informations pour qu'il puisse être affiché si l'utilisateur passe la souris dessus
        '''

        graphe=self.master.Graphe.graphe #récupération du graphe dans l'application
        self.delete('all')               #assure que le canevas soit vidé de tout dessins 
        liste_doublon=[]                 #liste pour éviter les doublons dans les flèche qui vont dans les 2 sens
  
        #affichage des sommets/arcs... et la distance entre les noeuds
        for noeud in graphe:              
            for adjacent in range(len(graphe[noeud]['adjacent'])):           #pour chaque adjacent de chaque noeud
                adjacent_value=graphe[noeud]['adjacent'][adjacent]
                x1 , y1 = graphe[noeud]['coordonnees'];y1=-y1                #extraction des coordonnées du noeud
                x2 , y2 = graphe[adjacent_value]['coordonnees']              #extraction des coordonnées de l'adjacent à ce noeud
                if self.master.Graphe.type == 'GrapheNO': #Ligne pour les graphes non orientés
                    self.ajout_element('ligne',x1, y1,x2-x1,-y2-y1,fill='black') #dessine les ligne qui relie les noeud (sommet,arête...)
                else:                                     #Flèches pour les graphes orientés
                    rads=atan2(-y2-y1,x2-x1)%(2*pi)                            #décalage de la fléche à l'aide de la trigonométrie
                    if noeud in graphe[adjacent_value]['adjacent'] and noeud != adjacent_value:           #flèche dans les deux sens si les 2 chacun va vers l'autre 
                        liste_doublon.append((noeud,adjacent_value))
                        if (adjacent_value,noeud) not in liste_doublon:
                            self.ajout_element('fleche',x1+int(cos(rads)*10), y1+int(sin(rads)*10),x2-x1+(int(cos(rads))*self.taille['sommet']/2)-int(cos(rads)*20),-y2-y1-(int(sin(rads))*self.taille['sommet']/2)-int(sin(rads)*20),fill='black',arrow=tk.BOTH)
                    elif adjacent_value != noeud :
                         self.ajout_element('fleche',x1+int(cos(rads)*10), y1+int(sin(rads)*10),x2-x1+(int(cos(rads))*self.taille['sommet']/2)-int(cos(rads)*20),-y2-y1-(int(sin(rads))*self.taille['sommet']/2)-int(sin(rads)*20),fill='black',arrow=tk.LAST)
                    else :                                 #Si un noeud est un adjacent à lui même (une boucle)
                        rads=atan2(y1,x1)%(2*pi)                                              
                        self.ajout_element('fleche',x1-self.taille['sommet'],y1,self.taille['sommet']/2,0,fill='black',arrow=tk.LAST)
                        self.ajout_element('cercle_arc',x1-self.taille['sommet']*1.5,y1-self.taille['sommet']*1.5,self.taille['sommet']*1.5,self.taille['sommet']*1.5,outline="black")
                    
                if self.configuration['distance'] == 'True':                 #affiche la distance calculer grâce aux données extraites auparavant (selon les préférences de l'utilisateur)
                    self.ajout_element('texte',(x1+x2)//2, (y1-y2)//2,
                                       text=str(int(self.distance_noeud(x1, x2, (-y1), y2))),
                                       fill=self.configuration['couleur_distance'],
                                       font=tkFont.Font(family="Arial", size=self.taille['texte'])) 
                    
        #affichage noeuds et nom de ces derniers
        for noeud in graphe:
            # extraction des coordonnées et couleur du noeud pour le dessiner sur le canevas avec son nom
            x , y =  graphe[noeud]['coordonnees'];y=-y
            color = graphe[noeud]['couleur'] 
            self.ajout_element('rectangle',x-self.taille['sommet']/2, y-self.taille['sommet']/2,self.taille['sommet'],self.taille['sommet'], fill=color,tags=[noeud,graphe[noeud]['adjacent']])
            self.ajout_element('texte',x+self.taille['sommet']*1.5, y+self.taille['sommet']*1.5,1,1, text=noeud,font=tkFont.Font(family="Arial", size=self.taille['texte']))
            

