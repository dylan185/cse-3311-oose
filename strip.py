import urllib.request
from bs4 import BeautifulSoup

# Get WebPage
site_base = 'http://www.theshorthorn.com'
quote_page = 'http://www.theshorthorn.com/news/campus/'

# Parse WebPage
page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

# Find Top Articles from Page
top_articles = soup.find('div', attrs={'id': 'tncms-region-index-primary'})

# Get href links to articles and store in a list
links = [a['href'] for a in top_articles.find_all('a', href=True) if a.text.strip()]

# Deletes the comment links for each article (every odd position)
del links[1::2]

# Declare whitelist, i &lists
i = 0
headlines = []
contents = []
full_links = []
VALID_TAGS = ['p']

# Piece together links
for link in links:
    temp = site_base + link
    full_links.append(temp)

# Goes to each link and gets headline and content
for link in full_links:
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    headline = soup.find('h1', attrs={'class': 'headline'})
    headlines.append(headline.text.strip())

    paragraphs = soup.find('div', attrs={'class': 'asset-content subscriber-premium'})
    p = paragraphs.find_all('p')
    tempstring = ''

    for item in p:
        tempstring = tempstring + ' ' + item.get_text(strip=True)

    contents.append(tempstring)

# Combine into 2D list
article = [headlines, contents]
print(article)