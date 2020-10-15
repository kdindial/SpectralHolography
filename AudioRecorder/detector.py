from PyQt5.QtMultimedia import (QAudio, QAudioFormat, QAudioInput)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout)
from PyQt5.QtCore import (pyqtSlot, pyqtSignal)
import numpy as np

from emitter import Emitter


class Detector(QAudioInput):

    dataReady = pyqtSignal(np.ndarray)
    
    def __init__(self, *args, **kwargs):
        
        format = QAudioFormat()
        format.setCodec("audio/pcm")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        format.setChannelCount(1)
        format.setSampleSize(16)
        format.setSampleRate(44100)

        super(Detector, self).__init__(format, *args, **kwargs)

    @pyqtSlot(QAudio.State)
    def handleStateChanged(self, state):
        if state == QAudio.ActiveState:
            self.buffer = self.start()
        elif state == QAudio.IdleState:
            self.stop()
            self.data = np.frombuffer(self.buffer.readAll(), dtype=np.int16)
            self.dataReady.emit(self.data)
        
    @pyqtSlot(QAudio.State)
    def report(self, state):
        if state == QAudio.IdleState:
            print(self.data)
        
        
class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.emitter = Emitter(self)
        self.detector = Detector(self)
        self.configureUI()
        self.connectSignals()

        self.emitter.duration = 0.1
        
    def configureUI(self):
        self.bStart = QPushButton('Start')
        self.bStop = QPushButton('Stop')
        layout = QVBoxLayout()
        layout.addWidget(self.bStart)
        layout.addWidget(self.bStop)
        self.setLayout(layout)
        
    def connectSignals(self):
        self.bStart.clicked.connect(self.emitter.play)
        self.bStop.clicked.connect(self.emitter.doStop)
        self.emitter.stateChanged.connect(self.detector.handleStateChanged)
        self.emitter.stateChanged.connect(self.detector.report)


def main():
    app = QApplication([])

    a = Example()
    a.show()
    
    app.exec_()

    
if __name__ == '__main__':
    main()


    
