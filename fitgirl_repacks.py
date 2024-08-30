#VERSION: 1.1
# AUTHORS: Bioux, Ralkey

import json
from http.cookiejar import CookieJar
from urllib.parse import unquote
from urllib.request import HTTPCookieProcessor, build_opener

try:
    from novaprinter import prettyPrinter  # Production environment
except ImportError:
    # Mock for development
    def prettyPrinter(data):
        print(data)


USER_AGENT: tuple = ('User-Agent',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
    'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15')


class fitgirl_repacks(object):
    url = 'https://fitgirl-repacks.site/'
    name = 'FitGirl Repacks'
    supported_categories = {'all': ''}

    cj = CookieJar()
    session = build_opener(HTTPCookieProcessor(cj))
    session.addheaders = [USER_AGENT]

    def search(self, what, cat='all'):
        search_url = 'https://hydralinks.cloud/sources/fitgirl.json'

        with self.session.open(search_url, timeout = 10) as response:
            response = response.read()
            response_json = json.loads(response)

            what = unquote(what)
            search_terms = what.lower().split()

            for result in response_json['downloads']:
                if any(term in result['title'].lower() for term in search_terms):
                    res = {'link': self.download_link(result),
                        'name': result['title'],
                        'size': result['fileSize'],
                        'seeds': '-1',
                        'leech': '-1',
                        'engine_url': self.url,
                        'desc_link': '-1'}
                    prettyPrinter(res)

    def download_link(self, result):
            return result['uris'][0]
    
if __name__ == "__main__":
    test = fitgirl_repacks()
    test.search("grand theft auto")
