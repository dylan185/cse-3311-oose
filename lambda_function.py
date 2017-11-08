import urllib.request
import os
import datetime
import re
from bs4 import BeautifulSoup

def get_page(the_string):
    # This function gets the correct webpage depending on the string sent
    quote_page = ''
    if the_string == 'sports':
        quote_page = 'http://www.theshorthorn.com/sports/'
    elif the_string == 'life entertainment' or the_string == 'life and entertainment':
        quote_page = 'http://www.theshorthorn.com/life_and_entertainment/'
    elif the_string == 'opinion':
        quote_page = 'http://www.theshorthorn.com/opinion/'
    elif the_string == 'events':
        quote_page = 'http://www.theshorthorn.com/calendar/'
    else:
        quote_page = 'http://www.theshorthorn.com/news/'
    
    return quote_page

def get_weather():
    # Set the strings for welcome message
    welcome = 'Welcome to U.T.A Short horn news! '
    weather_temperature = "The temperature expected on campus today is "
    weather_condition = ", and it is expected to be "
    # Go to page
    page = urllib.request.urlopen('https://www.accuweather.com/en/us/arlington-tx/76010/daily-weather-forecast/331134?day=1')
    soup = BeautifulSoup(page, 'html.parser')
    
    # Get the weather for the day
    current_temperature = soup.find('span', attrs={'class': 'large-temp'})
    current_condition = soup.find('div', attrs={'class': 'cond'})
    
    # Strip to basic text
    temperature = current_temperature.text.strip()
    condition = current_condition.text.strip()
    temperature = " ".join(temperature.split())
    condition = " ".join(condition.split())
    
    weather = welcome + weather_temperature + temperature + weather_condition + condition + "."
    
    #print(weather)
    
    return weather


def num_convert(num):
    if(num == '1st'):
        return 0
    elif num == '2nd':
        return 1
    elif num == '3rd':
        return 2
    elif num == '4th':
        return 4
    elif num == '5th':
        return 5
    elif num == '6th':
        return 6
    else:
        return -1

def get_article(genre):
    temp_string = ''
    contents = []
    now = datetime.datetime.now()
    currentDate = str(now)[:10]
    currentHour = now.hour
    
    # Set webpage to specified
    site_base = 'http://www.theshorthorn.com'
    quote_page = get_page(genre)
    
    if genre == 'events':
        # Parse Event WebPage
        page = urllib.request.urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        
        # Find Top Events from Page
        top_events = soup.find('div', attrs={'id': 'tncms-region-index-full'})
        
        # Get href links to events and store in a list
        links = [a['href'] for a in top_events.find_all('a', href=True) if a.text.strip()]
        
        # Enter loop to build the list of links and pull data & set up the list to put in
        full_links = []
        breaker = 1
        for link in links:
            temp = site_base + link
            if temp[:-9] not in full_links:
                full_links.append(temp)
            else:
                breaker = breaker - 1
            if breaker == 5:
                break
            else:
                breaker = breaker + 1
        
        breaker = 1
        
        # Get rid of the first trash address
        del full_links[0]
        event_list = []
        
        # Enter loop to go to each event and get data
        for link in full_links:
            temp = []
            page = urllib.request.urlopen(link)
            soup = BeautifulSoup(page, 'html.parser')
            event_name = soup.find('h1', attrs={'itemprop': 'name'})
            event_date_time = soup.find('div', attrs={'class': 'event-time'})
            event_location = soup.find('div', attrs={'class': 'event-venue'})
            
            # Get rid of all annoying \n, \t, and excessive spaces
            name = event_name.text.strip()
            date_time = event_date_time.text.strip()
            location = event_location.text.strip()
            name = " ".join(name.split())
            date_time = " ".join(date_time.split())
            location = " ".join(location.split())
            
            temp.append(name)
            temp.append(date_time)
            temp.append(location)
            
            event_list.append(temp)
        
        return event_list
    
    else:
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
        full_links = []
        VALID_TAGS = ['p']
        
        breaker = 1
        # Piece together links
        for link in links:
            temp = site_base + link
            if temp[:-9] not in full_links:
                full_links.append(temp)
            else:
                breaker = breaker - 1
            if breaker == 6:
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
            try:
                p = paragraphs.find_all('p')
            except:
                continue
            
            tempstring = ''
            
            for item in p:
                tempstring = tempstring + ' ' + item.get_text(strip=True)
            
            contents.append(tempstring)
            if breaker == 6:
                break
            else:
                breaker = breaker + 1

# Combine into 2D list
article = [headlines, contents]

# Adds in the command for alexa to pause inbetween article headlines
for j in range(0, len(article[0])):
    if j != 0:
        temp_string = temp_string + '<break time="700ms"/>' + article[0][j]
        else:
            temp_string = temp_string + article[0][j]

# Start checking the content and headlines for blacklisted words
blacklist = [['news-editor.shorthorn@uta.edu', 'news-editor dot shorthorn at U.T.A dot E.D.U'], [' @', ' Author '], ['uta.edu', ' U.T.A dot e.d.u'], ['\xa0', ' '], ['UTA', ' U.T.A '], ['10-20-30', 'ten-twenty-thirty']]
#['\\',' ']
m = 0
    for m in range(0, len(blacklist)):
        temp_string = re.sub(blacklist[m][0], blacklist[m][1], temp_string, flags=re.IGNORECASE)
m = 0
    for m in range(0, len(contents)):
        k = 0
        for k in range(0, len(blacklist)):
            contents[m] = re.sub(blacklist[k][0], blacklist[k][1], contents[m], flags=re.IGNORECASE)

# Set and return the final article
final_article = [temp_string, contents]
return final_article

#sample = get_weather()
#print(get_weather)

#print(get_article('news'))

#This is the lambda function, the event parameter is the Jason request from which we will extract the intents.
def lambda_handler(event, context):
    # This is to check to make sure our app is the only skill that can access this lambda function
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    #Thus is where we return a response in JASON format to the Alexa skill speach output.
    #intentName=event["request"]["intent"]["name"]
    if event["request"]["type"] == 'LaunchRequest':
        #        welcome_message = get_weather()
        welcome_message = 'Welcome to U.T.A Short horn news! '
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
            GT = get_article("news")
            headlines_out = GT[0]
            response_2 =    {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': headlines_out,
                    }
                        }
                    }
            return response_2
        elif intentName == 'ReadGenreHeadlines':
            Genre = event["request"]["intent"]["slots"]["Gen"]["value"]
            GT = get_article(Genre)
            headlines_out = GT[0]
            response_2 =    {
                'version': '1.0',
                    'response': {
                        'outputSpeech': {
                            'type': 'PlainText',
                                'text': headlines_out,
                                }
                                }
                            }
            return response_2
        elif intentName == 'ReadSpecificArticle':
            num = event["request"]["intent"]["slots"]["Num"]["value"]
            GT = get_article('news')
            num = num_convert(num)
            if (num != -1):
                content = GT[1][num]
                response_2 =    {
                'version': '1.0',
                    'response': {
                        'outputSpeech': {
                            'type': 'PlainText',
                                'text': content,
                                }
                                }
                            }
                return response_2
            else:
                response_2 =    {
                'version': '1.0',
                    'response': {
                        'outputSpeech': {
                            'type': 'PlainText',
                                'text': 'Invalid Request',
                                }
                                }
                            }
                return response_2


#returning the response JASON structure
#return response

