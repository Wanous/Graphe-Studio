import tkinter as tk
from tkinter import messagebox,PhotoImage
from tkinter.filedialog import askopenfilename

from src.Interface.Canevas import ZoomCanevas
from src.Interface.Console import ConsoleCommande
from src.Graphe.Graphe import Graphe

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("DEMO Graphe Studio")
        self.configuration={'x':1000,'y':500}
        self.iconbitmap("src/Ressource/Icone.ico")
        self.geometry("1000x500")

        self.size = 500
        self.resizable(0, 0) 

        self.after(1000,self.gestion_affichage)
        self.after(1000,self.creer_menu)
        
        self.Graphe=Graphe(self)
        self.creer_widgets()

    def run(self):
        img = PhotoImage(file="src/Ressource/ImageDemarrage.png")
        label = tk.Label(self, image=img)
        label.place(x=-2,y=0)
        label.after(1000,label.destroy)

        self.mainloop()

    def creer_menu(self):
        menu_bar = tk.Menu(self,background='black')
        
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouveau", command=self.do_something)
        menu_file.add_command(label="Ouvrir...", command=self.open_file)
        menu_file.add_command(label="Sauvegarder...", command=self.save_image)
        menu_file.add_separator()
        menu_file.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_edit = tk.Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Retour", command=self.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(label="Copier", command=self.do_something)
        menu_edit.add_command(label="Couper", command=self.do_something)
        menu_edit.add_command(label="Coller", command=self.do_something)
        menu_bar.add_cascade(label="Edit", menu=menu_edit)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_about)
        menu_bar.add_cascade(label="Projet", menu=menu_help)

        self.config(menu=menu_bar,background='black')
        
    def creer_widgets(self):
        # création canevas
        self.canv = ZoomCanevas(self, width=self.size, height=self.size, bg="lightgrey",highlightbackground="black")                            
        self.console = ConsoleCommande(self)
        
    def gestion_affichage(self):    

        #position des widgets constituant le canevas
        self.canv.place(x=11,y=0)
        self.canv.bouton_nozoom.place(x=195,y=470)
        self.canv.coord_label.place(x=185,y=10)   

        #position des widgets constituant la console
        self.console.bouton_envoyer.place(x=935,y=471)
        self.console.saisie.pack(side=tk.BOTTOM,ipady=5, anchor=tk.SE,padx=63)
        self.console.zone_texte.place(x=525,y=0)
        
    def open_file(self):
        file = askopenfilename(title="choisissez un fichier à ouvrir",
                               filetypes=[("fichier texte TXT ", ".txt")])
        print(file)

    def do_something(self):
        print("Menu cliqué")

    def do_about(self):
        messagebox.showinfo("Projet", "Ce projet a été produit par Erwan Marais de la Terminal Romilly")
    
    def save_image(self):
        self.canv.postscript(file="votre_graphe.eps", colormode='color')


if __name__ == "__main__":
    app = Application()        
    
