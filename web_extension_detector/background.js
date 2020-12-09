
(async()=>{
    console.log('2') 
    globalThis.model = await tf.loadLayersModel('https://raw.githubusercontent.com/OriLaish/phishing-detection-ANN-model/main/model.json');
    console.log(model1)
     = model1;

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
    
    cretaePredictions.bind(globalThis)
    cretaePredictions();
    chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
       // alert(model1.predict(message.msg))
       console.log(message.msg)
        salert(globalThis.model.predict(tf.tensor(message.msg, [1, 15])))
        sendResponse({
            type: "NO_DATA"
        });
    });
    })();

