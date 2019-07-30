import os, sys
import threading
import queue
import time

import getImgUrl
import threadDownload

class gentleman():
    def __init__(self):
        # establish gentleman
        print("\n###############################################################################\n")

    def downloadImg(self, url :str):
        self.url = url
        self.urlObj = getImgUrl.getImgUrl(self.url)
        print("Title\t: %s" % self.urlObj.bookTitle )
        print("Pages\t: %s" % self.urlObj.bookPages )

        # if download dir (books) not exist , mkdir
        if not os.path.isdir("books"):
            os.mkdir("books")
        # create dir with bookTitle as dir name
        try:
            os.mkdir("books/"+self.urlObj.bookTitle)
        except Exception as e:
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
            print("Status\t: Accident Happened, plz Check Download Data.")
            print("Error\t: %s" %str(e))

        else:
            print("Status\t: All Done.")
            print("Error\t: ")
        finally:
            print("Cost\t: Total %s Secs." %str(time.time()-stt))
    
    def __del__(self):
        os.system('pause')

if __name__ == "__main__":

    exitGentleman = 0
    Gentleman = gentleman()

    while ( exitGentleman == 0 ) :
        print("> Input nhUrl 'https://nhentai.net/g/XXXXXX/' to Download, 0 to Exit")
        url = str(input())

        if ( url == '0' ) :
            print("\n> Exit.")
            break
        else :    
            Gentleman.downloadImg(url)
        print("\n###############################################################################\n")

    Gentleman = None