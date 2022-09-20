from multiprocessing import context
import requests
import pandas as pd
from bs4 import BeautifulSoup 
from email.message import EmailMessage
import ssl
import smtplib


# Read the CSV file
data = pd.read_csv('https://www.imdb.com/list/ls565814860/export')
data_title = data['Title'].tolist() # Creates a list from the Const column of the CSV


# Transforms the names in link names, repalace any space with "+"
new_names = []
for name in data_title:
    new_name = name.replace(' ', '+')
    new_names.append(new_name)


# Here we create the link list
link_list = [] # This is the list with all links that we need
for names in new_names:
    url = f'https://www.1377x.to/search/{names}/1/'
    link_list.append(url)


# This is the funtion that converts the list to string, so we can put it in the body email
def ListToString(s):
    str1 = ' '
    return (str1.join(s))


# The list of all names and links
names_Links = []


email_body_str = ListToString(names_Links)


# Here we will search for the download link
for link in link_list:
    url = requests.get(link).text
    soup = BeautifulSoup(url, 'html.parser')
    name_movie = soup.find('td', class_ = 'coll-1 name').text.replace('.', ' ')
    
    linksList = [] # The list of all the names

    for ele in soup.find_all('a'):
        links = ele.attrs['href']
        linksList.append(links)

    messages = f"""
The name of the movie is: {name_movie}
Download links:
https://www.1377x.to/{linksList[32]}
https://www.1377x.to/{linksList[35]}
https://www.1377x.to/{linksList[38]}
https://www.1377x.to/{linksList[41]}
    """
    names_Links.append(messages)

    
email_body_str = ListToString(names_Links)

email_sender = 'email sender'
email_password = '16 digit password'
email_receiver = 'email receiver'
subject = 'Movies and Links'
body = f"""
{email_body_str}
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
