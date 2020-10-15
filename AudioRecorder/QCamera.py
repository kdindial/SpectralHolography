from PyQt5.QtWidgets import (QApplication, QWidget)
from emitter import Emitter
from detector import Detector
from wCamera import Ui_wCamera


class QCamera(QWidget):

    def __init__(self):
        super(QCamera, self).__init__()
        self.ui = Ui_wCamera()
        self.ui.setupUi(self)
        self.emitter = Emitter()
        self.detector = Detector()
        self.plot = self.ui.wPlot.plot()
        self.connectSignals()

        self.emitter.window=False
        self.emitter.duration = 2.
        self.emitter.frequency=880.

    def connectSignals(self):
        self.ui.bMeasure.clicked.connect(self.emitter.play)
        self.emitter.stateChanged.connect(self.detector.handleStateChanged)
        self.detector.dataReady.connect(self.plot.setData)

        
def main():
    app = QApplication([])
    camera = QCamera()
    camera.show()
    app.exec_()

    
if __name__ == '__main__':
    main()
    

