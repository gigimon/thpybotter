import requests
from lxml import html

class Kinopoisk:
    """Kinopoisk parser class"""
    def __init__(self):
        self.search_url = "http://www.kinopoisk.ru/index.php?first=yes&what=&kp_query=%s"
        self.id_url = "http://www.kinopoisk.ru/film/%d/"
        self.kinopoisk_url = "http://www.kinopoisk.ru"

    def parse(self, url):
        headers = {
                "User-Agent": 
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
                }

        req = requests.get(url, headers=headers)
        tree = html.fromstring(req.content)

        try:
            if req.history:
                movie_url = self.kinopoisk_url + req.history[0].headers['location']
            else:
                movie_url = url
            
            top250_tree = tree.xpath("//span[@style='color: #007; font-size: 21px; position: absolute; top: 4px; left: 30px; margin-top:7px;']")
            
            if top250_tree:
                top250 = top250_tree[0].getchildren()[0].text
            else:
                top250 = None

            return  {
                    "name": tree.xpath("//h1[@itemprop='name']")[0].text_content(),
                    "altname": tree.xpath("//span[@itemprop='alternativeHeadline']")[0].text_content(),
                    "year": tree.xpath("//div[@style='position: relative']")[0].text_content().strip(),
                    "country": tree.xpath("//div[@style='position: relative']")[1].text_content().strip(),
                    "slogan": tree.xpath("//td[@style='color: #555']")[0].text_content(),
                    "description": tree.xpath("//div[@itemprop='description']")[0].text_content().strip().replace(u"\x97", "-"),
                    "director": tree.xpath("//td[@itemprop='director']")[0].text_content(),
                    "duration": tree.xpath("//td[@id='runtime']")[0].text_content(),
                    "genre": tree.xpath("//span[@itemprop='genre']")[0].text_content(),
                    "rating": tree.xpath("//span[@class='rating_ball']")[0].text_content(),
                    "ratingCount": tree.xpath("//span[@class='ratingCount']")[0].text_content(),
                    "url": movie_url,
                    "top250": top250
                    }

        except:
            return None 

    def search_movie(self, namestr):
        """ Returns the first found item """
        return self.parse(self.search_url % namestr)

    def get_movie(self, id):
        """ Returns result by given ID """
        return self.parse(self.id_url % id)
