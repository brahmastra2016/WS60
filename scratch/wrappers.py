from quote import quote #pip install quote

quote('shakespeare', limit=1)

# !quote shakespeare

# !pip install urbandict
#https://github.com/novel/py-urbandict
import urbandict

urbandict.define('Thirst Trap')

# https://github.com/martin-majlis/Wikipedia-API/
# !pip install wikipedia-api

from wikipediaapi import Wikipedia
wiki = Wikipedia('en')

page = wiki.page('Python_(programming_language)')
page.exists()
page.text


#
