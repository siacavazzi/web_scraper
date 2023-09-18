from bs4 import Tag
from HTML_fetch import WebFetch
from process_HTML import ProcessHTML
urls = ["https://dice.fm/browse/new-york","https://www.nyc.com/events/","https://www.nyc.gov/events/events-filter.html", "https://www.eventbrite.com/c/new-york-city-event-calendar-cfxwcyg/", "https://javitscenter.com/events/"]
other = ["https://www.msg.com/calendar?venues=KovZpZA7AAEA", "https://www.facebook.com/search/events/?q=nyc%20events&sde=AbrVxKua3d7Q7RQz7ZWPsa9be21FsYZGGfNj98HZhw7z4Jr8oNcvAkTnImoVykXdacbGlW6lojQ2wh8K7DGAbDnw"]
fetcher = WebFetch()
elements = fetcher.get_web_content(other[1])
fetcher.end_session()

#processer = ProcessHTML()
#items = processer.get_items(html)
#processer.reset()
elements.print()
print("========== MOST LIKELY ELEMENT =========")

test = elements.get_most_likely_content()
print(test.content[1])





