from bs4 import BeautifulSoup as bs4
import requests
import re
import pandas as pd

# Pretend like we're human
# https://stackoverflow.com/a/43441551
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url = "https://www.ign.com/articles/2005/04/06/xenosaga-episode-ii-jenseits-von-gut-und-bose-enemy-faq-545281"

response = requests.get(url, headers=headers)
soup = bs4(response.content, "html.parser")


# Find the div/class with the text we want
text = soup.find('section', {'class': 'article-page'})

# For names, match all instances of text after 2-3 digits followed by a whitespace, |, and another whitespace but before <br/>
names_dirty = re.findall("\d{2,3}\s\|\s(.*?)<br/>", str(text))
# We need to remove all the elements after the last enemy
index_cutoff = names_dirty.index("Mikumari") + 1
# Slice the list to remove the extra elements
names = names_dirty[:index_cutoff]
# Now we should have 109 elements in the names list, which matches up with 75 enemies + 34 bosses = 109 enemies total. Nice!