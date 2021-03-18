FEED_SEARCH_API = 'https://feedsearch.dev/api/v1/search?url='
BASE_PATH = 'result'
PROPERTIES_FILE = 'properties.txt'
SITEMAP_LOCATIONS = [
    '/sitemap.xml',
    '/feeds/posts/default?orderby=updated',
    '/sitemap.xml.gz',
    '/sitemap_index.xml',
    '/s2/sitemaps/profiles-sitemap.xml',
    '/sitemap.php',
    '/sitemap_index.xml.gz',
    '/vb/sitemap_index.xml.gz',
    '/sitemapindex.xml',
    '/sitemap.gz',
    '/sitemap_news.xml',
    '/sitemap-index.xml',
    '/sitemapindex.xml',
    '/sitemap-news.xml',
    '/post-sitemap.xml',
    '/page-sitemap.xml',
    '/portfolio-sitemap.xml',
    '/home_slider-sitemap.xml',
    '/category-sitemap.xml',
    '/author-sitemap.xml'
]


class ResultType:
    RSS = 'rss'
    SITEMAP = 'sitemap'
