# Neural_Network_clothes

Date: 2019-05-17

## Explication
Ceci est un program qui a pour objectif de décrire un habit à partir d'une image.  
Pour la réalisation de ce projet **Python**, je me suis servie Principalement des librairies Keras pour le réseau de neurone convolutif et CV2 pour le preprocessing.  

Il est possible de lancer un entrainement du reseau de neurone(RN) avec la fonction `train()` de la classe network.  
Le Reseau reconnait a 84% les elements de l'image a condition que l'image soit propre.  
Le fichier **json** représente le modèle du RN et le **. h4** représente ses poids. Ils sont tous les deux charger au lancement du program.  

## Initialisation

Les commandes suivante s'addresse au utilisateur linux.

### Premiere etape

* Ce projet est réalisé en python, il est donc necesaire de crée un environnement `python3 -m venv env`. 
* `source env/bin/activate`
* Il est nécessaire d'installer toutes les librairies avec la commande `pip install -r requirement.txt`

### Lancer le Program

* `python main.py "votre Path de l'image"`

#### Exemple

`python main.py "test_set/tshirt_01.jpg"`  
`>> L'image est un T-shirt noir`  

## Warning

Le programme ne peut reconnaitre que les vetements sur fond blanc non porter.  
Le dossier `test_set` contient des examples d'images valide.  
