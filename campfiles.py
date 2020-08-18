import requests
from bs4 import BeautifulSoup
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

base_url = 'https://openev.debatecoaches.org'
base_page = requests.get(base_url)

soup = BeautifulSoup(base_page.text, 'html.parser')

panel = soup.select('div.panel.expanded.PanelsFilesByType.FilesByType span.wikilink')

createFolder("Camp Files")
# files = []

for row in panel:
    folder_url = base_url + row.find('a')['href']
    folder_page = requests.get(folder_url)
    folder_soup = BeautifulSoup(folder_page.text, 'html.parser')
    f = folder_soup.select('span.wikiexternallink a')
    if f:
        createFolder(f"Camp Files/{row.text}")
        for file in f:
            filename = file['href'].split('/')[-1]
            print(f'Downloading ... {row.text: <14} - {filename} ... ')
            doc = requests.get(file['href'])
            with open(f"Camp Files/{row.text}/{filename}", "wb") as item:
                item.write(doc.content)

            '''
            if filename not in files:
                files.append(filename)
                print(f'Downloading ... {row.text: <14} - {filename} ... ')
                doc = requests.get(file['href'])
                with open(f"Camp Files/{row.text}/{filename}", "wb") as item:
                    item.write(doc.content)
            '''