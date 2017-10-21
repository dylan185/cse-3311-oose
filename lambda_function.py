import urllib.request
import datetime
from bs4 import BeautifulSoup
#This is the connection to our content database AWS Relational database service
#try:
#    conn = pymysql.connect(host='utaechonews.coflj2xb1eul.us-east-1.rds.amazonaws.com', port=3306, user='kash_if47', passwd='HelloEcho2017', db='NewsDb')
#except:
#    print ("Error")
#
#cur = conn.cursor()


articleDate = '2017-10-21'
now = datetime.datetime.now()
currentDate = str(now)[:10]
currentHour = now.hour

if (articleDate != currentDate) and (currentHour > 9):
    print('Fetch articles from URL')

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

    breaker = 1
    # Piece together links
    for link in links:
        temp = site_base + link
        if temp[:-9] not in full_links:
            full_links.append(temp)
        #print(temp)
        else:
            breaker = breaker - 1
        if breaker == 10:
            break
        else:
            breaker = breaker + 1

    breaker = 1

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
        if breaker == 10:
            break
        else:
            breaker = breaker + 1

    # Combine into 2D list
    article = [headlines, contents]

    temp_string = ''
    for j in range(0, len(article[0])):
        if j != 0:
            temp_string = temp_string + ' . . ' + article[0][j]
        else:
            temp_string = temp_string + article[0][j]

#This is the lambda function, the event parameter is the Jason request from which we will extract the intents.
def lambda_handler(event, context):
    # This is to check to make sure our app is the only skill that can access this lambda function
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    #Thus is where we return a response in JASON format to the Alexa skill speach output.
    #intentName=event["request"]["intent"]["name"]
    if event["request"]["type"] == 'LaunchRequest':
        welcome_message = 'Welcome to U.T.A Short horn news!'
        response_1 = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': welcome_message,
            }
        }
        }
        return response_1
    elif event["request"]["type"] == 'IntentRequest':
        intentName=event["request"]["intent"]["name"]
        if intentName == 'ReadHeadlinesIntent':
            response_2 =    {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': temp_string,
                    }
                        }
                        }
            return response_2

#returning the response JASON structure
#return response