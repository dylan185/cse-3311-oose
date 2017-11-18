import urllib.request
import os
import datetime
import re
import json
from bs4 import BeautifulSoup

now = datetime.datetime.now()
currentDate = str(now)[:10]
currentHour = now.hour

def get_page(the_string):
    # This function gets the correct webpage depending on the string sent
    quote_page = ''
    if the_string == 'sports':
        quote_page = 'http://www.theshorthorn.com/sports/'
    elif the_string == 'life entertainment' or the_string == 'life and entertainment':
        quote_page = 'http://www.theshorthorn.com/life_and_entertainment/'
    elif the_string == 'opinion':
        quote_page = 'http://www.theshorthorn.com/opinion/'
    else:
        quote_page = 'http://www.theshorthorn.com/news/'
    
    return quote_page

def get_weather():
    # Set the strings for welcome message
    welcome = 'Welcome to U.T.A Short horn news! '
    weather_temperature = "Today, on campus it is "
    weather_condition = " degrees, and it is expected to be "
    url = "http://api.wunderground.com/api/57d9e55c1fccce10/conditions/q/TX/Arlington.json"

    request = urllib.request.Request(url)
    response = json.load(urllib.request.urlopen(request))
    
    temperature = str(int(response["current_observation"]["temp_f"]))
    condition = response["current_observation"]["weather"]
    
    weather = welcome + weather_temperature + temperature + weather_condition + condition + "."
    
    print(weather)
    
    return weather

def num_convert(num):
    if(num == '1st' or num == 'first'):
        return 0
    elif num == '2nd' or num == 'second':
        return 1
    elif num == '3rd' or num == 'third':
        return 2
    elif num == '4th' or num == 'fourth':
        return 3
    elif num == '5th' or num == 'fifth':
        return 4
    elif num == '6th' or num == 'sixth':
        return 5
    else:
        return -1

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def event_wrapper():
    # Wrapper function for the events that will call the event function and turn it into a string.
    # It will also filter the events through a blacklist if needed.
    
    # Get events
    eventDate = ''
    event_list = []
    try:
        file = open("/tmp/event.txt", "r")
        #        file = open("event.txt", "r")
        data = file.read().splitlines()
        eventDate = data[0][:10]
        for i in range(1, len(data)):
            event_list.append(data[i].split("@!"))
    except:
        event_list = get_events()
    finally:
        if(eventDate != currentDate):
            event_list = get_events()
    if not event_list:
        return 'No events happening on campus today!'
    #event_list = get_events()
    # Convert the list into a string
    event_string = 'The current events today are <break time="700ms"/>'
    for j in range(0, len(event_list)):
        temp = event_list[j][1]
        #print(event_list[j][1])
        try:
            dt = temp.split("@ ",1)[0]
            time = temp.split("@ ",1)[1]
            if len(time) < 10:
                temp = ' . . at ' + time
            else:
                temp = ' .. from ' + time
            #print (custom_strftime('%B {S}, %Y', now))
            currentDateFormat2 = custom_strftime('%B {S}, %Y', now)
            currentDateFormat2 = currentDateFormat2 + ' '
            try:
                dt = dt.split(', ')
                dt = dt[1] + ', ' + dt[2]
                print(dt)
            except:
                print(dt)
            
            if(dt == currentDateFormat2):
                print("True")
            else:
                continue
        except:
            temp = ' . . happening right now'
        if j != 0:
            event_string = event_string + '<break time="700ms"/>' + event_list[j][0] +  temp + ' in ' + event_list[j][2] + ' '
        else:
            event_string = event_string + event_list[j][0] +  temp + ' in ' + event_list[j][2] + ' '
    
    # Start checking the events for blacklisted words
    blacklist = [['uta.edu', ' U.T.A dot e.d.u'], ['\xa0', ' '], ['UTA', ' U.T.A '], ['&', ' and ']]
    m = 0
    for m in range(0, len(blacklist)):
        event_string = re.sub(blacklist[m][0], blacklist[m][1], event_string, flags=re.IGNORECASE)
    
    return event_string

def get_events():
    # Finds the current events on campus and returns a list of the events with times, locations, names
    try:
        os.remove("/tmp/event.txt")
    except:
        print('do nothing')
    # Parse Event WebPage
    site_base = 'http://www.theshorthorn.com'
    quote_page = 'http://www.theshorthorn.com/calendar/'
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    
    # Find Top Events from Page
    top_events = soup.find('div', attrs={'id': 'tncms-region-index-full'})
    
    # Get href links to events and store in a list
    links = [a['href'] for a in top_events.find_all('a', href=True) if a.text.strip()]
    
    # Enter loop to build the list of links and pull data & set up the list to put in
    full_links = []
    breaker = 1
    print('links: ' + str(len(links)))
    for link in links:
        temp = site_base + link
        if temp[:-9] not in full_links:
            full_links.append(temp)
        else:
            breaker = breaker - 1
        if breaker == 8:
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
    
    file = open('/tmp/event.txt','w+')
    file.write(currentDate)
    file.write('\n')
    j = 0
    for j in range(0, len(event_list)):
        for i in range(0, len(event_list[j])):
            file.write(event_list[j][i])
            if(i != (len(event_list[j]) - 1)):
                file.write('@!')
        file.write('\n')
    file.close()
    return event_list

def get_article_wrapper(genre1):
    articleDate = ''
    contents = []
    checker = False
    genre = ''
    if(genre1 == 'life and entertainment'):
        genre = 'life entertainment'
    else:
        genre = genre1
    
    fname = '/tmp/' + genre + '.txt'
    final_article = []
    try:
        file = open(fname, "r")
        data = file.read().splitlines()
        articleDate = data[0][:10]
        i = 0
        for i in range(2, len(data)):
            contents.append(data[i])
        temp_string = data[1]
        final_article = [temp_string, contents]

    except:
        final_article = get_article(genre)
        checker = True
    finally:
        if (articleDate != currentDate) and (currentHour > 9) and (checker == False):
            final_article = get_article(genre)

    return final_article

def get_article(genre):
    # This will find all the articles of today and return a list of headlines and contents
    fname = '/tmp/' + genre + '.txt'
    try:
        os.remove(fname)
    except:
        print('do nothing')

    temp_string = ''
    contents = []
    now = datetime.datetime.now()
    currentDate = str(now)[:10]
    currentHour = now.hour
    
    # Set webpage to specified
    site_base = 'http://www.theshorthorn.com'
    quote_page = get_page(genre)
    
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
        
        paragraphs = soup.find('div', attrs={'class': 'asset-content subscriber-premium'})
        try:
            p = paragraphs.find_all('p')
            headlines.append(headline.text.strip())
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
    blacklist = [['news-editor.shorthorn@uta.edu', 'news-editor dot shorthorn at U.T.A dot E.D.U'], [' @', ' Author '], ['uta.edu', ' U.T.A dot e.d.u'], ['\xa0', ' '], ['UTA', ' U.T.A '], ['10-20-30', 'ten-twenty-thirty'], ['&', ' and ']]
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
    file = open(fname,'w+')
    file.write(currentDate)
    file.write('\n')
    file.write(temp_string)
    file.write('\n')
    j = 0
    for j in range(0, len(article[1])):
        file.write(article[1][j])
        file.write('\n')

    file.close()
    return final_article

#sample = get_weather()
#print(get_weather())
#print(event_wrapper())
#print(get_article('news'))

#This is the lambda function, the event parameter is the Jason request from which we will extract the intents.
def create_response(input):
    output = '<speak>' + input + '</speak>'
    response_2 =    {
        'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': output,
                    },
                'shouldEndSession': 'false'
                    }
                }
    return response_2

def create_response_end(input):
    output = '<speak>' + input + '</speak>'
    response_2 =    {
        'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'SSML',
                    'ssml': output,
                    },
                'shouldEndSession': 'true'
                }
        }
    return response_2



def lambda_handler(event, context):
    # This is to check to make sure our app is the only skill that can access this lambda function
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    #Thus is where we return a response in JASON format to the Alexa skill speach output.
    #intentName=event["request"]["intent"]["name"]
    if event["request"]["type"] == 'LaunchRequest':
        try:
            welcome_message = get_weather()
            welcome_message = welcome_message + '<break time="700ms"/> How can I help you?'
            return create_response(welcome_message)
        except:
            return create_response('Welcome to U.T.A Short horn news! <break time="700ms"/> How can I help you?')
    
    elif event["request"]["type"] == 'IntentRequest':
        intentName=event["request"]["intent"]["name"]
        if intentName == 'ReadHeadlinesIntent':
            GT = get_article_wrapper("news")
            headlines_out = GT[0]
            return create_response_end(headlines_out)
        
        elif intentName == 'ReadGenreHeadlines':
            Genre = event["request"]["intent"]["slots"]["Gen"]["value"]
            GT = get_article_wrapper(Genre)
            headlines_out = GT[0]
            return create_response_end(headlines_out)
        
        elif intentName == 'ReadSpecificArticle':
            num = event["request"]["intent"]["slots"]["Num"]["value"]
            GT = get_article_wrapper('news')
            num = num_convert(num)
            if (num != -1):
                content = GT[1][num]
                return create_response_end(content)
            
            else:
                return create_response_end('Invalid Request')

        elif intentName == 'ReadSpecificArticleGenre':
            num = event["request"]["intent"]["slots"]["Num"]["value"]
            Genre = event["request"]["intent"]["slots"]["Gen"]["value"]
            GT = get_article_wrapper(Genre)
            num = num_convert(num)
            if (num != -1):
                content = GT[1][num]
                return create_response(content)
            else:
                return create_response_end('Invalid Request')

        elif intentName == 'EventsIntent':
            output = event_wrapper()
            return create_response_end(output)

        elif intentName == 'AMAZON.StopIntent':
            return create_response_end('')

        elif intentName == 'AMAZON.CancelIntent':
            return create_response_end('Goodbye')
        elif intentName == 'CacheIntent':
            try:
                temp = get_article('news')
                temp = get_article('life entertainment')
                temp = get_article('opinion')
                temp = get_article('sports')
                temp = get_events()
                return create_response_end('Cash updated!')
            except:
                return create_response_end('Something went wrong!')



#returning the response JASON structure
#return response

