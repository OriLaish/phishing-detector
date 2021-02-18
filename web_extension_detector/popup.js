PhishingElement = document.getElementById("PhishingButton");
LegitimateElement = document.getElementById("LegitimateButton");

PhishingElement.addEventListener("click", PhishingSites);  
LegitimateElement.addEventListener("click", LegitimateSites);
   


function PhishingSites() {
    console.log("phishing");
    chrome.runtime.sendMessage({Is_Phishing: false , sender: "popup.js"}, function(response) {
        console.log(response);
      });
    

}



function LegitimateSites() {
    console.log("Legitimate");
    chrome.runtime.sendMessage({Is_Phishing: true , sender: "popup.js"}, function(response) {
        console.log(response);
      });
    

}