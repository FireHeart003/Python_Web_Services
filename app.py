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
import socket
from concurrent.futures import ThreadPoolExecutor

# Figuring out the redirects
# Set verify = true, https
    # Set verify = false if SSL Cert Invalid

ret = []
def get_response_status(link):
    ip = ''
    response_url = ''
    try:
        # Making a get request
        url = 'https://' + link
        response_url = url
        response = requests.head(url, timeout = 5)
        ip = (get_ip_address(url))
        # if 300 <= response.status_code < 400:
        #     ret.append([response.status_code, "", ip, url])
        #     return str(response.status_code) + " ~ IP: " + ip + " ~ " +  url
        if 200 <= response.status_code < 300:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            if soup.title:
                ret.append([response.status_code, soup.title.string, url])
                return str(response.status_code) + ": " + soup.title.string + " ~ IP: " + ip +  " ~ " + url
            else:
                ret.append([response.status_code, "", url])
                return str(response.status_code) + " ~ IP: " + ip + " ~ " + url
        # else:
        #     ret.append([response.status_code, "", ip, url])
        #     return str(response.status_code) + ": " + " ~ IP: " + ip + " ~ " + url
    except requests.exceptions.SSLError:
        # ret.append(["SSL Error", "", ip, response_url])
        return "SSL Error for: " + response_url
    except requests.exceptions.ConnectTimeout:
        # ret.append(["Connection Timeout", "", ip, response_url])
        return "Connection Timeout for: " + response_url
    except requests.exceptions.ReadTimeout:
        # ret.append(["Read Timeout", "", ip, response_url])
        return "Connection Read Timeout for: " + response_url
    except requests.exceptions.TooManyRedirects:
        # ret.append(["Too Many Redirects", "", ip, response_url])
        return "Too many redirects for: " + response_url
    except requests.exceptions.ConnectionError:
        # ret.append(["Connection Error", "", ip, response_url])
        return "Connection Error for " + response_url
    except Exception as e:
        return e

def get_ip_address(url):
    hostname = urlparse(url).hostname
    return socket.gethostbyname(hostname)

def threader(urls):
    with ThreadPoolExecutor(max_workers = 100) as executor:
        data = list(executor.map(get_response_status, urls))
    return data

urls = []
with open('domains.csv', mode='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        urls.append(lines[0])

results = threader(urls)
print(results)

with open('filtered.csv', mode = 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Status Code/Error", "Title", 'URL'])
    writer.writerows(ret)
    print(len(ret))
