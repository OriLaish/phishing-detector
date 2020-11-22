const Phishing = -1
const Legitimate = 1
const Suspicious = 0

//1.1.1
function IPInAdress(url){
    checkForIP = RegExp('^http[s]?:\/\/((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])');
    if(checkForIP.test(url))
        return Phishing
    
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
function TinyURL(url)
{

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
function favicon(url , tab){
    const urlObj = new URL(url)
    const faviconurl = new URL(tab.favIconUrl)
    if(urlObj.hostname == faviconurl.hostname)
        return Legitimate
    
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



//try to get html file
let htmlcontent = document.getElementsByTagName("*"); //get all elemnts .
for(i=0; i<htmlcontent.length; i++){
    console.log(htmlcontent[i])

}