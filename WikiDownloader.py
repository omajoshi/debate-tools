import requests
from bs4 import BeautifulSoup
import os

cwd = os.getcwd()

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

base = "https://hsld.debatecoaches.org"
soup = BeautifulSoup(requests.get(base).text, 'html.parser')

teams = soup.select('.PanelsSchools .wikilink')

grid = [(team.text,team.find('a').attrs['href']) for team in teams]

for team in grid:
    t = requests.get(base+team[1]).text
    soup = BeautifulSoup(t, 'html.parser')
    p = soup.select(".grid.sortable.doOddEven tr")
    if (len(p) > 1):
        print(team[1][1:])
        createFolder(team[1][1:])
        with open(f"{team[1][1:]}/index.html", "w", encoding='utf-8') as item:
            item.write(t.replace("display:none", "").replace('href="/', f'href="{cwd}/'))
        for d in p[1:]:
            (a, n) = d.find_all(class_="wikilink")
            print(a.text, n.text)
            createFolder(f"{team[1][1:]}/{a.text}")
            aff = requests.get(base+a.find('a').attrs['href']).text
            with open(f"{team[1][1:]}/{a.text}/index.html", "w", encoding='utf-8') as item:
                item.write(aff.replace("display:none", "").replace('href="/', f'href="{cwd}/'))
            createFolder(f"{team[1][1:]}/{n.text}")
            neg = requests.get(base+n.find('a').attrs['href']).text
            with open(f"{team[1][1:]}/{n.text}/index.html", "w", encoding='utf-8') as item:
                item.write(neg.replace("display:none", "").replace('href="/', f'href="{cwd}/'))
    else:
        grid.remove(team)
