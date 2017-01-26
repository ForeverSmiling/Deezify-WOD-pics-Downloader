from bs4 import BeautifulSoup
import urllib.request
import time

minPage = 160
maxPage = 200
wodLinks = []
mainurl = 'http://deezify.com'
defaulturl = mainurl + '/train/wod.html'
imageUrls = []
pauseTime = 0.5
imagesFolder = "C:/Users/serg/Downloads/222/"

def addToWodList(page):
    if not page: return
    for title in page.find_all('h2', 'item-title'):
        titleLink = title.find('a')
        if titleLink:
            wodLinks.append(mainurl + titleLink.get('href'))

def parseWodPage(wodPageLink):
    if not wodPageLink: return
    time.sleep(pauseTime)
    request = urllib.request.Request(wodPageLink)
    if not request: return
    response = urllib.request.urlopen(request)
    if not response: return
    soup = BeautifulSoup(response, 'lxml')
    if not soup: return
    allText = soup.find('div', 'itemFullText')
    if allText:
        addToImageList(allText)
    return

def addToImageList(article):
    if not article: return
    for image in article.find_all('img'):
        imageUrls.append(mainurl + image.get('src'))
    nextElem = article.find('span', 'myjsp-next')
    if nextElem and nextElem.find('a'):
        nextUrl = mainurl + nextElem.find('a').get('href')
        parseWodPage(nextUrl)


request = urllib.request.Request(defaulturl)
response = urllib.request.urlopen(request)
soup = BeautifulSoup(response, 'lxml')

addToWodList(soup)

#print(wodLinks)

for pageNumber in range(minPage, maxPage + 10, 10):
    time.sleep(pauseTime)
    url = defaulturl + '?start=' + str(pageNumber)
    request = urllib.request.Request(url)
    if not request: break
    response = urllib.request.urlopen(request)
    if not response: break
    soup = BeautifulSoup(response, 'lxml')
    if not soup: break
    addToWodList(soup)

print(wodLinks)

for wodPage in wodLinks:
    parseWodPage(wodPage)

print(imageUrls)

for imageUrl in imageUrls:
    time.sleep(pauseTime/2)
    imageName = imageUrl.rsplit('/',1)[1]
    urllib.request.urlretrieve(imageUrl,imagesFolder + imageName)