class Operation_graphe:

    def parcours_profondeur(graphe, s,liste = None):
        """
        Méthode permettant de visualiser le graphe en utilisant le parcours en profondeur à partir d'un point s donné.
        Retourne :
            liste -> liste des points formant le parcours en profondeur
        """
        if not graphe:
            return []
        #Initialisez une liste vide afin d'éviter que celle-ci soit sauvegardée à la fin de chaque utilisation de la fonction
        if liste==None:
            liste=[]
        if not s in liste: #Ajouter le point de départ à la liste s'il n'y est pas
           liste.append(s)
           for v in graphe[s]['adjacent']:
               Operation_graphe.parcours_profondeur(graphe,v,liste) #S'appelle pour chaque voisin non visité
        return liste
    
    def parcours_chemin(graphe, s):
        """
        Méthode pour parcourir le graphe en utilisant le parcours en largeur à partir d'un point s donné.
        Retourne:
            index: Dictionnaire contenant les nœuds visités avec leur prédécesseur comme valeur.
        """
        file_attente = []  # File d'attente pour les noeuds à explorer
        liste = {s: None}  # Dictionnaire pour stocker les noeuds visités et leur prédécesseur
        index = {s: 0}  # Indice pour suivre le prochain noeud à explorer dans la file d'attente

        while len(liste) > 0:
            s = liste.popitem()[0]

            # Ajoute les voisins non visités du noeud actuel à la file d'attente
            for voisin in graphe[s]['adjacent']:
                if voisin not in index:
                    file_attente.append(voisin)
                    index[voisin] = s  # Stocke le prédécesseur du voisin

            # Si la file d'attente est vide, met à jour la liste et la file d'attente
            if len(liste) == 0:
                for node in file_attente:
                    liste[node] = index[node]
                file_attente.clear()

        return index

    def chemins(graphe, x, y):
        """
        Méthode pour trouver le plus court chemin depuis le sommet x jusqu'au sommet y.
        Paramètres:
            x: Point de départ du chemin.
            y: Point de destination du chemin.

        Retourne:
            chemin: Liste représentant le plus court chemin de x à y.
        """
        x,y
        parcours = Operation_graphe.parcours_chemin(graphe,x)
        chemin = [y]
        while y != x:
            y = parcours[y]
            chemin.append(y)
        chemin.reverse() #Après avoir rempli à reculons 'chemin' grâce à append, inverse la liste pour l'afficher
        return chemin
    
    def parcours_largeur(graphe, s):
        """
        Méthode permettant de visualiser le graphe en utilisant le parcours en largeur à partir d'un point s donné.
        Retourne :
            index -> liste des points formant le parcours en largeur
        """        
        file_attente = []  # File d'attente pour les noeuds à explorer
        liste = {s}  # Liste pour stocker les noeuds visités
        index = [s]  # Liste pour suivre le prochain noeud à explorer dans la file d'attente
    
        while len(liste) > 0:
            s = liste.pop()
    
            # Ajoute les voisins non visités du noeud actuel à la file d'attente
            for voisin in graphe[s]['adjacent']:
                if voisin not in index:
                    file_attente.append(voisin)
                    index.append(voisin)
            if len(liste)==0:
                liste,file_attente=file_attente,[]
        
        return index
    
    def matrice(graphe):
        """
        Méthode pour afficher la matrice d'adjacence du graphe
        Retourne :
            m : matrice d'adjacence du graphe associé
        """
        m=[]
        k=graphe.keys()
        for i in range(len(k)): #Création d'une matrice vide
            r=[0]*len(k)
            m.append(r)
        sommets = sorted(k) #Tri des sommets du graphe
        for sommet, categorie in graphe.items():
            index = sommets.index(sommet) #Cherche l'indice du sommet étudié
            for v in categorie['adjacent']:
                voisin = sommets.index(v) #Cherche l'indice du sommet adjacent
                m[index][voisin] = 1
        return m
    




