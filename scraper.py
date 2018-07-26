import requests
from lxml import etree
from urllib.parse import urljoin
from models import Child
from helpers import requests_image


class Scraper:
    def __init__(self):
        self.session = None
        self.scraped_ids = set()
        self.scraped_names = set()
        self.initiate_session()

    def initiate_session(self):
        self.session = requests.session()
        self.session.headers.update(Scraper.get_header())

    @staticmethod
    def get_header():
        headers = {
            'Connection': "keep-alive",
            'Cache-Control': "no-cache",
            'Origin': "http://trackthemissingchild.gov.in",
            'Upgrade-Insecure-Requests': "1",
            'Content-Type': "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Referer': "http://trackthemissingchild.gov.in/trackchild/photograph_missing.php",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-US;q=0.6,en-GB;q=0.5",
        }
        return headers

    def scrape_missing(self):
        url = "http://trackthemissingchild.gov.in/trackchild/photograph_missing.php"
        for i in range(1, 10):
            payload = "pagination=pagination&page="+str(i)+"&filter=child"
            response = self.session.post(url, data=payload)
            tree = etree.HTML(response.text)
            details = tree.xpath('/html/body/div[1]/div[3]/div[2]/div[2]/a/@value')
            for entities, detail in zip(response.text.split("missing_id=")[1:], details):
                phone_number = detail.split("Mobile:")[1].split("<br/>")[0]
                missing_id = entities.split("\"")[0]
                if missing_id in self.scraped_ids:
                    pass
                else:
                    self.scraped_ids.add(missing_id)
                    self.scrape_each_child(missing_id, phone_number)

    def scrape_each_child(self, missing_id, phone_number):
        url = "http://trackthemissingchild.gov.in/trackchild/missing_dtl.php"
        base_path = "http://trackthemissingchild.gov.in/trackchild/"

        querystring = {"missing_id": missing_id,
                       "category": "91.92.98.105"}
        response = self.session.get(url, params=querystring)
        tree = etree.HTML(response.text)
        name = tree.xpath('//*[@id="cont-1"]/p[1]//text()')

        try:
            if name[1] in self.scraped_names:
                pass
            else:
                self.scraped_names.add(name[1])
                name = name[1]
                age = tree.xpath('//*[@id="cont-1"]/p[2]//text()')[1]
                gender = tree.xpath('//*[@id="cont-1"]/p[3]//text()')[1]
                guardian_name = tree.xpath('//*[@id="cont-1"]/p[4]//text()')[1]
                place_of_missing = tree.xpath('//*[@id="cont-1"]/p[5]//text()')[1]
                date_of_missing = tree.xpath('//*[@id="cont-1"]/p[6]//text()')[1]
                image_path_rel = tree.xpath('//*[@id="childphoto"]/div/div/img/@src')[0]
                image_url = urljoin(base_path, image_path_rel)
                try:
                    if int(age.split(" ")[0]) < 19:
                        child_id = Child.generate_id()
                        child = Child()
                        child.child_id = child_id
                        child.child_name = name
                        child.guardian_name = guardian_name
                        child.date_of_missing = date_of_missing
                        child.place_of_missing = place_of_missing
                        child.gender = gender
                        child.age = int(age.split(" ")[0])
                        child.image_url = image_url
                        child.phone_number = phone_number
                        child.image_path = "images/"+str(child_id)
                        requests_image(image_url, "images/"+str(child_id))
                        try:
                            child.save()
                        except Exception as e:
                            print(e)
                except IndexError as e:
                    print(e)
        except IndexError as e:
            print(e)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape_missing()
        

