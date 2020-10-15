from PyQt5.QtMultimedia import (QAudio, QAudioFormat, QAudioOutput)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout)
from PyQt5.QtCore import (QByteArray, QBuffer, QIODevice,
                          pyqtSignal, pyqtSlot, pyqtProperty)
import numpy as np
from scipy.signal import blackmanharris


class Emitter(QAudioOutput):

    finished = pyqtSignal()
    
    def __init__(self, *args, **kwargs):

        format = QAudioFormat()
        format.setCodec('audio/pcm')
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        format.setChannelCount(1)
        format.setSampleSize(16)
        format.setSampleRate(44100)
        
        super(Emitter, self).__init__(format, *args, **kwargs)

        self.buffer = QBuffer()
        self.data = QByteArray()

        self._window = False
        self._frequency = 440
        self._duration = 1
        self.volume = 20000
        
        self.stateChanged.connect(self.handleStateChanged)

    @pyqtProperty(float)
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = float(value)
        self.makeData()

    @pyqtProperty(float)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = float(value)
        self.makeData()

    @pyqtProperty(float)
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = float(value)
        self.makeData()

    @pyqtProperty(bool)
    def window(self):
        return self._window

    @window.setter
    def window(self, state):
        self._window = bool(state)
        self.makeData()

    def makeData(self):
        self.data.clear()
        sampleRate = self.format().sampleRate()
        npts = int(self.duration * sampleRate)
        
        t = np.linspace(0, self.duration, npts)
        signal = self.volume * np.sin(2.*np.pi * self.frequency * t)
        if self.window:
            signal *= blackmanharris(npts)
        encoded_signal = signal.astype(np.int16).tobytes()
        self.data.append(encoded_signal)
        
    @pyqtSlot()
    def play(self):
        self.doStop()
        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        self.start(self.buffer)
    
    @pyqtSlot()
    def doStop(self):
        if self.state() == QAudio.ActiveState:
            self.stop()
        if self.buffer.isOpen():
            self.buffer.close()

    @pyqtSlot(QAudio.State)
    def handleStateChanged(self, state):
        if state == QAudio.IdleState: # finished playing: success!
            self.stop()
        elif state == QAudio.StoppedState: # something wrong!
            pass


class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.emitter = Emitter(self)
        self.configureUI()
        self.connectSignals()
        
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
        
def main():
    app = QApplication([])

    a = Example()
    a.show()
    
    app.exec_()

    
if __name__ == '__main__':
    main()
