import json
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup as Soup
from googlesearch import search

from constants import FEED_SEARCH_API


def get_domain(url):
    """
    :param url: any url of any website
    :return: website's domain
    """
    return urlparse(url).netloc


def get_scheme(url):
    """
    :param url: any url of any website
    :return: website's scheme
    """
    return urlparse(url).scheme


def get_domain_with_scheme(url):
    """
    :param url: any url of any website
    :return: website's domain with scheme
    """
    return get_scheme(url) + "://" + get_domain(url)


def find_rss_link_home_page(url):
    result = []
    res = requests.get(url)
    soup = Soup(res.text, 'html.parser')
    all_a = soup.find_all('a')
    for a in all_a:
        if 'rss' in str(a).lower():
            result.append(urljoin(url, a['href']))
    return result


def find_rss_in_page(url, domain):
    result = []
    soup = Soup(requests.get(url).text, 'html.parser')
    all_a = soup.find_all('a')
    for a in all_a:
        if 'href' in str(a):
            if '.rss' in str(a['href']).lower() or '/rss/' in str(a['href']).lower():
                rss_url = urljoin(domain, a['href'])
                result.append(rss_url)
    return result


def find_rss_with_feed_search(url):
    result = []
    res = requests.get(FEED_SEARCH_API + url)
    json_res = json.loads(res.text)
    for item in json_res:
        rss_url = item['url']
        result.append(rss_url)
    return result


def get_rss_results_from_gg(domain):
    result = []
    query = domain + ' rss'
    for url in search(query, tld="co.in", num=10, stop=10, pause=2):
        if domain in url and 'rss' in str(url).lower():
            rss_in_page = find_rss_in_page(url, domain)
            result += rss_in_page
    return result


def parse_rss(url):
    print('Parsing RSS: ' + url)
    result = []
    try:
        res = requests.get(url, timeout=10)
        soup = Soup(res.text, 'lxml')
        items = soup.find_all('item')
        for item in items:
            if item.link is not None:
                item_url = item.link.next_sibling
                if item_url[-1] == '\n':
                    item_url = item_url[:-1:]
                # change .rss -> rss to get all url contains rss
                if '.rss' in item_url:
                    result.append(item_url)
                    result += parse_rss(item_url)
    except:
        print('___ Cant connect to RSS url ___')
    finally:
        return result


def get_all_rss(domain):
    rss_urls_in_home = find_rss_link_home_page(domain)
    rss_home = []
    for url in rss_urls_in_home:
        rss_home += find_rss_in_page(url, domain)
    rss_feed_search = find_rss_with_feed_search(domain)
    rss_gg = get_rss_results_from_gg(domain)

    main_rss = list(set(rss_home + rss_feed_search + rss_gg))
    result = main_rss

    for rss_url in main_rss:
        result += parse_rss(rss_url)
    result = list(set(result))

    return sorted(result)
