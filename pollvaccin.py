# coding: utf-8
from bs4 import BeautifulSoup
import requests
import re


url = "https://www.prullenbakvaccin.nl/"
posturl = "https://www.prullenbakvaccin.nl#location-selector"


def poll_site(location="1000"):
    """poll site for location and return list of locations"""
    client = requests.session()
    r = client.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    token = soup.form.input['value']
    data = {"_token": token, "location": location}

    r = client.post(posturl, data)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def parse_priklocatie(s):
    """
    Locatie #95 (17.99 km)   Heeft geen vaccins
    
    return id, dist (hele km)
    """
    m = re.match(r".*#(\d+).*\((\d+).\d+ km\)", s)
    if m:
        id, dist = map(int, m.groups())
    return id, dist


## voor debuggen zonder de hele tijd de site te pollen
soup = poll_site("gouda")
priklocaties = soup.find_all("div", {"class": "card-body"})

for priklocatie in priklocaties:
    priklocatie = priklocatie.text.replace('\n', ' ')

    if "Heeft geen vaccins" not in priklocatie:
        print(priklocatie)
        id, dist = parse_priklocatie(priklocatie)
        if dist < 5:
            print('Vaccin beschikbaar binnen fietsafstand!!!')
            print(priklocatie)
    
