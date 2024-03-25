# Graphe Studio
# ![Logo.png](https://github.com/Wanous/Graphe-Studio/blob/main/Ressources/Logo.png)
<img alt="Taille du code GitHub" src="https://img.shields.io/github/languages/code-size/Wanous/Graphe-Studio?label=taille%20du%20code">

Graphe Studio est un logiciel permettant la création de graphe orienté comme non orienté 
de manière simple ,rapide et efficace destiné à de multiple usage .
Ce logiciel permet non seulement de créer des graphes mais aussi d'intéragire avec en 
appliquant la théorie des graphes .

## Comment utiliser

- Téléchargez Python 3.10 à partir de [ce lien](https://www.python.org/downloads/)
- Téléchargez ce dépôt en utilisant `git clone` ou le bouton de téléchargement
- Ouvrez un terminal dans le dossier où vous avez téléchargé le dépôt
- Exécutez la commande `python -m pip install -r requirements.txt` pour installer les dépendances
- Exécutez la commande `python main.py` pour lancer le programme

## Interface
Le logiciel débutera par une fenêtre dans laquelle vous pourrez choisir un type de graphe à crée 
ou vous pouvez directement en importer un .

Suite à cela vous serez accueilli par l'interface principale dans laquelle vous pourrez laisser
libre cours à votre créativité pour votre graphe .
Aussi l'interface de l'application a été produit avec la bibliothèque Tkinter dont voici une photo 
mettant en valeur les possibilités offertes :

# ![Logo.png](https://github.com/Wanous/Graphe-Studio/blob/main/Ressources/Interface.png)

(Dans cette exemple un fichier `.graf` à été importé)

## Interragir avec votre graphe 
Il est possible d'ajouter,de supprimer ou même de modifier un noeud de 
votre graphe à partir de quelques cliques :

- `Clique gauche sur un noeud` : Modifier ou supprimer un noeud
- `Clique gauche hors d'un noeud` : Ajouter un noeud
- `Clique droit sur un noeud` : permet de le sélectionner pour le déplacer

Voici à quoi ressemble ces menus :
# ![Logo.png](https://github.com/Wanous/Graphe-Studio/blob/main/Ressources/EditionNoeud.png)
# ![Logo.png](https://github.com/Wanous/Graphe-Studio/blob/main/Ressources/CreationNoeud.png)

## Menu

Graphe Studio contient un menu dans lequel vous trouverez tout ce qu'il vous faut pour configurer 
vos préférences comme sauvegarder votre graphe .

Voici un tableau contenant les noms et rôles de chaque menu de la barre :

| Menu | rôle |
| ------ | ------ |
| Fichier | Menu permettant de sauvegarder/importer un graphe `.graf` ,de commmencer un nouveau graphe ,de prendre une photo d'un graphe en `.png` et de quitter le logiciel .|
| Doc | Menu contenant des informations sur les types de graphes que contient le logiciel pour aider.Pratique pour ceux qui ne connaissent pas/oublier ce que sont les graphes .  |
| Console |  Menu permettant l'ouverture de la console ,un outil pour effectuer des opérations avancés sur un graphe comme un parcours en profondeur ou l'algorithme de Dijkstra .  |
| Preferences | Menu permettant de choisir la couleur du tableur et du canevas ainsi que de faire apparaître ou disparaître des informations sur le canevas pour une meilleurs visibilité .Il donne aussi la possiblité de sauvegarder les préférences . |
| Projet | Menu affichant un simple message qui indique que c'est un projet réaliser dans le cadre d'un concours|

  
#### Boutons

Les boutons ambigus sont répertoriés ici, les autres sont faciles à comprendre

- `C` : Effacer l'entrée (et l'ancien résultat)
- `DEL` : Supprimez le dernier caractère de l'entrée
- `d/dx` : Dérivez l'entrée
- `x^n` : Ajoutez `^` à l'entrée (par exemple `2^3` sera `8`)
- `x` : Ajoutez `x` à l'entrée
- `Draw` : Dessinez l'entrée sous forme d'arbre
- `Hist.` : Passer à l'onglet de l'historique
- `=` : Ajoutez `=` à l'entrée
- `EXE` : Calculez l'entrée (ou résolvez l'équation, en fonction de la présence de = dans l'expression)



