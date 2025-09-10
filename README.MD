# Projet VueAstro

## Description

VueAstro est une application pour les images astronomiques FITS créée en python. 
L'application permet de visualiser, manipuler et enregistrer des images astronomiques sur galaxies, des nébuleuses, des amas stellaires et d'autres objets célestes.

## Fonctionnalités

- **Téléchargement** : Télécharge automatiquement les images FITS depuis `astroquery.skyview`.
- **Affichage** : Affiche les images avec des filtres rouge, bleu et infrarouge.
- **Contrôle des Filtres** : Activation/désactivation des filtres et ajustement de leur intensité.
- **Zoom** : Possibilité de zoom vers l'avant et vers l'arrière.
- **Sauvegarde** : Enregistre l'image affichée au format PNG.

## Prérequis

- Python 3.9+
- Bibliothèques Python :
  - PyQt6
  - matplotlib
  - astropy
  - astroquery
  - scipy
  
- Installation des dépendances nécessaires :
  - Windows :
    ```bash
    pip install -r requirements.txt
    ```
  - Linux :
    ```bash
        pip3 install -r requirements.txt
    ```

## Exécution

Exécution de l'application :
   ```bash
   python Application.py
   ```

## Développeurs

- **BARANGER Phoedora**
- **GERME Charlotte**
