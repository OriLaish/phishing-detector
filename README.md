# Phishing Detector

The project consists of two main parts. A web extension that identifies phishing sites using a machine learning model and alerts such sites to the user and server that maintains the system that retrains the model and improves it through feedback that the web extension returns from users and an external API, updates the web extension with the new model.

## Getting Started

Follow these instructions and you will get you a copy of the project up and running.

### Prerequisites


```
* The hardware requirements required is a computer connected to the Internet.
* Download VS Code
```

### Installing

Follow the steps to install and save the project.

```
Step 1: Download Phishing Detector folder from the master branch.
Step 2: Extract the folder and save it in your computer.
```

Steps to set the Extension:

```
Step 1: Click this [link](chrome://extensions/)
Step 2: Press load unpacked and select the Phishing Detector/web_extension_detector folder
Step 3: At top left, click the extensions icon
Step 4: Click  the thumbtack

now you should have a new green icon at top left, if you do it worked.
if not, repeat the steps.
```

Steps to run the Server:
```
Step 1: Open The Phishing Detector/Server_Creation on VS code
Step 2: Open The terminal on server_creation/Phishing_Detector folder
Step 3: Enter this command : "python manage.py runserver"
```


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - The server's framework
* [Chrome Developers](https://developer.chrome.com/) - Web extension developer API
* [TensorFlow](https://www.tensorflow.org/) - Used to create and train the model


## Authors

* **Ori Laish**
* **Yahel Argas**


## Acknowledgments

* To our guide and mentor, whom helped us through the whole project.

