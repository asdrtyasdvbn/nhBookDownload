import os
import time
import requests
import threading
import queue
import shutil

header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }

def imgDownload( imgUrl :str, title :str, page :int, type :str ):
    # first send get to img url and allow stream
    imgLoad = requests.get( imgUrl, headers = header, stream = True )

    # try to write binary file 
    try:
        img = open("books/"+ title +"/p"+ str(page) + type, 'wb' )
        shutil.copyfileobj( imgLoad.raw, img )
        img.close()

    except Exception as e:
        print(e)

class downloadWorker(threading.Thread):
    def __init__( self, queue, semaphore, title :str):
        super().__init__()
        self.queue = queue
        self.semaphore = semaphore
        self.title = title
    
    def run(self):
        # if still have works
        while (self.queue.qsize()) > 0:
            # acquire semaphore
            self.semaphore.acquire()
            # get urlObj's urls from main program, then do the func: imgDownload
            url = self.queue.get()
            imgType = '.' + url.split('.')[-1]
            page = url.split('/')[-1].split('.')[0]
            imgDownload( url, self.title, page, imgType)
            # after work done, release semaphore
            self.semaphore.release()


if __name__ == "__main__":
    
    testList = ['https://i.nhentai.net/galleries/1185129/1.jpg', 'https://i.nhentai.net/galleries/1185129/2.jpg', 'https://i.nhentai.net/galleries/1185129/3.jpg', 'https://i.nhentai.net/galleries/1185129/4.jpg', 'https://i.nhentai.net/galleries/1185129/5.jpg', 'https://i.nhentai.net/galleries/1185129/6.jpg', 'https://i.nhentai.net/galleries/1185129/7.jpg', 'https://i.nhentai.net/galleries/1185129/8.jpg', 'https://i.nhentai.net/galleries/1185129/9.jpg', 'https://i.nhentai.net/galleries/1185129/10.jpg', 'https://i.nhentai.net/galleries/1185129/11.jpg', 'https://i.nhentai.net/galleries/1185129/12.jpg', 'https://i.nhentai.net/galleries/1185129/13.jpg', 'https://i.nhentai.net/galleries/1185129/14.jpg', 'https://i.nhentai.net/galleries/1185129/15.jpg', 'https://i.nhentai.net/galleries/1185129/16.jpg', 'https://i.nhentai.net/galleries/1185129/17.jpg', 'https://i.nhentai.net/galleries/1185129/18.jpg', 'https://i.nhentai.net/galleries/1185129/19.jpg', 'https://i.nhentai.net/galleries/1185129/20.jpg']
    
    testTitle = "[アズマサワヨシ] あやかし館へようこそ！ 第1-10話 [中国翻訳]"
    
    try:
        if not os.path.isdir("books"):
            os.mkdir("books")
        if not os.path.isdir("books/" + testTitle):
            os.mkdir("books/" + testTitle)
    except:
        print("here")

    testQueue = queue.Queue()
    testPages = 20
    for i in range(testPages):
        testQueue.put(testList[i])

    testWorker = []
    workers = 5
    testSemaphore = threading.Semaphore(workers)
    stt = time.time()
    for i in range(workers):
        testWorker.append( downloadWorker( testQueue, testSemaphore, testTitle ) )
        testWorker[i].start()
    for i in range(workers):
        testWorker[i].join()
    print("cost "+ str(time.time()-stt) +" secs" )