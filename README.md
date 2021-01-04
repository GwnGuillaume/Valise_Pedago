# Valise pédagogique

Cette valise pédagogique s'adresse aux enseignants en Collège ou Lycée en support à une démarche de sensibilisation des élèves à la problématique des nuisances sonores. Un kit de supports pédagogiques est mis à disposition qui comprend :
* un ensemble de **documents ressources** introduisant les concepts physiques et perceptifs associés au bruit ;
* une application pour la cartographie du bruit en espace clos tel qu'une salle de classe sur la base de mesures acoustiques réalisées à partir de l'application Android gratuite NoiseCapture (https://noise-planet.org/noisecapture.html).

# Documents ressources

Les supports sont disponibles au format pdf dans le dossier : *Documents ressources*.

# Application pour la cartographie du bruit

## Téléchargement et lancement de l'application

### Windows

1. Télécharger l'archive https://ci.appveyor.com/project/GwnGuillaume/valise-pedago/artifacts/build/carto_acoustique_interieure_win32.zip.
2. Décompresser l'archive *carto_acoustique_interieure_win32.zip* dans un dossier.
3. Lancer l'application en double-cliquant sur l'exécutable *carto_acoustique_interieure.exe*.

### Linux

1. Télécharger l'archive : https://github.com/GwnGuillaume/Valise_Pedago/archive/master.zip.
2. Compiler le projet :
   1. Décompresser l'archive *master.zip* dans un dossier avec la commande `$ unzip master.zip -d /chemin_vers_le_dossier`
   2. Aller dans le répertoire des scripts (`$ cd /chemin`) et taper la ligne de commande `$ python setup.py build`
3. Lancer l'application avec la commande : `$ ./carto_acoustique_interieure`

## Interface

Au lancement de l'application, le menu principal s'affiche et propose 2 options :
1. Générer le tableau et l'image de la grille de points de mesures ;
2. Produire la cartographie sonore à partir des mesures.

En cliquant sur *Générer le tableau et l'image de la grille de points de mesures*, l'interface prend l'apparence suivante.
<img src="/images/noisemap_app_grid.png" alt="Grid generation" title="Noise mapping" width="400" height="320" />

En cliquant sur *Produire la cartographie sonore à partir des mesures* dans le menu principal, l'interface prend à présent la forme suivante.
<img src="/images/noisemap_app_measures.png" alt="Noise mapping" title="Noise mapping" width="400" height="320" />

# Remerciements
PRSE Grand-Est
Gwendall Petit
