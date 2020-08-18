import requests
import re
from bs4 import BeautifulSoup

def soup(link):
    return BeautifulSoup(requests.get(link).text, 'html.parser')

def joy_print_results(base_url=''):
    while not base_url:
        base_url = input("Which tournament? ")
    if base_url[-1] != "/":
        base_url += "/"
    page_soup = soup(base_url)

    for event in page_soup.find_all(lambda s: s.text=="Prelim Standings"):
        event_soup = soup(f"{base_url}{event['href']}")
        teams = event_soup.find_all(lambda p: p.name == "tr" and "Winston Churchill HS" in p.text)
        if teams:
            print(event_soup.select('div.title')[0].text[:-17])
        for team in teams:
            print(team.find_all('td')[1].text, team.find_all('td')[0].text[:-20])


# TO GET ALL JOY TOURNAMENTS
# page_soup = soup('https://www.joyoftournaments.com/bystate.asp?state=TX&mon=-99&go=Filter+Now')
# for x in page_soup.select("#tlist td [target=_new]"):
#     joy_print_results(x['href'])


# page_soup1 = soup('https://www.tabroom.com/index/index.mhtml')
# tournaments1 = page_soup1.find('table').find_all(lambda p: p.name=="a" and "tourn_id" in p["href"])
# page_soup2 = soup('https://www.tabroom.com/index/results/')
# tournaments2 = page_soup2.find('table').find_all(lambda p: p.name=="a" and "tourn_id" in p["href"])
# tournaments = [*tournaments1, *tournaments2]
# for tournament in tournaments:
#     tourn_id = tournament['href'][27:]
#     events_link = f"https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}"
#     events_soup = soup(events_link)
#     for event in events_soup.select('.menu a.dkblue.full, .menu a.blue.full'):
#         event_id = event['href'][49:]
#         event_name = event.text.strip()
#         prelims_url = f"https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id={event_id}&tourn_id={tourn_id}"
#         prelims_soup = soup(prelims_url)
#         teams = prelims_soup.find_all(lambda p: "Winston Churchill " in p.text and p.name=="tr")
#         if teams:
#             print(event_name)
#         for team in teams:
#             print(f"{team.find_all('td')[0].text.strip()} wins for {team.find_all('td')[1].text.strip()}")
#             


def tabroom_print_results(tourn_id):
    events_soup = soup(f"https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id={tourn_id}")
    for event in events_soup.select('.menu a.dkblue.full, .menu a.blue.full'):
        event_name = event.text.strip()
        re_search = re.search('event_id=(?P<event_id>[0-9]+)', event['href'])
        if re_search:
            event_id = re_search.group('event_id')
        else:
            print("Something went wrong...")
            return
        prelims_soup = soup(f"https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id={event_id}&tourn_id={tourn_id}")
        teams = prelims_soup.find_all(lambda p: "Winston Churchill " in p.text and p.name=="tr")
        if teams:
            print(event_name)
            for team in teams:
                print(f"{team.find_all('td')[0].text.strip()} wins for {team.find_all('td')[1].text.strip()}")

def print_results(base_url=''):
    while "tabroom" not in base_url and "joyoftournaments" not in base_url:
        base_url = input("Which tournament? ")
    if "tabroom" in base_url:
        re_search = re.search('tourn_id=(?P<tourn_id>[0-9]+)', base_url)
        if re_search:
            tourn_id = re_search.group('tourn_id')
            tabroom_print_results(tourn_id)
        else:
            print("Something went wrong...")
            return
    if "joyoftournaments" in base_url:
        if base_url[-1] != "/":
            base_url += "/"
        joy_print_results(base_url)