import requests
from bs4 import BeautifulSoup
from menu import menu
import os
import re

# updates the requested page and soupvar
def updatePage():
    global page
    global soup
    page  = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

# Updates the url which is used to send request
def updateUrl(x):
    global url
    url = def_url() + x
    print('New url is: %s' % url)
    
def readChosenCity():
    with open('chosen_city.txt', 'r') as f:
        city = f.read()
        if len(city) != 0 and not checkRequestError():
            updateUrl(city)
        else:
            global runMenu
            runMenu = False
            print("Error, no page content")
def getChosenCity():
    return open('chosen_city.txt', 'r')

def setChosenCity(inp):
    with open('chosen_city.txt', 'w') as f:
        f.write(inp)
        # Update city so file doesnt have to open twice.
        updateChosenCity(inp)
def updateChosenCity(inp):
    global city
    city = inp 
def promptChosenCity():
    setChosenCity(input('Select new city: '))
def checkRequestError():
      return re.search('Någonting gick fel', soup.text)
def getNotifications(soup):
    try:
        # check if there are any notifications on site
        r = soup.find_all('p', class_='notification-text')
        print(r[1].text)
        print(r[0].text)
    except IndexError:
        print("No Notifications to show")

def getTodayTemp(soup):
    try:
        # GET ELEMENT BY class
        r = soup.find_all('span', class_='temp-high')
        # PRINT
        print('Dagens temperatur: ' + r[0].text)
    except IndexError:
        print("No Temperature found")       

def getDownfall(soup):
    try:
        r = soup.find_all('p', class_='rain-value')
        txt = r[0].text.lstrip()
        txt = txt.rstrip()
        # Lägga in rstrip också?
        print('Dagens regn: %s' % txt)
    except IndexError:
        print("No Rainvalue found")


def getWind(soup):
    try:
        r = soup.find_all('p', class_='wind-value')
        txt = r[0].text.lstrip()
        print('Vind: %s' % txt)
    except IndexError:
        print("No Windvalue found")

def pretty():
    return soup.prettify()

def show_week():
    print(
        'Monday' + 'Tuesday' + 'Wednesday \n' 
        + '1' + '2' + '3'
    )
# TODO: Rename to scrape
def run_main():
    global city
    check_os_clear()
    print(f"<-- {city} -->")
    getTodayTemp(soup)
    getDownfall(soup)
    getWind(soup)
    getNotifications(soup)

def check_os_clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        pass

# TODO: implement this
def init():
    pass
def def_url():
    return 'https://www.klart.se/'
'''
    In the event a request returns with more than 1 choice of city,
    prompt user for specification.
'''
def mul_responses():
    # prompt for another city
    print("Request gave several answers!")
    # Scrape different places in response
    r = soup.find_all('span', class_='place')
    # create a list of places
    places = list(x.text for x in r)
    # print(*places)
    # prompt user for specific place/city
    m = menu(*places)
    updateUrl(m.getMenuItem().strip())
    updatePage()
    setChosenCity(m.getMenuItem().strip())
    #setChosenCity(m.getMenuItem().strip())

def sendRequest():
    global url
    global page
    # GET THE PAGE
    print("Requesting: %s" % url)
    page = requests.get(url)
    # repr chosen city
    soupPage()
         
def soupPage():
    global page
    global soup
    soup = BeautifulSoup(page.content, 'html.parser')
'''
    Globals
'''
# Loopswitch
runMenu = True
# Set the city
city = getChosenCity().read()
# BaseURL
url = def_url() + city
# Send request
page = requests.get(url)
# soupify
soup = soupPage()
# Exit var
exit = False

# DEBUG
#print(soup)
if __name__ == '__main__':
    while True:
        init()
        check_os_clear()
        sendRequest()
        '''
            If runMenu is set to true, the script runs. runMenu is false if
            there are more than 1 response from the webscraped website.
        '''
        if runMenu:
            # Check if the chosen city was correctly gotten
            if not re.search("Någonting gick fel", soup.text):
                print("A page was found \n\n")
                # Run the main method
                run_main()
               # print(soup)
                # TODO:
                # show_week()
            else:
                # handler for multiple responses
                mul_responses()
        else:
            with open('chosen_city.txt', 'w') as f:
                f.write(input('Please choose a city . . .\n'))
                updatePage()
        # Print the menu
        print('\n--------------------------------\n')
        menu_choice = input('1) Refresh \n2) Select another day \n3) Select city \n5) Quit \n\nSelect --> ')
        if not menu_choice.isalnum() or not len(menu_choice) == 1:
            check_os_clear()
            print("Please choose a number")

        elif menu_choice == '1':
            run_main()
        elif menu_choice == '2':
            pass
        elif menu_choice == '3':
            promptChosenCity()
            # setChosenCity()
            readChosenCity()
            updatePage()
        else:
            check_os_clear()
            exit = True
            break
        if exit:
            break
