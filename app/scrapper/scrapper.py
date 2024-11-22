import requests
from bs4 import BeautifulSoup, Tag

from config import settings

# URLs
login_url = "https://rutracker.org/forum/login.php"
query = "Винни пух"
search_url = "https://rutracker.org/forum/tracker.php?nm={search_query}".format(
    search_query=query
)
topic_url = "https://rutracker.org/forum/{topic_id}"

# Your login credentials
credentials = {
    "login_username": settings.RUTRACKER.LOGIN,
    "login_password": settings.RUTRACKER.PASSWORD,
    "login": "Вход",  # The value for the login button (Russian for "Login")
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
# Create a session to manage cookies
session = requests.Session()

# Log in
response = session.post(login_url, data=credentials)
if response.status_code != 200:
    print("Login failed")
else:
    print("Login successful")

# Access the target page
response = session.get(search_url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    # Example of extracting data (e.g., torrent titles)
    torrents = soup.find_all(
        "a", attrs={"data-topic_id": True}
    )  # Adjust the class name based on the actual HTML
    for torrent in torrents:
        print(torrent.text.strip())
    torrent_topic_url = "https://rutracker.org/forum/{topic_href}".format(
        topic_href=torrents[0].get("href")
    )
    res = session.get(torrent_topic_url, headers=headers)
    if res.status_code == 200:
        soup_1 = BeautifulSoup(res.content, "html.parser")
        magnet_link_tag = soup_1.find("a", class_="magnet-link")
        if isinstance(magnet_link_tag, Tag):
            magnet_link = magnet_link_tag.get("href")
        ...
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
