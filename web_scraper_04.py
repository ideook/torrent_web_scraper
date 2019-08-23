#!/usr/bin/env python3
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import subprocess
import re
import json
import web_scraper_lib

webpage_addr = [
        "https://torrentwal.com/torrent_variety/torrent",
        "https://torrentwal.com/torrent_tv/torrent"
        ]

class site_scraper:
    def __init__(self, JD):
        self.sitename = "torrentwal"
        self.name = "web_scraper_04"
        self.mainUrl = "https://torrentwal.com"
        self.JD = JD

        self.kortv_ent_id = JD.get('history').get("%s_kortv_ent" % (self.sitename))
        self.kortv_drm_id = JD.get('history').get("%s_kortv_drm" % (self.sitename))

    def saveNewLatestIDwithCate(self, category, newId):
        tmp = self.JD.get('history')
        if category == 'kortv_ent':
            tmp.update(torrentdal_kortv_ent = newId)
            self.kortv_ent_id = newId
        elif category == 'kortv_drm':
            tmp.update(torrentdal_kortv_drm = newId)
            self.kortv_drm_id = newId
        else:
            print("Something Wrong, category = %s" % category)
        
        self.JD.set('history', tmp)
        return

    def needKeepGoing(self, category, id):
        tmp = None
        if category == 'kortv_ent':
            tmp = self.kortv_ent_id
        elif category == 'kortv_drm':
            tmp = self.kortv_drm_id
        else:
            print("Something Wrong, category = %s" % category)
            return False
        
        if id > tmp:
            return True
        
        return False

    def getMainUrl(self):
        return self.mainUrl

    def checkMainUrl(self):
        ret = web_scraper_lib.checkUrl(self.mainUrl)
        return ret

    def getName(self):
        return (self.name)
                
    def getScrapUrl(self, cateIdxNo, count):
        return (webpage_addr[cateIdxNo]+str(count)+".htm")
                
    def getParseData(self, url):
        bsObj = web_scraper_lib.getBsObj(url)
        nameList = bsObj.find('table', attrs={'class' : 'board_list'})
        nameList = nameList.find_all('a', href=re.compile("(.*torrent)(.*html)"))
        return nameList

    #url을 기반으로 wr_id text를 뒤의 id parsing 
    def get_wr_id(self, url):

        tmp = url.rfind('/')
        #tmp = url.rfind('wr_id=')
        if (tmp < 0): # 둘다 검색 못하면 포기
            return 0
        else:
            checkStr = '/' #'wr_id='

            startp = tmp+len(checkStr)
            endp = startp
           
            for endp in range(startp,len(url)):
                if (url[endp]).isdigit():
                    continue
                else:
                    endp = endp-1
                    break
        
            endp = endp+1
        return int((url[startp:endp]))

    def getmagnetDataFromPageUrl(self, url):
        
        bsObj = web_scraper_lib.getBsObj2(url)
        
        
        magnet = bsObj.find('a', href=re.compile("(.*magnet.*)(.*xt=.*)"))
        magnet = magnet.get('href')

        #print(magnet)
        return magnet 
