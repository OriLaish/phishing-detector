const Phishing = -1
const Legitimate = 1
const Suspicious = 0

function IPInAdress(url){
    checkForIP = RegExp('^http[s]?:\/\/((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])');
    if(checkForIP.test(url))
        return Phishing
    
    else
        return Legitimate
}


function URLlength(url){
    if(url.length < 54 )
        return Legitimate

    else if(url.length >= 54 && url.length <= 75)
        return Suspicious

    else
        return Phishing
}

function TinyURL(url){

}

//symbol = "@"
function symbolInURL(url) {
    if(url.indexOf("@") != -1 ) //if it not equals to -1 it means there is a @ in the url
        return Phishing

    else
        return Legitimate

}

//this function check for the index of the "//" in the url
function redirectingURL(url) {
    if(url.indexOf("//") > 7)
        return Phishing
    
    else
        return Legitimate

}

function minusInURL(url){
    if(url.indexOf("-") != -1 ) //if it not equals to -1 it means there is a - in the url
        return Phishing

    else
        return Legitimate

}

function subDomainInUrl(url){
    let count = url.split('.').length - 2
    if (count == 0)
        return Legitimate
    else if (count == 1) 
        return Suspicious
    return Phishing
}

