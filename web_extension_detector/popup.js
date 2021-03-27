PhishingElement = document.getElementById("PhishingButton");
LegitimateElement = document.getElementById("LegitimateButton");

PhishingElement.addEventListener("click", PhishingSites);  
LegitimateElement.addEventListener("click", LegitimateSites);
   


function PhishingSites() {
  
  chrome.cookies.get({ url: 'http://127.0.0.1:8000', name: 'PhishingDetectorCookie' },
  function (cookie) {
    if (cookie) { //cookie exist
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: cookie.value}, function(response) {
        
      });
    }
    else { // need to create the cookie
      
      var HTTPRequest = new XMLHttpRequest();
      var ServerURL = "http://127.0.0.1:8000/get_uid"

      HTTPRequest.onreadystatechange = function() {//Call a function when the state changes.
        if(HTTPRequest.readyState == 4 && HTTPRequest.status == 200) {
          
            var returnJson = JSON.parse(HTTPRequest.responseText); //get the uid from the server 
            chrome.cookies.set({ url: "http://127.0.0.1:8000", name: "PhishingDetectorCookie", value: returnJson.uid}); // create the cookie
          chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: returnJson.uid}, function(response) {
            
          });
          } 
        }
      
      HTTPRequest.open('GET', ServerURL, true);
      HTTPRequest.send( null )
    }  
});
}



function LegitimateSites() {
  
  chrome.cookies.get({ url: 'http://127.0.0.1:8000', name: 'PhishingDetectorCookie' },
  function (cookie) {
    if (cookie) { //cookie exist 
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: cookie.value}, function(response) {
        
      });
    }
    else { // need to create the cookie
      var HTTPRequest = new XMLHttpRequest();
      var ServerURL = "http://127.0.0.1:8000/get_uid"
      HTTPRequest.onreadystatechange = function() {//Call a function when the state changes.
        if(HTTPRequest.readyState == 4 && HTTPRequest.status == 200) {
            var returnJson = JSON.parse(HTTPRequest.responseText); //get the uid from the server 
            chrome.cookies.set({ url: "http://127.0.0.1:8000", name: "PhishingDetectorCookie", value: returnJson.uid}); // create the cookie
            chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: returnJson.uid}, function(response) {
              
            });
          } 
        }
  
      HTTPRequest.open('GET', ServerURL, true);
      HTTPRequest.send( null )
    }   
  });

}
