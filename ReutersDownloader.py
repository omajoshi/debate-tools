import requests
from bs4 import BeautifulSoup
import os

def createDir(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Creating Directory ... {dir: <20} ... done")
    except OSError:
        print('DirectoryCreationError: Encountered error creating directory ', dir)

def download(region, start=0, end=75):
    base_url = "https://www.reuters.com"
    createDir(f"Extemp")
    for pg in range(start, end):
        url = base_url+f"/news/archive/{region}?view=page&page={1+pg}&pageSize=10"
        s1 = BeautifulSoup(requests.get(url).text, "html.parser")
        for link in s1.select(".story-content a"):
            topic = link.attrs['href'].split('/')[2]
            title = link.attrs['href'].split('/')[3]
            path = f"{os.getcwd()}\\Extemp\\{topic}\\{title}.html"
            if os.path.isfile(path):
                print(f"{1+pg: <2} - Duplicate {topic: <20} / {title: <20}")
                continue
            else:
                print(f"{1+pg: <2} - Downloading {topic: <20} / {title: <20}")
            s2 = BeautifulSoup(requests.get(base_url+link.attrs['href']).text, 'html.parser')
            try:
                headline = s2.select('.ArticleHeader_headline')[0].text
            except IndexError:
                continue
            date = s2.select('.StandardArticleBody_body')[0].text
            text = s2.select('.ArticleHeader_date')[0].text
            createDir(f"{os.getcwd()}\\Extemp\\{topic}")
            with open(path, "w", encoding='utf-8') as f:
                f.write(f"<h1>{headline}</h1>{text}<br><br>{date}")
                print(f"{1+pg: <2} - Downloading {topic: <20} / {title: <20}")