from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import favicon
import re
from flask import request, g
import pyppeteer
import asyncio

#global vars:
Phishing = -1
Legitimate = 1
Suspicious = 0

#1.1.1
def is_ip(url):
    if url.replace('.', '').isnumeric() or not url.split('.')[-1].isalpha():
        return Phishing
    
    return Legitimate

#1.1.2
def longUrl(url):
    if len(url) < 54:
        return Legitimate
    elif len(url) >= 54 and len(url) <= 75:
        return Suspicious

    return Phishing


#1.1.3
def tinyUrl(refferer):
    tinyurlArray = [ "bitly.com" , "rebrandly.com" , "short.io" , "linklyhq.com" , "clickmeter.com" , "bl.ink" , "cutt.ly" , "manage.smarturl.it" , "soo.gd" , "tinycc.com" , "clkim.com" , "tinyurl.com" , "pixelme.me" , "t2mio.com" , "tiny.ie" , "shorturl.at" , "bit.do" , "yourls.org" , "musicjet.com" , "adf.ly" , "is.gd" ]
    if refferer in tinyurlArray:
        return Phishing
    return Legitimate

#1.1.4
def hasSymbolInUrl(url): 
    if "@" in url:
        return Phishing
    return Legitimate

#1.1.5
def rederectingUrl(url): 
    if url.index("//") > 7:
        return Phishing
    return Legitimate

#1.1.6
def minusInUrl(url):
    if "-" in url:
        return Phishing
    return Legitimate

#1.1.7
def subDomainsInUrl(url):
    if url.count(".")  == 1:
        return Legitimate
    elif url.count(".") == 2:
        return Suspicious

    return Phishing


#1.1.10
def faviconUrl(url):
    icons = favicon.get(url)
    favicon1 = icons[0] #get the favicon
    parsedfavicon = urlparse(favicon1.url)
    parsedUrl = urlparse(url)
    if parsedfavicon.netloc == parsedUrl.netloc:#check if they have the same hostname\netloc
        return Legitimate
    return Phishing #if not return Phishing

#1.1.11
def nonstandardPort(url):
    parsedUrl = urlparse(url)
    if (parsedUrl.port == 21 or parsedUrl.port == 22 or parsedUrl.port == 23 or parsedUrl.port == 445 or parsedUrl.port == 1433 or parsedUrl.port == 1521 or parsedUrl.port == 3306 or parsedUrl.port == 3389 ):
        return Phishing
    
    return Legitimate 

#1.1.12
def httpsInUrl(url):
    if url.count("https") == 2 or url.index("https") > 7:
        return Phishing
    return Legitimate


#1.2.1
def internalUrlRequests(soup, url):
    internalCounter = 0
    externalCounter = 0
    parsedUrl = urlparse(url)
    imgTags = soup.find_all("img")
    for tag in imgTags:
        srcOfImg = (tag.get("src"))
        if srcOfImg[0] == "/":
            internalCounter += 1
        elif urlparse(srcOfImg).netloc == parsedUrl.netloc:
            print(urlparse(srcOfImg).netloc)
            print(parsedUrl.netloc)
            internalCounter += 1
        else:
            externalCounter += 1
    
    if len(imgTags) == 0: #no img elements
        return Legitimate

    if(externalCounter / (externalCounter + internalCounter) > 0.61): #pracentage specified in feature docs
        return Phishing

    elif(externalCounter / (externalCounter + internalCounter) < 0.22):
        return Legitimate
    
    return Suspicious
 
    

#1.2.2
def internalUrlRequestsinA(soup, url):
    internalCounter = 0
    externalCounter = 0
    parsedUrl = urlparse(url)
    aTags = soup.find_all("a")
    for atag in aTags:
        hreftag = (atag.get("href"))
        if urlparse(hreftag).netloc == parsedUrl.netloc: #check if they have the same netloc
            internalCounter += 1

        elif urlparse(hreftag).netloc == "": #if a.href is empty then is internal.
            internalCounter += 1

        else:
            externalCounter += 1
    
    if len(aTags) == 0: #no A elements
        return Legitimate

    if(externalCounter / (externalCounter + internalCounter) > 0.67): #pracentage specified in feature docs
        return Phishing

    elif(externalCounter / (externalCounter + internalCounter) < 0.31):
        return Legitimate
    
    return Suspicious


#1.2.3
def internalUrlRequestsinMetaScriptsLink(soup , url):
    URL_REGEX = "(ftp:\/\/|www\.|https?:\/\/){1}[a-zA-Z0-9u00a1-\uffff0-]{2,}\.[a-zA-Z0-9u00a1-\uffff0-]{2,}(\S*)"
    internalCounter = 0
    externalCounter = 0
    parsedUrl = urlparse(url)
    linkTags = soup.find_all("link")
    for linkElement in linkTags:
        hrefofElemet = (linkElement.get("href"))
        if urlparse(hrefofElemet).netloc == parsedUrl.netloc: #check if they have the same netloc
            internalCounter += 1

        elif urlparse(hrefofElemet).netloc == "": #if a.href is empty then is internal.
            internalCounter += 1

        else:
            externalCounter += 1


    scrpitTags = soup.find_all("script")
    for scriptElement in scrpitTags:
        srcOfElemnt = scriptElement.get("src")
        if urlparse(srcOfElemnt).netloc == parsedUrl.netloc:
            internalCounter += 1

        elif urlparse(srcOfElemnt).netloc == "": #if a.href is empty then is internal.
            internalCounter += 1
        
        else:
            externalCounter += 1
    
    metaTags = soup.find_all("meta")
    for element in metaTags:
        elementHasOwnProperty = element.get("hasOwnProperty")
        if elementHasOwnProperty:
            if elementHasOwnProperty("content"): #checks if the element has the propertyt to check
                urls = re.findall(URL_REGEX, elementHasOwnProperty.content) #gets all urls in 
                print(urls)
                for url1 in urls:
                    if urlparse(url1).netloc == parsedUrl.netloc: #if same host name of tab and  url in element
                        internalCounter += 1

                    else:
                        externalCounter += 1
            else:
                internalCounter += 1 # if no .hasOwnProperty then it is an internal element
        else:
            internalCounter += 1    
            
    if (externalCounter == 0  and internalCounter == 0) : #if no elements found then its legitimate 
        return Legitimate
    
    if (externalCounter / (externalCounter + internalCounter) > 0.81): #pracentage specified in feature docs
        return Phishing
    
    elif (externalCounter / (externalCounter + internalCounter) < 0.17):
        return Legitimate
    
    return Suspicious



#1.2.4
def getIsSFH(soup, url):
    parsedUrl = urlparse(url)
    formTags = soup.find_all("form")
    for element in formTags:
        if element.get("action") != None: #check if there is a action in the tag
            if element.get("action") == 'about:blank': 
                return Phishing
            
            if urlparse(element.get("action")).netloc == parsedUrl.netloc: #check if they have the same netloc \ hostname
                return Legitimate

            else:
                return Suspicious
    
    return Legitimate #if there is no elemts then its legitimate.


#1.3.5
def usingIframe(soup):
    arrayOfIframeTags = soup.find_all("iframe")
    if(len(arrayOfIframeTags) > 0): #check if there are iframe tags
        return Phishing
    
    else:
        return Legitimate



async def web_scraping(url , browser = False):  
    # launches a chromium browser, can use chrome instead of chromium as well.
    print("in web scraping")
    is_local_browser = True
    if not browser:
        print("in gi")
        is_local_browser = False
        browser = await pyppeteer.launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
    # creates a blank page
    print("opened browser")
    page = await browser.newPage()
    # follows to the requested page and runs the dynamic code on the site.
    print("url is: ", url)
    await page.goto(url)
    print("after goto")
    # provides the html content of the page
    cont = await page.content()

    soup = BeautifulSoup(cont, "html.parser")
    
    
    ArrayOfFeatures = []
    ReffererOfPage = await page.goBack() #get the reffer of the page

    ArrayOfFeatures.append(is_ip(url)) #1.1.1
    ArrayOfFeatures.append(longUrl(url)) #1.1.2
    ArrayOfFeatures.append(tinyUrl(ReffererOfPage)) #1.1.3
    ArrayOfFeatures.append(hasSymbolInUrl(url)) #1.1.4
    ArrayOfFeatures.append(rederectingUrl(url)) #1.1.5
    ArrayOfFeatures.append(minusInUrl(url)) #1.1.6
    ArrayOfFeatures.append(subDomainsInUrl(url)) #1.1.7
    ArrayOfFeatures.append(faviconUrl(url)) #1.1.10 
    ArrayOfFeatures.append(nonstandardPort(url))#1.1.11
    ArrayOfFeatures.append(httpsInUrl(url)) #1.1.12
    ArrayOfFeatures.append(internalUrlRequests(soup, url))    #1.2.1
    ArrayOfFeatures.append(internalUrlRequestsinA(soup, url)) #1.2.2
    ArrayOfFeatures.append(internalUrlRequestsinMetaScriptsLink(soup, url))  #1.2.3
    ArrayOfFeatures.append(getIsSFH(soup,url))  #1.2.4
    ArrayOfFeatures.append(usingIframe(soup))  #1.3.5

    if is_local_browser:
        await browser.close()
    print("finished web scraping")
    return ArrayOfFeatures

# loop = asyncio.get_event_loop()
# loop.run_until_complete(web_scraping("https://www.w3schools.com/python"))

#if __name__ == "__wep_scraping__":
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(main())

