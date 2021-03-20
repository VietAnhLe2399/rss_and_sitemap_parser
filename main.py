import os
from pathlib import Path

from constants import ResultType, BASE_PATH, PROPERTIES_FILE
from sitemap_utils import find_all_sitemaps
from url_utils import get_all_rss, get_domain
import json


def save_result(result_list, url, result_type):
    if not Path(BASE_PATH).exists():
        Path(BASE_PATH).mkdir()
    domain = get_domain(url)
    if result_type == ResultType.RSS:
        result_name = f'{domain}_RSSs'
    else:
        result_name = f'{domain}_sitemaps'

    with open(os.path.join(BASE_PATH, result_name + '.txt'), "w") as record_file:
        json.dump({result_name: result_list}, record_file)


if __name__ == '__main__':
    with open('domains.txt') as f:
        domain_list = f.read().splitlines()

    if not os.path.isfile(PROPERTIES_FILE):
        with open(PROPERTIES_FILE, 'w') as f:
            json.dump({}, f)
    with open(PROPERTIES_FILE) as f:
        properties_records = json.load(f)

    for domain in domain_list:
        # Comment statement below to parse all websites
        if domain in properties_records:
            continue

        print(f'\n----------------\n{domain}\n----------------\n')
        print('*** GET RSS ***')
        list_rss = get_all_rss(domain)
        save_result(list_rss, domain, ResultType.RSS)

        print('*** GET SITEMAP ***')
        list_sitemap = find_all_sitemaps(domain)
        print(list_sitemap)
        save_result(list_sitemap, domain, ResultType.SITEMAP)

        properties_records[domain] = {}
        properties_records[domain]['rss_count'] = len(list_rss)
        properties_records[domain]['sitemap_count'] = len(list_sitemap)

    with open(PROPERTIES_FILE, 'w') as f:
        json.dump(properties_records, f)
