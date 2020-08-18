import requests
from bs4 import BeautifulSoup

def soup(link):
    return BeautifulSoup(requests.get(link).text, 'html.parser')

def print_results():
    page_soup = soup(f"https://www.joyoftournaments.com{soup(input('Which tournament? ')).find('iframe')['src']}")

    for event in page_soup.find_all(lambda s: "Prelims" in s.text and "Prelim Standings" in s.text):
        event_soup = soup(f"{base_url}{event['href']}")
        teams = event_soup.find_all(lambda p: "Winston Churchill HS" in p.text and p.name == "tr")
        if teams:
            print(event_soup.select('div.title')[0].text[:-17])
        for team in teams:
            print(team.find_all('td')[1].text, team.find_all('td')[0].text[:-20])


print_results()