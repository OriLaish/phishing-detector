PhishingElement = document.getElementById("PhishingButton");
LegitimateElement = document.getElementById("LegitimateButton");

PhishingElement.addEventListener("click", PhishingSites);  
LegitimateElement.addEventListener("click", LegitimateSites);
   


function PhishingSites() {
  
  chrome.cookies.get({ url: 'http://127.0.0.1:8000', name: 'PhishingDetectorCookie' },
  function (cookie) {
    if (cookie) { //cookie exist 
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: cookie.value}, function(response) {
        console.log(response);
      });
    }
    else { // need to create the cookie
      

      //need to get the id from the server !
      chrome.cookies.set({ url: "http://127.0.0.1:8000", name: "PhishingDetectorCookie", value: "44444"}); // create the cookie
      console.log("phishing");
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js"}, function(response) {
        console.log(response);
      });
    }
});


  
    

}



function LegitimateSites() {
  chrome.cookies.get({ url: 'http://127.0.0.1:8000', name: 'PhishingDetectorCookie' },
  function (cookie) {
    if (cookie) { //cookie exist 
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js" , cookieValue: cookie.value}, function(response) {
        console.log(response);
      });
    }
    else { // need to create the cookie
      

      //need to get the id from the server !
      chrome.cookies.set({ url: "http://127.0.0.1:8000", name: "PhishingDetectorCookie", value: "44444"}); // create the cookie
      console.log("phishing");
      chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js", cookieValue: "44444"}, function(response) {
        console.log(response);
      });
    }
});
    

}