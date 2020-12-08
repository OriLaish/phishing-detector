const Phishing = -1
const Legitimate = 1
const Suspicious = 0

//1.1.1
function IPInAdress(url){
    checkForIP = RegExp('^http[s]?:\/\/((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])');
    let count = (url.match(/0x/g));
    if(count != undefined){
        if(checkForIP.test(url) || count.length == 4) // if count == 4 then its a hexa ip in the url . 
        return Phishing
    
    }
    
    else
        return Legitimate
}

//1.1.2
function URLlength(url){
    if(url.length < 54 )
        return Legitimate

    else if(url.length >= 54 && url.length <= 75)
        return Suspicious

    else
        return Phishing
}

//1.1.3 
function tinyURL(){
    let tinyurl = [ "bitly.com" , "rebrandly.com" , "short.io" , "linklyhq.com" , "clickmeter.com" , "bl.ink" , "cutt.ly" , "manage.smarturl.it" , "soo.gd" , "tinycc.com" , "clkim.com" , "tinyurl.com" , "pixelme.me" , "t2mio.com" , "tiny.ie" , "shorturl.at" , "bit.do" , "yourls.org" , "musicjet.com" , "adf.ly" , "is.gd" ]
    if(document.referrer == "")
        return Legitimate
    let reffererToCheck = new URL(document.referrer);
    if(tinyurl.indexOf(reffererToCheck.hostname) > -1 ) //check if the hostname is in the tinyurl list
        return Legitimate
    
    else
        return Phishing
}



//symbol = "@" 1.1.4 
function symbolInURL(url) {
    if(url.indexOf("@") != -1 ) //if it not equals to -1 it means there is a @ in the url
        return Phishing

    else
        return Legitimate

}

//this function check for the index of the "//" in the url 1.1.5
function redirectingURL(url) {
    if(url.indexOf("//") > 7)
        return Phishing
    
    else
        return Legitimate

}

//1.1.6
function minusInURL(url){
    if(url.indexOf("-") != -1 ) //if it not equals to -1 it means there is a - in the url
        return Phishing

    else
        return Legitimate

}

//1.1.7
function subDomainInUrl(url){
    let count = url.split('.').length - 2
    if (count <= 0)
        return Legitimate
    else if (count == 1) 
        return Suspicious
    return Phishing
}


//1.1.10
function favicon(url){
    const urlObj = new URL(url)
    let favicon = undefined;
    let nodeList = document.getElementsByTagName("link"); //get the favicon
    for (let i = 0; i < nodeList.length; i++)
    {
        if((nodeList[i].getAttribute("rel") == "icon")||(nodeList[i].getAttribute("rel") == "shortcut icon"))
        {
            favicon = nodeList[i].getAttribute("href");
        }
    }
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator

    if(pattern.test(favicon)) //check if the favicon is a url if not its phishing
    {
        const faviconurl = new URL(favicon)
        if(urlObj.hostname == faviconurl.hostname)
            return Legitimate 
    
        else
            return Phishing
    }
    
    else
        return Phishing
}



//1.1.11 check for non standard port
function nonStandardPort(url){
    const getPort = new URL(url)
    if( getPort.port == 21 || getPort.port == 22 || getPort.port == 23 || getPort.port == 445 || getPort.port == 1433 || getPort.port == 1521 || getPort.port == 3306 || getPort.port == 3389 )
        return Phishing
    
    else
        return Legitimate
   


}

//1.1.12 - check if there is a https in the domain that is part of the name of the domain
function httpsInURL(url){

    if(url.indexOf("://") < url.indexOf("https") )
        return Phishing
    else
        return Legitimate
}


//1.2.1
function internalUrlRequests(){
    var internalCounter = 0, externalCounter = 0;
    var homeHost = (new URL(location.href)).hostname;
    var aElements = document.getElementsByTagName("img"); //get all elemnts in specific tag .
    for (element in aElements){
        if(element.href){ //check if the element has herf field
            if(element.href.hostname == homeHost) //if same host name of tab and element
            internalCounter += 1;
        else
            externalCounter += 1;
        }
    }
    if(externalCounter / (externalCounter + internalCounter) > 0.61) //pracentage specified in feature docs
        return Phishing;
    else if(externalCounter / (externalCounter + internalCounter) < 0.22)
        return Legitimate;
    return Suspicious;
}

//1.2.2
function internalUrlRequestsinA(){
    var internalCounter = 0, externalCounter = 0;
    var homeHost = (new URL(location.href)).hostname;
    var aElements = document.getElementsByTagName("a"); //get all elemnts .
    for (element in aElements){

        if(element.href){ //checking if  <a> </a> herf  exist
            let herfOfElement = new URL(element.href)
            if(herfOfElement.hostname == homeHost) //if same host name of tab and element
                internalCounter += 1;
            else
                externalCounter += 1;

        }
    }
    if(externalCounter / (externalCounter + internalCounter) > 0.67) //pracentage specified in feature docs
        return Phishing;
    else if(externalCounter / (externalCounter + internalCounter) < 0.31)
        return Legitimate;
    return Suspicious;
}

//1.2.3 
function internalUrlRequestsinMetaScriptsLink(){
    const URL_REGEX = '(ftp:\/\/|www\.|https?:\/\/){1}[a-zA-Z0-9u00a1-\uffff0-]{2,}\.[a-zA-Z0-9u00a1-\uffff0-]{2,}(\S*)';
    var internalCounter = 0, externalCounter = 0;
    var homeHost = (new URL(location.href)).hostname;

    var elements = document.getElementsByTagName("link"); //get all elemnts of link.
    for (element in elements){
        if(element.href){ //check if herf exist on the elemnt
            
            if(element.href.hostname == homeHost) //if same host name of tab and element
                internalCounter += 1;
            
            else
                externalCounter += 1;
        }

    }

    elements = document.getElementsByTagName("script"); //get all elemnts of script.
    for (element in elements){
        if(element.src){
            if(new URL (element.src).hostname == homeHost) //if same host name of tab and element
                internalCounter += 1;
            else
                externalCounter += 1;
        }
    }

    elements = document.getElementsByTagName("meta"); //get all elemnts of meta.
    for (element in elements){
        if(element.hasOwnProperty('content')){ //checks if the element has the propertyt to check
            urls = element.content.matchAll(URL_REGEX) //gets all urls in content
            for (url in urls){
                if(new URL (url).hostname == homeHost) //if same host name of tab and  url in element
                    internalCounter += 1;
                else
                    externalCounter += 1;
            }
        }
        
    }

    if(externalCounter / (externalCounter + internalCounter) > 0.81) //pracentage specified in feature docs
        return Phishing;
    else if(externalCounter / (externalCounter + internalCounter) < 0.17)
        return Legitimate;
    return Suspicious;

}

//1.2.4
function getIsSFH(){
    var homeHost = (new URL(location.href)).hostname;
    formElement = document.getElementsByTagName("form")[0]; //get all elemnts of meta.
    if(formElement.action == 'about:blank')
        return Phishing;
    if(new URL (formElement.action).hostname == homeHost)
        return Legitimate;
    return Suspicious;
    
}

//1.3.1

//1.3.3

//1.3.5
function usingIFrame(){
    var iFrameElements = document.getElementsByTagName("iframe")
    if(iFrameElements.length > 0)
        return Phishing
    
    else
        return Legitimate
}


//try to get html file
/*let htmlcontent = document.getElementsByTagName("*"); //get all elemnts .
for(i=0; i<htmlcontent.length; i++){
    console.log(htmlcontent[i])
    
}*/
var listOfFeatures = [] ;
listOfFeatures += (IPInAdress(window.location.href))
listOfFeatures += (URLlength(window.location.href))
listOfFeatures += (tinyURL())
listOfFeatures += (symbolInURL(window.location.href))
listOfFeatures += (redirectingURL(window.location.href))
listOfFeatures += (minusInURL(window.location.href))
listOfFeatures += (subDomainInUrl(window.location.href))
listOfFeatures += (favicon(window.location.href))
listOfFeatures += (symbolInURL(window.location.href))
listOfFeatures += (nonStandardPort(window.location.href))
listOfFeatures += (httpsInURL(window.location.href))
listOfFeatures += (internalUrlRequests())
listOfFeatures += (internalUrlRequestsinA())
listOfFeatures += (internalUrlRequestsinMetaScriptsLink())
listOfFeatures += (getIsSFH())
listOfFeatures += (usingIFrame())


chrome.runtime.sendMessage({msg: listOfFeatures}, function(response) {
    console.log("message recived");
  });
