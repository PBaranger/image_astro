# BARANGER Phoedora
# GERME Charlotte
# BUT2 TD3 App

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog, QComboBox, QPushButton, QHBoxLayout, QCheckBox, QLabel, QSlider
import matplotlib.pyplot as plt
from PyQt6.QtGui import QCloseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ImageAstro import ImageAstro
from AstroImageManager import AstroImageManager
import time


class VueAstro(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.astronomical_objects = {
            # Galaxies
            "Andromède": "M31",
            "Galaxie du Sombrero": "M104",
            "Galaxie des Chiens de Chasse": "M51",
            "Galaxie d’Andromède satellite": "M32",
            "Galaxie du Triangle": "M33",
            "Centaurus A": "NGC 5128",
            "Galaxie de Bode": "M81",
            "Galaxie du Cigare": "M82",
            
            # Nébuleuses
            "Nébuleuse d’Orion": "M42",
            "Nébuleuse de la Tête de Cheval": "IC 434",
            "Nébuleuse de l’Aigle": "M16",
            "Nébuleuse de la Lyre": "M57",
            "Nébuleuse de la Rosette": "NGC 2237",
            "Nébuleuse du Crabe": "M1",
            
            # Amas Stellaires
            "Amas des Pléiades": "M45",
            "Amas d’Hercule": "M13",
            "Amas Oméga du Centaure": "NGC 5139",
            
            # Objets Divers
            "Pulsar du Crabe": "PSR B0531+21",
            "Quasar 3C 273": "3C 273",
            "Restes de supernova Cassiopée A": "Cassiopeia A",
            "Étoile Polaire": "Alpha Ursae Minoris"
        }
               
        self.nom_dossier = []

        self.setWindowTitle("Image Fits")
        self.resize(800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        self.combo = QComboBox()
        self.combo.addItems(list(self.astronomical_objects.keys()))
        self.combo.currentIndexChanged.connect(self.update_image)
        self.layout.addWidget(self.combo)
        
        self.checkbox_layout = QHBoxLayout()
        self.red_filter = QCheckBox("Filtre Rouge")
        self.blue_filter = QCheckBox("Filtre Bleu")
        self.ir_filter = QCheckBox("Infrarouge")
        self.red_filter.setChecked(True)
        self.blue_filter.setChecked(True)
        self.ir_filter.setChecked(True)
        self.checkbox_layout.addWidget(self.red_filter)
        self.checkbox_layout.addWidget(self.blue_filter)
        self.checkbox_layout.addWidget(self.ir_filter)
        self.layout.addLayout(self.checkbox_layout)
        
        self.slider_layout = QVBoxLayout()
        self.red_slider = self.slider("Intensité Rouge", self.update_filters)
        self.blue_slider = self.slider("Intensité Bleu", self.update_filters)
        self.ir_slider = self.slider("Intensité Infrarouge", self.update_filters)
        self.layout.addLayout(self.slider_layout)
        
        self.resetSlider = QPushButton("Reset")
        self.resetSlider.clicked.connect(self.reset_slider)
        self.layout.addWidget(self.resetSlider)
        
        self.saveButton = QPushButton("Sauvegarder")
        self.saveButton.clicked.connect(self.save_image)
        self.layout.addWidget(self.saveButton)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.subplots()
        
        self.zoomPlusButton = QPushButton("Zoom + ")
        self.zoomPlusButton.clicked.connect(self.zoomPlus)
        self.layout.addWidget(self.zoomPlusButton)
        
        self.zoomMoinsButton = QPushButton("Zoom - ")
        self.zoomMoinsButton.clicked.connect(self.zoomMoins)
        self.layout.addWidget(self.zoomMoinsButton)
        
        
        self.red_filter.stateChanged.connect(self.update_filters)
        self.blue_filter.stateChanged.connect(self.update_filters)
        self.ir_filter.stateChanged.connect(self.update_filters)
        
        self.statusBar()       
               
    def slider(self, label, callback):
        slider_layout = QHBoxLayout()
        slider_label = QLabel(label)
        slider_layout.addWidget(slider_label)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.valueChanged.connect(callback)
        slider_layout.addWidget(slider)
        value_label = QLabel(str(slider.value()))
        slider.valueChanged.connect(lambda val: value_label.setText(str(val)))
        slider_layout.addWidget(value_label)
        
        self.slider_layout.addLayout(slider_layout)
        return slider

    def reset_slider(self):
        self.red_slider.setValue(50)
        self.blue_slider.setValue(50)
        self.ir_slider.setValue(50)  
    
    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder l'image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        
        if file_name:
            self.ax.axis('off')
            self.canvas.figure.savefig(file_name, bbox_inches='tight', pad_inches=0)
            self.ax.axis('on')

    def update_image(self, index):
        
        self.statusBar().showMessage("Veuillez patienter le temps du téléchargement. Ne fermer pas la fenêtre.")

        if not (self.red_filter.isChecked() or self.blue_filter.isChecked() or self.ir_filter.isChecked()):
            if index is None:  
                self.red_filter.setChecked(True)
                
        cle_astro = self.combo.currentText()
        target = self.astronomical_objects[cle_astro]
        
        self.manager = AstroImageManager(target)
        self.manager.download_images()
        
        self.imageAstro = ImageAstro(
            f'{target.replace(" ", "_")}/{target.replace(" ", "_")}_DSS2_Red.fit', 
            f'{target.replace(" ", "_")}/{target.replace(" ", "_")}_DSS2_Blue.fit',
            f'{target.replace(" ", "_")}/{target.replace(" ", "_")}_DSS2_IR.fit'
        )
        
        self.imageAstro.normalize_data(
            red=self.red_filter.isChecked(),
            blue=self.blue_filter.isChecked(),
            ir=self.ir_filter.isChecked()
        )
        self.ax.clear()
        self.ax.imshow(self.imageAstro.colors, origin='lower')
        self.ax.axis('on')
        self.canvas.draw()
        
        self.nom_dossier.append(target.replace(' ', '_'))
    
        self.statusBar().showMessage("Téléchargement terminé.")

    def update_filters(self):
        
        if hasattr(self, 'imageAstro') and self.imageAstro is not None:
            red_intensity = self.red_slider.value() / 100.0
            blue_intensity = self.blue_slider.value() / 100.0
            ir_intensity = self.ir_slider.value() / 100.0
            
            self.imageAstro.normalize_data(
                red=self.red_filter.isChecked(),
                blue=self.blue_filter.isChecked(),
                ir=self.ir_filter.isChecked(),
                red_intensity=red_intensity,
                blue_intensity=blue_intensity,
                ir_intensity=ir_intensity
            )
            
            self.ax.clear()
            self.ax.imshow(self.imageAstro.colors, origin='lower')
            self.ax.axis('on')
            self.canvas.draw()
        else:
            self.statusBar().showMessage("Veuillez télécharger une image avant de modifier les filtres.")
        
    def zoomPlus(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        zoom_factor = 0.8 
        
        new_xlim = (xlim[0] + (xlim[1] - xlim[0]) * (1 - zoom_factor) / 2,
                    xlim[1] - (xlim[1] - xlim[0]) * (1 - zoom_factor) / 2)
        new_ylim = (ylim[0] + (ylim[1] - ylim[0]) * (1 - zoom_factor) / 2,
                    ylim[1] - (ylim[1] - ylim[0]) * (1 - zoom_factor) / 2)
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

    def zoomMoins(self):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        
        zoom_factor = 1.2
        
        new_xlim = (xlim[0] - (xlim[1] - xlim[0]) * (zoom_factor - 1) / 2,
                    xlim[1] + (xlim[1] - xlim[0]) * (zoom_factor - 1) / 2)
        new_ylim = (ylim[0] - (ylim[1] - ylim[0]) * (zoom_factor - 1) / 2,
                    ylim[1] + (ylim[1] - ylim[0]) * (zoom_factor - 1) / 2)
        
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()
        
        
    def closeEvent(self,event):
        time.sleep(1)
        for fichier in range(len(self.nom_dossier)):
            fichier1 = AstroImageManager(self.nom_dossier[fichier])
            fichier1.delete_images()
 
    