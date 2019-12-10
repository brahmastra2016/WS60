import re
from gazpacho import get, Soup

URL = "https://www.goodreads.com/quotes/search"

query = 'The Reluctant Fundamentalist Mohsin Hamid'
page = 1

params = {"q": query, "commit": "Search", "page": page}
html = get(URL, params)
soup = Soup(html)

quotes = soup.find("div", {"class": "quoteText"})

quote_text = quotes[0]
quote_text.find("a", {"class": "authorOrTitle"}).text
quote_text.find("span", {"class": "authorOrTitle"}).text.replace(",", "")
re.search("(?<=“)(.*?)(?=”)", quote_text.text).group(0)

def parse_quote(quote_text):
    try:
        book = quote_text.find("a", {"class": "authorOrTitle"}).text
    except AttributeError:
        book = None
    author = quote_text.find("span", {"class": "authorOrTitle"}).text.replace(",", "")
    quote = re.search("(?<=“)(.*?)(?=”)", quote_text.text).group(0)
    return {"author": author, "book": book, "quote": quote}

def get_page_quotes(soup):
    quotes = []
    for quote_text in soup.find("div", {"class": "quoteText"}):
        try:
            quote = parse_quote(quote_text)
            quotes.append(quote)
        except:
            pass
    return quotes

get_page_quotes(soup)
