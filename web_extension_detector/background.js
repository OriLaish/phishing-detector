

//let newModel = tf.sequential();
debugger
 console.log('1');
(async()=>{
    console.log('2')
    //debugger  
    const model1 = await tf.loadLayersModel('https://raw.githubusercontent.com/OriLaish/phishing-detection-ANN-model/main/model.json');
    console.log(model1)
    //const p = model1.predict([1, -1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 0, 0, 0, 1, 1]);
    //console.log(p)
    globalThis.x = 12;
    globalThis.model = model1;

    /*let contextMenus = {};
    contextMenus.userMenu = chrome.contextMenus.create(
    { "title": "userMenu" },
    function()
    {
        if(chrome.runtime.lastError)
        {
            console.error(chrome.runtime.lastError.message)
        }
    });*/

    const cretaePredictions = () =>{
        //debugger
        console.log(globalThis.x);
    };
    
    cretaePredictions.bind(globalThis)
    cretaePredictions();
    chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
       // alert(model1.predict(message.msg))
       console.log(message.msg)
        alert(globalThis.model.predict(tf.tensor(message.msg, [1, 15])))
        sendResponse({
            type: "NO_DATA"
        });
    });
    })();

//this.x = 12;
/*function cretaePredictions(){
    debugger
    console.log(this.x);
}

cretaePredictions.bind(this)
cretaePredictions();
chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
   // alert(model1.predict(message.msg))
    alert(message.msg)
    sendResponse({
        type: "NO_DATA"
    });
});
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
    );*/