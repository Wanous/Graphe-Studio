import tkinter as tk
import tkinter.font as tkFont

class ZoomCanevas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
        self.master=master
        self.taille={'sommet':10,'ligne':2,'texte':10}
        self.label_info=tk.Label(self.master)
        self.scale_factor = 1.0
        self.widgets_canvas()
        self.draw_map()
        self.reperes()

    def widgets_canvas(self):
        # boutons
        self.bouton_nozoom = tk.Button(self, text="Reinitialiser le zoom",command=self.reset_zoom)
        # Coordonnées
        self.coord_label = tk.Label(self.master, text=f"Coordonnées : (0,0)")
        #widget d'information sur le graphe 
        self.axe_X = self.create_line(5,10,self.master.size-10,10)
        self.axe_Y = self.create_line(10,5,10,self.master.size-10)
        self.info_axe = self.create_text((70,25),text=f'taille : ({-self.master.size},{self.master.size})')
        self.info_zoom = self.create_text((50,25),text=f'zoom : x{self.scale_factor}')          
        # Événements de la souris (à mettre dans le canva def interface)
        self.bind("<Motion>", self.maj_coordinates)
        self.bind("<MouseWheel>", self.maj_coordinates)
        self.bind("<Motion>", self.info,add="+")
        self.bind("<MouseWheel>", self.on_mousewheel,add="+")
    
    def mise_a_jour(self):
        #méthode pour mettre à jour les informations du caneva 
        self.draw_map()
        self.reperes()

    def maj_coordinates(self, event): #pour rafraichir pense a multiplier ducoup
        # Mettre à jour les coordonnées affichées
        x, y = event.x - self.master.size/2, self.master.size/2 - event.y  # Ajuster les coordonnées au repère
        self.coord_label.config(text=f"Coordonnées : ({x//self.scale_factor}, {y//self.scale_factor})")
    
    def reperes(self,event=None):
        #mise à jour du repère rapportant le repère au nouveau niveau de zoom
        self.delete(self.axe_X,self.axe_Y,self.info_axe,self.info_zoom)
        self.axe_X = self.create_line(5,10,self.master.size-10,10)
        self.axe_Y = self.create_line(10,5,10,self.master.size-10)
        self.info_axe = self.create_text((70,25),text=f'taille : ({-self.master.size/2//self.scale_factor},{self.master.size/2//self.scale_factor})')
        self.info_zoom = self.create_text((50,50),text=f'zoom : x{round(self.scale_factor,2)}')     

    def info(self,event):
        bord = self.gettags("current")
        if len(bord) >= 2 and bord != ():
            self.label_info['text']="sommet :",bord[0],"adjacent :",bord[1]
            self.label_info.place(x=event.x-40-len(self.label_info['text']),y=event.y-30)
        else:
            self.label_info.place_forget()

        # autre façon pratique avec le zoom
        #self.find_closest(*clic)
        #if len(self.gettags(bord)) >= 2:
        #    print("sommet :",self.gettags(bord)[0],"adjacent :",self.gettags(bord)[1])

    def on_mousewheel(self, event):
        if event.delta >0:
            self.zoom(1.1, 250, 250)
        elif event.delta <0:
            self.zoom(0.9, 250, 250)
        self.reperes()

    def zoom(self, factor, x, y):
        self.scale_factor *= factor
        self.scale("all", x, y, factor, factor)

    def reset_zoom(self):
        # Remettre à zéro le facteur d'échelle
        self.reset()
        self.scale_factor = 1.0
        self.scale("all", 250, 250, self.scale_factor, self.scale_factor)
        self.draw_map()
        self.reperes()
    
    def reset(self):
        self.delete('all')
    
    def recadrer(self):
        origX = self.xview()[0]
        origY = self.yview()[0]
        self.xview_moveto(origX)
        self.yview_moveto(origY)

    def add_element(self, element_type, x, y, width, height, **kwargs):
        # Convertion des coordonnées pour le canva afin d'appliquer le niveau de zoom et le recadrage
        #formule : coordonnée*zoom+decalage 
        #pour annuler la fonction : (coordonnée - Taille canva/2) // zoom

        x1 = x * self.scale_factor + self.master.size/2
        y1 = y * self.scale_factor + self.master.size/2
        x2 = (x + width) * self.scale_factor + self.master.size/2
        y2 = (y + height) * self.scale_factor + self.master.size/2

        # Add element to the canvas
        if element_type == "rectangle":
            element = self.create_rectangle(x1, y1, x2, y2, **kwargs)
        elif element_type == "oval":
            element = self.create_oval(x1, y1, x2, y2, **kwargs)
        elif element_type == "ligne":
            element = self.create_line(x1,y1,x2,y2, **kwargs)
        elif element_type == "texte":
            element = self.create_text((x1, y1),  **kwargs)
        return element
    
    def draw_map(self , hospitals = []):
        c = self
        graphe=self.master.Graphe.graphe
        self.delete('all')
        for noeud in graphe:
            for adjacent in graphe[noeud]['next']:
                x1 , y1 = graphe[noeud]['coords']
                x2 , y2 = graphe[adjacent]['coords']
                c.add_element('ligne',x1+2, y1+2,x2-x1,y2-y1,fill='black')
                c.add_element('texte',(x1+x2)//2, (y1+y2)//2,20,20, text=graphe[noeud]['next'][adjacent],font=tkFont.Font(family="Arial", size=self.taille['texte']))

        for noeud in graphe:
            x , y =  graphe[noeud]['coords']
            color = 'red' if noeud in hospitals else 'black' 
            c.add_element('rectangle',x, y,self.taille['sommet'],self.taille['sommet'], fill=color,tags=[noeud,list(graphe[noeud]['next'].keys())])
            c.add_element('texte',x+self.taille['sommet']+12, y+self.taille['sommet']+12,1,1, text=noeud,font=tkFont.Font(family="Arial", size=self.taille['texte']))
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomCanvas(root)
    root.mainloop()
