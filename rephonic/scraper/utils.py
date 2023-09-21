import re
from datetime import datetime
from bs4 import BeautifulSoup


def get_csrf_token(session, podcast_id):
    url = f'https://podcastaddict.com/podcast/{podcast_id}'
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', text=re.compile('var csrf_token'))
    match = re.search( r"var csrf_token = '([a-zA-Z0-9]+)'", script.string) if script else None
    return match.group(1) if match else ''


def fetch_reviews(session, csrf_token, podcast_id):
    url = 'https://podcastaddict.com/class/ajax/get_reviews.php'
    payload = {'csrf_token': csrf_token, 'podcastId': podcast_id, 'showAds': 'false'}
    headers = {
        'authority': 'podcastaddict.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://podcastaddict.com',
        'referer': 'https://podcastaddict.com/podcast/99-invisible/3628410',
        'sec-ch-ua': '"Google Chrome";v="117", " Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = session.post(url, headers=headers, data=payload)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print(BeautifulSoup(response.text, 'html.parser'))
    return BeautifulSoup(response.text, 'html.parser') if response.status_code == 200 else None


def parse_reviews(soup):
    reviews = []
    for cell in soup.find_all('div', class_="cellcontent"):
        username = cell.find('div', class_='caption2').find_all('span')[0].text.strip().split()[-1]
        date_str = cell.find('div', class_='caption2').find_all('span')[1].text.strip()
        date = datetime.strptime(date_str, "%b %d %Y")
        content = cell.find('div', class_="lighttext").text.strip()
        
        reviews.append({
            'author_name': username,
            'created_date': date,
            'text_content': content
        })
    return reviews
