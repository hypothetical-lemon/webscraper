import json
import certifi
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from json import JSONEncoder


class Review(JSONEncoder):
    def __init__(self):
        super().__init__()
        self.data = dict()

    def default(self, o):
        return o.__dict__


def webscrap():
    url = "https://www.coffeereview.com/top-30-coffees-2017/"

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url, retries=False)
    soup = BeautifulSoup(response.data, "html.parser")
    marshalobj = []
    # get all links with words "review"
    for link in soup.find_all('a'):
        if link.get('title') == "Read Complete Review":
            # follow link
            print(link.get('href'))
            # set up selenium driver
            driver = webdriver.Chrome()
            driver.implicitly_wait(30)
            driver.get(link.get('href'))
            # get request
            soup2 = BeautifulSoup(driver.page_source, "html.parser")
            tags = soup2.find_all("p")
            review = Review()

            # loop thru webpage
            for tag in tags:
                if tag is not None:
                    expr = re.compile(':|[.]')
                    if re.search(expr, str(tag)):
                        print(tag.get_text())
                        str1 = str(tag.get_text()).split(":")
                        if len(str1) > 1:
                            review.data[str1[0]] = str1[1]
                            marshalobj.append(review)
            with open('coffeeData.json', 'w') as outfile:
                json.dump([ob.data for ob in marshalobj], outfile)

            driver.close()


if __name__ == '__main__':
    webscrap()
