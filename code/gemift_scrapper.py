from bs4 import BeautifulSoup
import requests

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

my_url = "https://www.houseofindya.com/women-clothing/indo-western-kurtas-tunics/layered/cat"

client = requests.get(my_url)

soup = BeautifulSoup(client.content, features="html.parser")
p_name = soup.findAll("div", {"class":"catgName"})

for i in range(0,len(p_name)):
    p_price = p_name[i].findAll("span")
    if len(p_price) > 0:
        for x in range(0, len(p_price)):
            price = p_price[x].text.strip()
            print ("The price is ", price)
    else:
        print ( p_name[i].find("p").text)

