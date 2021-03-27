
(async()=>{ 
    globalThis.model = await tf.loadLayersModel('https://raw.githubusercontent.com/OriLaish/phishing-detection-ANN-model/main/model.json');


const PhishingPradiction = 0.99

    chrome.runtime.onMessage.addListener(function ( message, sender , sendResponse)  {
        if (message.sender == "feature_extractor.js"){
        globalThis.features = message.features //save the features
        var pradiction = globalThis.model.predict(tf.tensor(message.features, [1, 15])).dataSync()
            if(pradiction < PhishingPradiction){ //Phishing
                chrome.browserAction.setIcon( {path : "IconPhishingSites.PNG"} //change the favicon to the phishing one
                );

            }
        
            else{ //Legitimate
                chrome.browserAction.setIcon( {path : "IconLegitimateSites.png"}); //change the favicon to the legitimate one

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
                var CookieId = message.cookieValue
                var ServerURL = "http://127.0.0.1:8000/submit_url"
                // send it to the server
                var HTTPRequest = new XMLHttpRequest();
                var params = 'is_phishing='+ Is_PhishingToSend + '&url=' + url  + '&features=' + featuresToSend + "&uid=" + CookieId;
                HTTPRequest.open('POST', ServerURL, true);

                //Send the proper header information along with the request
                HTTPRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

                HTTPRequest.onreadystatechange = function() {//Call a function when the state changes.
                if(HTTPRequest.readyState == 4 && HTTPRequest.status == 200) {}
                }
                HTTPRequest.send(params);
                alert("Thank you for your feedback!")


              });
            
            sendResponse({
                type: "NO_DATA"});
    
        }
    });
    })();

