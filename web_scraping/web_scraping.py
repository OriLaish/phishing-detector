from bs4 import BeautifulSoup
import requests

#just testing with random url
urlToSend = "https://labs.vocareum.com/main/main.php?m=editor&asnid=287309&stepid=287310&hideNavBar=1"
response = requests.get(urlToSend)

soup = BeautifulSoup(response.content, "html.parser")

print(type(soup)) #check if the soup type is beautifulsoup
print(soup.prettify()) #print the html file ,  with all tags.