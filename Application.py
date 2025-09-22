# BARANGER Phoedora
# GERME Charlotte
# BUT2 TD3 App
import sys
from PyQt6.QtWidgets import QApplication
from VueAstro import VueAstro

class Application():

    if __name__ == "__main__":

        app = QApplication(sys.argv)
        viewer = VueAstro()
        viewer.show()
        sys.exit(app.exec())