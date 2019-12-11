import re
from gazpacho import get, Soup
import pandas as pd

url = 'https://www.capfriendly.com/'
html = get(url)

soup = Soup(html)
table = soup.find('table', {'id': 'ich'})
trs = table.find('tr', {'class': 'tmx'})
tr = trs[0]

tr.find('a', mode='first').text
tr.find('td', {'data-label': 'PROJECTED CAP HIT'}, strict=True).text

def parse_tr(tr):
    team = tr.find('a', mode='first').text
    cap = tr.find('td', {'data-label': 'PROJECTED CAP HIT'}, strict=True).text
    cap = float(cap.replace(',', '').replace('$', ''))
    return team, cap

cap_hits = [parse_tr(tr) for tr in trs]

url = 'https://www.hockey-reference.com/friv/playoff_prob.fcgi'
html = get(url)

soup = Soup(html)

east = pd.read_html(str(soup.find('table')[0]))[0]
west = pd.read_html(str(soup.find('table')[1]))[0]
df = pd.concat([east, west])[['Team', 'W']].reset_index(drop=True)
df['W'] = df['W'].apply(pd.to_numeric, errors='coerce')
wins = df.dropna()

cap_hits = pd.DataFrame(cap_hits, columns=['Team', 'spend'])

df = pd.merge(wins, cap_hits, on='Team', how='left')
df['mpw'] = round(df['spend'] / df['W'] / 1_000_000, 2)
df.sort_values('mpw', ascending=True)

#
