from gazpacho import get, Soup

# HTML start

with open('data/bad.html', 'r') as f:
    html = f.read()

soup = Soup(html)
soup.find('p')
soup.find('p', {'id': 'bar'})
soup.find('p', {'id': 'bar'}).text

soup.find('div')
soup.find('div', mode='first')

soup.find('div', {'class': 'foo'}).text
soup.find('b').text

soup.find('div', {'class': 'foo'}).remove_tags()

# get start

# 1xx Informational

# 2xx Sucess
200 - OK

# 3xx Redirection

# 4xx Client Error (YOUR FAULT)

400 - Bad Request
401 - Unauthorized
403 - Forbidden
404 - Not Found
418 - 🍵
429 - Too many requests

# 5xx Server Error (THEIR FAULT)

500 - Internal Server Error
501 - Not Implemented
502 - Bad Gateway
503 - Service Unavailable
504 - Gateway Timeout

# Examples

get('https://httpstat.us/403')
get('https://httpstat.us/404')
get('https://httpstat.us/418')

get('https://httpstat.us/503')
get('https://httpstat.us/500')

get('https://httpstat.us/200')

# structuring a request

url = 'https://httpbin.org/anything?year=2020&colour=black'

print(get(url))

url = 'https://httpbin.org/anything'

r = get(url, params={'year': 2020, 'colour': 'black'}, headers={'User-Agent': 'gazpacho'})

print(r)
