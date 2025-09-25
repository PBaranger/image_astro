# BARANGER Phoedora
# GERME Charlotte
# BUT2 TD3 App

from astropy.io import fits
import numpy as np
from scipy.ndimage import zoom

class ImageAstro():
    def __init__(self, image1, image2, image3):
        super().__init__()
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.liste_image = []

    def normalize_data(self, red=True, blue=True, ir=True, red_intensity=1.0, blue_intensity=1.0, ir_intensity=1.0):
        """Normalise les images FITS"""
        
        # self.liste_image = [
        #     fits.getdata(self.image1),
        #     fits.getdata(self.image2),
        #     fits.getdata(self.image3)
        # ]
        
        self.liste_image = [
            (fits.open(self.image1))[0].data.copy(),
            (fits.open(self.image2))[0].data.copy(),
            (fits.open(self.image2))[0].data.copy()
        ]
        
        color = []
        for img in self.liste_image:
            vmin, vmax = np.percentile(img, [1, 99])
            normalized = np.clip((img - vmin) / (vmax - vmin), 0, 1)
            color.append(normalized)
        colorFilter = []
        if red:
            colorFilter.append(color[0] * red_intensity)
        else:
            colorFilter.append(np.zeros_like(color[0]))
        if blue:
            colorFilter.append(color[1] * blue_intensity)
        else:
            colorFilter.append(np.zeros_like(color[1]))
        if ir:
            colorFilter.append(color[2] * ir_intensity)
        else:
            colorFilter.append(np.zeros_like(color[2]))
        self.colors = np.dstack([colorFilter[0], colorFilter[1], colorFilter[2]])

