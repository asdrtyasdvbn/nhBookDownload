import requests
from bs4 import BeautifulSoup as BSoup

header = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' }
specChars = ['/' , '\\' , '|' , '*' , '?' , ':' , '<' , '>' , '"' ]
changeChars = { '/':'／' , '\\':'＼' , '|':'｜' , '<':'＜' , '>':'＞' , '?':'？' , ':':'：' , '"':'＂' , '*':'＊' }


class getImgUrl:
    def __init__(self, nhUrl :str):
        req = requests.get( nhUrl, headers = header ).text
        soup = BSoup(req,"html.parser")

        # html example 
        # <h2>(シンデレラ☆ステージ7STEP) [少女遺伝子 (綾瀬)] 歪みの扉 (アイドルマスター シンデレラガールズ)</h2>
        # <div class="thumb-container">
        #  <a class="gallerythumb" href="/g/132052/1/" rel="nofollow">
        #   <img data-src="https://t.nhentai.net/galleries/805708/1t.jpg"
        #  </a>
        # </div>

        # select title by h2 tag
        self.bookTitle  = soup.select("h2")[0].string

        # check illegal characters in title
        for x in range(9):
            if specChars[x] in self.bookTitle:
                self.bookTitle = self.bookTitle.replace( specChars[x] , changeChars[specChars[x]] )
                print("Illegal Characters, Replace "+ specChars[x] +" by " + changeChars[specChars[x]] )
            else :
                pass
                
        # make a list and append oriImgUrl to list
        self.imgUrlList = []
        # print(soup.select("div.thumb-container")[0])
        for data in soup.select("div.thumb-container"):
            self.imgUrlList.append(data.a.img.get("data-src").replace('t.nhe','i.nhe').replace('t.','.'))

        self.bookPages  = len(self.imgUrlList)


if __name__ == "__main__":
    obj = getImgUrl("https://nhentai.net/g/224383/")
    print(obj.imgUrlList[0].split('/')[-1].split('.')[0])
    print(obj.bookPages)