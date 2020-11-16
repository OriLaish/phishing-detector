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

chrome.webRequest.onBeforeRequest.addListener(
    function(details) { return {cancel: true}; },
    {urls: ["*://*.youtube.com/*"]},
    ["blocking"]
    );