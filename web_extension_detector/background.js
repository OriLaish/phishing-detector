import * as tf from '@tensorflow/tfjs'; 

let contextMenus = {};

contextMenus.userMenu = chrome.contextMenus.create(

    { "title": "userMenu" },
    function()
    {
        if(chrome.runtime.lastError)
        {
            console.error(chrome.runtime.lastError.message)
        }
    }
);
console.log("in background");
/*chrome.webNavigation.onBeforeNavigate.addListener(
    function(details)
    {
        if(details.url.indexOf("ynet.co.il") >= 0 )
        {
            alert("you entered YNETTT"); 
        }
    }


)*/

/*chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if(tab.active)
        alert(tab.url + "1");
 });*/ 
 

/*chrome.webRequest.onBeforeRequest.addListener(
    function(details) { return {cancel: true}; },
    {urls: ["*://*.youtube.com/*"]},
    ["blocking"]
    ); */