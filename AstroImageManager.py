# BARANGER Phoedora
# GERME Charlotte
# BUT2 TD3 App
from astroquery.skyview import SkyView
from astropy import units as u
import os
import shutil
import time
class AstroImageManager:
    def __init__(self, target):
        self.target = target
        self.directory = target.replace(" ", "_")
        self.surveys = ["DSS2 Red", "DSS2 Blue", "DSS2 IR"]
        self.radius = 0.5 * u.deg

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def download_images(self):
        """Télécharge les images FIT"""
        images_by_filter = SkyView.get_images(position=self.target, survey=self.surveys, radius=self.radius, cache=False)

        self.filenames = []
        for survey, fits_file in zip(self.surveys, images_by_filter):
            filename = os.path.join(self.directory, f"{self.target.replace(' ', '_')}_{survey.replace(' ', '_')}.fit")
            fits_file.writeto(filename, overwrite=True)
            self.filenames.append(filename)
            print(f"Fichier sauvegardé :", filename)

        return self.filenames
    
    def delete_images(self):
        """Supprime le dossier contenant les fichiers FIT."""
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
            print("Répertoire supprimé :",self.directory)
            
        self.filenames = []
            
