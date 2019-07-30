import os, sys
import threading
import queue
import time

import getImgUrl
import gentleman_ui
import threadDownload

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

class gentleman(QMainWindow):
    def __init__(self):
        super().__init__()
        self.myui = gentleman_ui.Ui_MainWindow()
        self.myui.setupUi(self)

        self.myui.downloadBtn.clicked.connect(self.downloadImg)

    @pyqtSlot()
    def downloadImg(self):
        self.urlObj = getImgUrl.getImgUrl(self.myui.urlInput.text())
        # show Title, Pages on MainWindow 
        self.myui.showTitle.setText(self.urlObj.bookTitle)
        self.myui.showPages.setText(str(self.urlObj.bookPages))
        self.myui.showError.setText('')
        self.myui.showTimeCost.setText('')

        # if download dir (books) not exist , mkdir
        if not os.path.isdir("books"):
            os.mkdir("books")
        # create dir with bookTitle as dir name
        try:
            os.mkdir("books/"+self.urlObj.bookTitle)
        except Exception as e:
            self.myui.showError.setText(str(e))
            print(e)
        # create queues

        downloadQueue = queue.Queue()
        for i in range( self.urlObj.bookPages ):
            downloadQueue.put(self.urlObj.imgUrlList[i])

        # create queue workers and semaphore 
        queueWorker = []
        workers = 15
        semaphore = threading.Semaphore(workers)
        stt = time.time()
        try:
            for i in range(workers):
                queueWorker.append( threadDownload.downloadWorker( downloadQueue, semaphore, self.urlObj.bookTitle ) )
                queueWorker[i].start()
            # wait for all trds done
            for i in range(workers):
                queueWorker[i].join()
        except Exception as e:
            self.myui.showStatus.setText("Accident Happened, plz Check Download Data.")
            self.myui.showError.setText(str(e))
            print(e)
        else:
            self.myui.showStatus.setText("All Done.")
        finally:
            self.myui.showTimeCost.setText("Total "+ str(time.time()-stt) +" Secs" )
            print("Total "+ str(time.time()-stt) +" Secs" )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = gentleman()
    widget.show()
    sys.exit(app.exec_())