from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import re
import glob, os

URL = 'https://apk-dl.com'
HEADER = {'User-Agent': 'Mozilla/5.0'}
total_apks = 0

#16 --26
FREE_GAMES = {'ACTION':'https://apk-dl.com/games/action',
              'ADVENTURE':'https://apk-dl.com/games/adventure',
              'ARCADE':'https://apk-dl.com/games/arcade',
              'BOARD':'https://apk-dl.com/games/board',
              'CARD':'https://apk-dl.com/games/card',
              'CASINO':'https://apk-dl.com/games/casino',
              'CASUAL':'https://apk-dl.com/games/casual',
              'EDUCATIONAL':'https://apk-dl.com/games/educational',
              'MUSIC':'https://apk-dl.com/games/music',
              'PUZZLE':'https://apk-dl.com/games/puzzle',
              'RACING':'https://apk-dl.com/games/racing',
              'ROLE PLAYING':'https://apk-dl.com/games/role-playing',
              'SIMULATION':'https://apk-dl.com/games/simulation',
              'SPORTS':'https://apk-dl.com/games/sports',
              'STRATEGY':'https://apk-dl.com/games/strategy',
              'TRIVIA':'https://apk-dl.com/games/trivia'}

#22 --28
FREE_APPS = {'BOOKS & REFERENCE':'https://apk-dl.com/apps/books-reference',
             'COMICS':'https://apk-dl.com/apps/comics',
             'COMMUNICATION':'https://apk-dl.com/apps/communication',
             'EDUCATION':'https://apk-dl.com/apps/education',
             'ENTERTAINMENT':'https://apk-dl.com/apps/entertainment',
             'HEALTH & FITNESS':'https://apk-dl.com/apps/health-fitness',
             'LIBRARIES & DEMO':'https://apk-dl.com/apps/libraries-demo',
             'LIFESTYLE':'https://apk-dl.com/apps/lifestyle',
             'MEDIA & VIDEO':'https://apk-dl.com/apps/media-video',
             'MEDICAL':'https://apk-dl.com/apps/medical',
             'MUSIC & AUDIO':'https://apk-dl.com/apps/music-audio',
             'NEWS & MAGAZINES':'https://apk-dl.com/apps/news-magazines',
             'PERSONALIZATION':'https://apk-dl.com/apps/personalization',
             'PHOTOGRAPHY':'https://apk-dl.com/apps/photography',
             'PRODUCTIVITY':'https://apk-dl.com/apps/productivity',
             'SHOPPING':'https://apk-dl.com/apps/shopping',
             'SOCIAL':'https://apk-dl.com/apps/social',
             'TOOLS':'https://apk-dl.com/apps/tools',
             'TRANSPORTATION':'https://apk-dl.com/apps/transportation',
             'TRAVEL & LOCAL':'https://apk-dl.com/apps/travel-local',
             'WEATHER':'https://apk-dl.com/apps/weather',
             'WORD':'https://apk-dl.com/apps/word',}


GAMES_QUANTITY = 26
APPS_QUANTITY = 28

def getApkFromUrl(url, section, tipo):
    match = re.search('^(?:[^\/]*\/){4}([^\/]*)', url).groups()[0]

    # retira 'https://' para encodar
    url = quote(url[8:])

    if(checkIfAlreadyDownloaded(match)):
        print(match + ' já baixado. Pulando para o próximo.')
        return

    try:
        response1 = urlopen('https://' + url)
    except:
        print('Error 404. Pulando.[ url = {0} ]'.format(url))
        return
    
    soup1 = BeautifulSoup(response1, 'html.parser')
    urn1 = soup1.find('a', attrs={'class':'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect fixed-size mdl-button--primary'})

    if(urn1 == None):
        deuRuim(url)
        return
    
    response2 = urlopen(URL + urn1['href'])
    soup2 = BeautifulSoup(response2, 'html.parser')
    urn2 = soup2.find('a', attrs={'rel':'nofollow'})

    if(urn2 == None):
        deuRuim(url)
        return

    req = Request(urn2['href'], headers=HEADER)
    response3 = urlopen(req)
    soup3 = BeautifulSoup(response3, 'html.parser')
    urn3 = soup3.find('a', attrs={'class':'mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect fixed-size'})

    if(urn3 == None):
        deuRuim(url)
        return

    download_url = 'http:' + urn3['href']
    
    print("Baixando: " + match)
    global total_apks
    total_apks += 1
    
    r = requests.get(download_url)
    #open('D:\\crawler\\' + tipo + '\\' + section + '\\' + match + '.apk', 'wb').write(r.content)
    open('D:\\crawler\\' + match + '.apk', 'wb').write(r.content)
    print('INFO: ' + str(total_apks) + ' apks baixados.')

def deuRuim(url):
    print('Erro ao baixar este apk. Pulando para o próximo. [ url = {0} ]'.format(url))
    file = open('D:\\crawler\\errorLog.txt','a')

    file.write('Falha ao baixar: ' + url + '\n')

def getApkFromSection(section, sectionUrl, quantity, tipo):
    response = urlopen(sectionUrl)
    soup = BeautifulSoup(response, 'html.parser')
    
    anchors = soup.find_all('a', attrs={'class':'card-click-target'})
    hrefs = []
    for a in anchors:
        hrefs.append(a['href'])
    
    hrefs = remove_duplicate(hrefs)
    
    apps_quantity = len(hrefs)

    if(quantity > apps_quantity):
        print('Quantidade({0}) maior do que número de apps({1}). Nova quantidade = {1}.'.format(quantity, apps_quantity))
        quantity = apps_quantity    

    for count in range(0, quantity):
        #urn = apps[count].find('a', attrs={'class':'card-click-target'})['href']
        print('-> {0}: apk número {1}'.format(section, count))
        url = URL + hrefs[count]

        getApkFromUrl(url, section, tipo)

def checkIfAlreadyDownloaded(fileName):
    os.chdir("D:\\crawler\\")
    
    for file in glob.glob("*.apk"):
        if fileName in file:
            return True

    return False    

def remove_duplicate(l):
    return list(set(l))

def getFreeGames():
    for section, url in FREE_GAMES.items():
        getApkFromSection(section, url, GAMES_QUANTITY, 'games')

def getFreeApps():
    for section, url in FREE_APPS.items():
        getApkFromSection(section, url, APPS_QUANTITY, 'apps')


getFreeGames()
getFreeApps()

print('\n==> APKS BAIXADOS NO TOTAL: ' + str(total_apks))
