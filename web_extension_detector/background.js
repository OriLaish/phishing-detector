
(async()=>{ 
    globalThis.model = await tf.loadLayersModel('https://raw.githubusercontent.com/OriLaish/phishing-detection-ANN-model/main/model.json');

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
    
    chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
       // alert(model1.predict(message.msg))
       console.log(message.msg)
        alert(globalThis.model.predict(tf.tensor(message.msg, [1, 15])))
        sendResponse({
            type: "NO_DATA"
        });
    });
    })();

