from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

#global vars:
Phishing = -1
Legitimate = 1
Suspicious = 0


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
                urls = element.content.findall(URL_REGEX) #gets all urls in content
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





#just testing with random url
urlToSend = "https://www.w3schools.com/python/python_for_loops.asp"
response = requests.get(urlToSend)

soup = BeautifulSoup(response.content, "html.parser")

#print(type(soup)) #check if the soup type is beautifulsoup
#print(soup.prettify()) #print the html file ,  with all tags.

print(internalUrlRequests(soup, urlToSend))    #1.2.1
print(internalUrlRequestsinA(soup, urlToSend)) #1.2.2
print(internalUrlRequestsinMetaScriptsLink(soup, urlToSend))  #1.2.3
print(getIsSFH(soup,urlToSend))  #1.2.4
print(usingIframe(soup))  #1.3.5


