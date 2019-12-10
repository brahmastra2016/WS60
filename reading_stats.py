import re
from gazpacho import get, Soup
import pandas as pd
from tqdm import tqdm
import time
import altair as alt

url = 'https://www.goodreads.com/review/list/16626766'
params = {
    'shelf': 'read',
    'order': 'd',
    'sort': 'date_read',
    'per_page': 30, # actually can't change
    'page': 1
}

html = get(url, params)
soup = Soup(html)
trs = soup.find('tr', {'class': 'bookalike review'})
tr = trs[0]

tr.find('a', {'href': '/book/show/'})[1].attrs['title']
tr.find('a', {'href': '/author/show'}).text
tr.find('span', {'class': 'date_started_value'}).text
tr.find('span', {'class': 'date_read_value'}).text
tr.find('nobr').remove_tags()

def parse_tr(tr):
    return {
        'title': tr.find('a', {'href': '/book/show/'})[1].attrs['title'],
        'author': tr.find('a', {'href': '/author/show'}).text,
        'end': tr.find('span', {'class': 'date_read_value'}).text,
    }

books = [parse_tr(tr) for tr in trs]

# scrape page

def scrape_page(user=16626766, page=1):
    url = f'https://www.goodreads.com/review/list/{user}'
    params = {
        'shelf': 'read',
        'order': 'd',
        'sort': 'date_read',
        'page': page
    }
    html = get(url, params)
    soup = Soup(html)
    trs = soup.find('tr', {'class': 'bookalike review'})
    books = [parse_tr(tr) for tr in trs]
    return books

books = []
pages = 5 * 52 // 30 + 1
for page in tqdm(range(1, pages+1)):
    books.extend(scrape_page(page=page))
    time.sleep(1)

df = pd.DataFrame(books)
df['end'] = pd.to_datetime(df['end'])
df = df.sort_values('end', ascending=True)
df['year'] = df['end'].dt.year
df['week'] = df['end'].dt.dayofyear // 7 + 1
df['read'] = 1

stats = df.groupby(['year', 'week'])['read'].count().groupby(['year']).cumsum()
df = stats.reset_index()

nearest = alt.selection(
    type='single',
    nearest=True,
    on='mouseover',
    fields=['week'],
    empty='none'
)

line = (
    alt.Chart(df)
    .mark_line(interpolate='basis')
    .encode(
        x='week',
        y='read',
        color='year:O'
    )
)

selectors = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x='week',
        opacity=alt.value(0)
    )
    .add_selection(nearest)
)

points = (
    line
    .mark_point()
    .encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
)

text = (
    line
    .mark_text(align='left', dx=5, dy=-5)
    .encode(
        text=alt.condition(nearest, 'read', alt.value(' '))
    )
)

rules = (
    alt.Chart(df)
    .mark_rule(color='red')
    .encode(x='week')
    .transform_filter(nearest)
)

chart = (
    alt.layer(line, selectors, points, rules, text)
    .properties(
        width=700,
        height=400,
        background='white',
        title='goodreads Challenge'
    )
)

chart
