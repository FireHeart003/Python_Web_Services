# Useful Params
# print response
# print(response)
#
# # print url
# print(response.url)
#
# # print(response.status_code)
# print(response.history)
from urllib.parse import urlparse

# Get request for a website
# Get the response.history => Lets me know if there were any redirects
# If the response is any status code in the 300s
# Get the response.url
# Print the response.url


# import requests module and beautiful soup
import requests
from bs4 import BeautifulSoup
import csv

# Figuring out the redirects
# Set verify = true, https
    # Set verify = false if SSL Cert Invalid
def get_response_status(link):
    response_url = ''
    try:
        # Making a get request
        url = 'http://' + link
        response_url = url
        response = requests.head(url, timeout = 5)
        if 300 <= response.status_code < 400:
            return str(response.status_code) + ": " + response.url
        elif 200 <= response.status_code < 300:
            r = requests.get(url, verify= False)
            soup = BeautifulSoup(r.text, 'html.parser')
            return str(response.status_code) + ": " + soup.title.string + "~" + response.url
        else:
            return str(response.status_code) + ": " + str(response.url)
    except requests.exceptions.SSLError as e:
        return e
    except requests.exceptions.ConnectTimeout:
        return "Connection Timeout for: " + response_url
    except Exception as e:
        return e

def get_ip_address(url):
    urlparse(url).hostname

with open('domains.csv', mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        print(get_response_status(lines[0]))
