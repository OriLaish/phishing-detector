
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

const PhishingPradiction = 0.99

    chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
       // alert(model1.predict(message.msg))
        if (message.sender == "feature_extractor.js"){
        console.log(message.features)
        globalThis.features = message.features //save the features
        var pradiction = globalThis.model.predict(tf.tensor(message.features, [1, 15])).dataSync()

            if(pradiction < PhishingPradiction){ //Phishing
                chrome.browserAction.setIcon( {path : "IconPhishingSites.PNG"}
                
                );

            }
        
            else{ //Legitimate
                chrome.browserAction.setIcon( {path : "IconLegitimateSites.png"});

            }
        

            sendResponse({
                type: "NO_DATA"
                    });

        
                }
        
        else if(message.sender == "popup.js")
        {
            chrome.tabs.query({
                active: true,
                currentWindow: true
              }, function(tabs) {
                // get all the needed information about the current site.
                var tab = tabs[0];
                var url = tab.url;
                var featuresToSend = globalThis.features
                var Is_PhishingToSend = message.Is_Phishing
                var ServerURL = "127.0.0.1:8000/submit_url"
                // send it to the server
                var HTTPRequest = new XMLHttpRequest();
                var params = 'Is_Phishing='+ Is_PhishingToSend + '&url=' + url  + '&features=' + featuresToSend;
                HTTPRequest.open('POST', url, true);

                //Send the proper header information along with the request
                HTTPRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

                HTTPRequest.onreadystatechange = function() {//Call a function when the state changes.
                if(HTTPRequest.readyState == 4 && HTTPRequest.status == 200) {
                    alert(HTTPRequest.responseText);
                    }
                }
                HTTPRequest.send(params);
                alert("sended")


              });
            
            sendResponse({
                type: "NO_DATA"});
    
        }


    });
    })();

