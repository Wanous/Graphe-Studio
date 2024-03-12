import tkinter as tk
from tkinter import scrolledtext

class ConsoleCommande:
    def __init__(self, master):

        self.master = master
        self.graphe = master.Graphe
        self.commandes=[]
        self.messages=[]
        self.up=0

        self.widgets_console()
        
    def widgets_console(self):
        self.zone_texte = scrolledtext.ScrolledText(self.master,font=("Arial 11"),wrap=tk.WORD, width=57, height=28, background="black", foreground="white")
        self.zone_texte.config(state=tk.DISABLED)

        self.saisie = tk.Entry(self.master, width=68)
        self.saisie.bind('<Return>',self.envoyer_commande)#Appuyez sur entrée envoie le message
        self.saisie.bind('<Key>',self.raccourci_clavier)

        self.bouton_envoyer = tk.Button(self.master, text="Envoyer", command=self.envoyer_commande,width=10,height=2 ,anchor='nw')
        #fléche du haut pour récupérer la commande d'avant       

    def envoyer_commande(self,event=None):
        message = self.saisie.get()#si la saisie n'est pas vide
        if message:
            self.zone_texte.config(state=tk.NORMAL)
            self.zone_texte.insert(tk.END, f">>> {message}\n")
            
            self.commandes.append(message) #c'est pour les réutiliser avec la fléche du haut et pour d'autres besoins
            self.decrypte()

            self.saisie.delete(0, tk.END)
            self.zone_texte.config(state=tk.DISABLED)
            #permet de descendre automatiquement la bar de scroll si la limite visible est dépassé
            #ça évite que l'utilisateur le fasse à chaque nouvelle commande/message
            self.zone_texte.yview_moveto(1.0)
    
    def envoyer_message(self,message):
            self.zone_texte.config(state=tk.NORMAL)
            self.zone_texte.insert(tk.END, f"|| {message}\n")
            self.zone_texte.config(state=tk.DISABLED)
            self.zone_texte.yview_moveto(1.0)

    def raccourci_clavier(self,event):
        
        #Fléche du haut pour réutiliser la commande précedante(peut s'accumulé)
        if event.keysym == 'Up' : 
            self.up+=1
            if self.up<=len(self.commandes):
                self.saisie.delete(0, tk.END)
                self.saisie.insert(tk.END,self.commandes[-self.up])
        else :
            self.up=0
        
        #Fléche droite pour supprimer la saisie
        if event.keysym == 'Down' : 
            self.saisie.delete(0, tk.END)
            
        
    def decrypte(self):
        commande=self.commandes[-1]
        decomposition=convertisseur.decouper_2(commande)
        #vérifie d'abord qu'un arbre a bien été initialisé
        if self.graphe.type == None :
            if decomposition == []:
                self.envoyer_message("créez un arbre d'abord")
                return None
            elif self.graphe.initialisation(decomposition[0]) == True:
                self.envoyer_message("arbre initialiser avec succés")
                return None
            else:
                self.envoyer_message("créez un arbre d'abord")
                return None
            
        #vérifie si la commande existe ou non
        if convertisseur.verifier(self,decomposition) == False :
            return None
        
        #décrypte et vérifie ses paramétres
        parametres=[]
        for element in decomposition[1:-2]:
            parametres.append(convertisseur.convertir(element))

        print(decomposition)
        print(parametres)

        if False in parametres:
            return self.envoyer_message("Paramètre érronée")


        #Si jusque là tout est bon alors la commande est envoyé
        #elle subira éventuellement un autre traitemant dans les méthodes car il n'est pas possible de faire du cas par cas
        #mais l'essentiel du traitement et de vérification est produit 
        self.master.canv.mise_a_jour()

class convertisseur:
    def decouper(commande):
        decomposition=[]
        indice=[]
        for c in range(len(commande)):
            if commande[c] == "(":
                decomposition.append(commande[:c])
                indice.append(c)
            elif commande[c]==',' and len(decomposition)!=0:
                decomposition.append( commande[indice[-1]+1:c]) 
                indice.append(c)
            elif commande[c]==')' and len(decomposition)!=0:
                decomposition.append( commande[indice[-1]+1:c]) 
        return decomposition
    
    def decouper_2(commande):
        decomposition=[]
        indice=[]
        for c in range(len(commande)):
            #début des paramètres
            if commande[c] == "(":
                indice.append(c)
                decomposition.append(commande[:c])
        
        for i in range(len(commande[c:])):
            if commande[i] == '[':
                decomposition.append(commande[indice[-1]:i])
                indice.append(i)
            elif commande[i] == ']' and commande[indice[-1]]=='[':
                decomposition.append(commande[indice[-1]:i])
                indice.append(i)
            elif commande[i] == ',' :
                if commande[indice[-1]]!='[':
                    decomposition.append(commande[indice[-1]:i])
                    indice.append(i)

        return decomposition
  
    
    def convertir(element):
        info={}
        for c in range(len(element)) :
            if element[0] == '"' :
                info['type']=str
                if element[-1] == '"':
                    info['valeur']=element[1:-1]
                else :
                    return False
            
            elif element[0] in [str(i) for i in range(10)]:
                try :
                    valeur=int(element)
                    info['type']=int
                    info['valeur']=valeur
                except ValueError:
                    return False
            
            elif element[0] =='[':
                liste=[i for i in element]
                print(liste)
                for i in range (len(liste)-1):
                    if liste[i] in [",","[","]"]:
                        liste.pop(i)
                    info['type']=list
                    info['valeur']=liste
        if info == {}:
            return False
        return info

    def verifier(console,commande):
        if commande == []:
            console.envoyer_message("Commande Fausse")
            return False
        for type_arbre in console.graphe.commandes:
            for fonction in console.graphe.commandes[type_arbre]:
                if fonction == commande[0] and console.graphe.type == type_arbre:
                    console.envoyer_message("Commande éxécuté avec succés")
                    return True
                elif fonction == commande[0] and console.graphe.type != type_arbre:
                    console.envoyer_message("Bonne commande mais elle n'est pas compatible avec votre type de graphe")
                    return False

        console.envoyer_message("Commande Fausse")
        return False

