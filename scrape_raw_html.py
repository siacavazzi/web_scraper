from bs4 import Tag
from lib.WebFetch import WebFetch
from lib.content_identifier import ProcessHTML
from lib.GPT_structuring import extract_contents
urls = ["https://dice.fm/browse/new-york","https://www.nyc.com/events/","https://www.nyc.gov/events/events-filter.html", "https://www.eventbrite.com/c/new-york-city-event-calendar-cfxwcyg/", "https://javitscenter.com/events/"]
other = ["https://www.msg.com/calendar?venues=KovZpZA7AAEA", "https://www.facebook.com/search/events/?q=nyc%20events&sde=AbrVxKua3d7Q7RQz7ZWPsa9be21FsYZGGfNj98HZhw7z4Jr8oNcvAkTnImoVykXdacbGlW6lojQ2wh8K7DGAbDnw"]
fetcher = WebFetch(max_pages=10)
elements = fetcher.get_web_content(urls[1], 1)
fetcher.end_session()

#processer = ProcessHTML()
#items = processer.get_items(html)
#processer.reset()

print("========== MOST LIKELY ELEMENT =========")

test = elements.get_most_likely_content()
print(test)
test.write_elements()


#contents = extract_contents(test)
#print(contents)






