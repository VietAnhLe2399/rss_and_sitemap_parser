import gzip
import io
import urllib.robotparser
import urllib.request
import requests
from bs4 import BeautifulSoup as Soup

from constants import SITEMAP_LOCATIONS
from url_utils import get_domain_with_scheme


def find_robots(url):
    """
    :param url: any url of website
    :return: (bool: is robots.txt exists, string: robots.txt if exists)
    """
    domain_with_scheme = get_domain_with_scheme(url)
    robots_url = domain_with_scheme + '/robots.txt'
    response = requests.get(robots_url)
    if response.status_code == 200:
        return True, robots_url
    return False, ''


def find_sitemap_in_robots(robots_url):
    """
    return list of all sitemaps in robots.txt file
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    result = rp.site_maps()
    return result if result is not None else []


def find_sitemap_with_locations(url):
    """
    :param url: any url of website
    :return: (bool: is sitemap exists, string: sitemap if exists)
    """
    domain_with_scheme = get_domain_with_scheme(url)

    for location in SITEMAP_LOCATIONS:
        sitemap_url = domain_with_scheme + location
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            return True, sitemap_url

    return False, ''


def find_main_sitemaps(url):
    """
    :param url: Website's url
    :return: list sitemaps from robots.txt and locations
    """
    list_sitemap = []
    # find sitemap by robots
    robots_exists, robots_url = find_robots(url)
    if robots_exists:
        list_sitemap += find_sitemap_in_robots(robots_url)

    # find sitemap by location
    sitemap_exists, location = find_sitemap_with_locations(url)
    if sitemap_exists and location not in list_sitemap:
        list_sitemap.append(location)
    return list_sitemap


def find_all_sitemaps(url):
    list_sitemap = find_main_sitemaps(url)
    # limit list_sitemap here
    for sitemap in list_sitemap:
        list_sitemap += parse_sitemap(sitemap)

    return sorted(list(set(list_sitemap)))


def parse_sitemap(sitemap_url):
    print('Parsing sitemap: ' + sitemap_url)
    result = []
    try:
        if '.gz' in sitemap_url:
            response = urllib.request.urlopen(sitemap_url)
            compressed_file = io.BytesIO(response.read())
            decompressed_file = gzip.GzipFile(fileobj=compressed_file)
            soup = Soup(decompressed_file, 'lxml')
        else:
            response = requests.get(sitemap_url)
            soup = Soup(response.content, 'lxml')

        list_sitemap_tag = soup.find_all('sitemap')

        if list_sitemap_tag is not None:
            for sitemap_tag in list_sitemap_tag:
                sitemap = sitemap_tag.find('loc').string
                result.append(sitemap)
                result += parse_sitemap(sitemap)
    except:
        print('___ Cant connect to sitemap url ___')
    finally:
        return result
