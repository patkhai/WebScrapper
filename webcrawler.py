import requests
import argparse
from urllib.error import URLError, HTTPError
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup


def checkURL(url):
    """
    This method checks if the url is valid 
    """
    try:
        result = urlparse(url)
        return bool(result.netloc) and bool(result.scheme)
    except HTTPError:
        return False
    except URLError:
        return False
    except ValueError: 
        return False 

inboundLink = set()
outboundLink = set()

def searchURL(url):
    """
    This method will returns all the links(urls) found in the webpage. 
    You can change the limit value up to your preference.
    By doing so the search will halt as soon as it hits the limit instead of filtering it after 
    finding all the matches 
    """
    urls = set()
    mainURL = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for href in soup.findAll("a", limit =30):
        link = href.attrs.get("href")

        if link == "" or link is None:
            continue

        link = urljoin(url, link)
        fullpath = urlparse(link)
        #urlparse for URL specify format 
        link = fullpath.scheme + "://" + fullpath.netloc + fullpath.path

        if not checkURL(link):
            continue
        if link in inboundLink:
            continue
        if mainURL not in link:
            if link not in outboundLink and not link.startswith("mailto:") and not link.startswith("tel:"):
                print(link)
                outboundLink.add(link)
            continue
        print(link)
        urls.add(link)
        inboundLink.add(link)
    return urls


def listURL(url):
    """
    print out all the url found with the domain on multiple levels
    """
    for links in searchURL(url):
        return listURL(links)

def main(): 
    parser = argparse.ArgumentParser(description="Python Web Crawler")
    parser.add_argument("url", help="Put the url to be crawled")
    args = parser.parse_args()
    listURL(args.url)
    print("\nTotal webpages crawled: {}\n".format(len(outboundLink) + len(inboundLink)))

if __name__ == "__main__":
    main()
    