import scrapy
import re
import numpy as np
# wichtig bei inport von items
from thomann.items import ThomannItem



class Thomann_Spider(scrapy.Spider):
    name = 'thomann_spider'
    start_urls = [
        
        'https://www.thomann.de/de/e-gitarren.html',
        'https://www.thomann.de/de/konzertgitarren.html',
        'https://www.thomann.de/de/westerngitarren.html',
        'https://www.thomann.de/de/e-baesse.html',
        'https://www.thomann.de/de/akustikbaesse.html',
        'https://www.thomann.de/de/bluegrass_instrumente.html'

    ]


    # Unterkategorie
    def parse(self, response):
        """ Einstieg erfolgt bei der Uebersichtsseite. Hier kann zwischen mehreren Gitarrentypen ausgewaehlt werden (ST,LP, usw)
            Die Kategorie ist der entsprechende Gitarrentyp und wird schon hier extrahiert. Sets werden ausgeschlossen
        """
        categorie = response.xpath('//div[@class="rs-cat header"]//h1/text()').extract_first()

        for sel in response.xpath('//div[@class="grid-section"]//li'):
            guitar_type = sel.xpath('.//span[@class="name"]/text()').extract_first()
        
            # Sets ausschließen, da diese mehrere Produkte beinhalten
            if not re.search(r" [Ss]ets?|[Ss]ets? |[A-Za-z]+sets?", guitar_type):
                url = sel.xpath('.//a/@href').get()
                request = scrapy.Request(url=url, callback=self.parse_all_articles)
                # speichere informationen als meta um sie in der nächsten Funktion verwenden zu können
                request.meta['categorie'] = categorie
                request.meta['guitar_type'] = guitar_type   
                yield request
        

    # Produktkategorie
    def parse_all_articles(self, response):
        categorie = response.meta.get("categorie")
        guitar_type = response.meta.get("guitar_type")
        
        for sel in response.xpath('//div[@class="extensible-article list-view compare parent"]'):
            url = sel.xpath('.//div[@class="right"]/div[@class="top"]/div[@class="head"]/a/@href').get()
            manufacturer = sel.xpath('.//span[@class="manufacturer"]/text()').extract_first()
            request = scrapy.Request(url=url, callback=self.parse_article_page)
            # speichere informationen als meta um sie in der nächsten Funktion verwenden zu können
            request.meta['categorie'] = categorie
            request.meta['guitar_type'] = guitar_type
            request.meta['manufacturer'] = manufacturer   
            yield request
            
        # Folgeseiten scrapen
        next_page = response.xpath('//div[@class="container"]//a[@class="button next"]/@href').get()
        if next_page is not None:
            url = response.urljoin(next_page)
            request = scrapy.Request(url=url, callback=self.parse_all_articles)
            request.meta['categorie'] = categorie
            request.meta['guitar_type'] = guitar_type 
            yield request

    # Artikeldetail
    def parse_article_page(self, response):
        """ In dieser Parsefunktion werden die Details zu einem Artikel extrahiert.
        """
        guitar = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//div[@class="prod-pricebox-price"]//span[@itemprop="price"]/text()').extract_first()

        # Zusatzinformationen zu den Artikeln, werden als dict in Zelle gespeichert und nicht jetzt schon extra aufgeschlüsselt, 
        # da sich diese innerhalb der verschiedenen Kategorien unterscheiden können
        kf_descriptions = response.xpath('//div[@class="rs-prod-keyfeatures"]//table//th/text()').extract()
        kf_values = response.xpath('//div[@class="rs-prod-keyfeatures"]//table//td/text()').extract()

        key_features = dict(zip(kf_descriptions,kf_values))
        
        # lade Metas
        categorie = response.meta.get("categorie")
        guitar_type = response.meta.get("guitar_type")
        manufacturer = response.meta.get("manufacturer")

        # wenn mehrere Reviews existieren, gehe zu "Alle Bewertungen lesen" Seite
        multi_reviews = response.xpath('//*[text() = "Alle Bewertungen lesen"]/@href').get()
        
        if multi_reviews is not None:
                request = scrapy.Request(multi_reviews, callback=self.parse_reviews)
                # speichere informationen als meta um sie in der nächsten Funktion verwenden zu können
                request.meta['categorie'] = categorie
                request.meta['guitar_type'] = guitar_type
                request.meta['guitar'] = guitar
                request.meta['price'] = price
                request.meta['manufacturer'] = manufacturer
                request.meta['key_features'] = key_features
                yield request

    # REVIEW SEITE
    def parse_reviews(self, response):
        """ Diese Funktion kümmert sich um das Parsen der großen Bewertungsseite, welche alle Bewertungen zu einem Artikel anzeigt
        """
     
        item = ThomannItem()

        # lade Metas
        categorie = response.meta.get("categorie")
        guitar_type = response.meta.get("guitar_type")
        guitar = response.meta.get("guitar")
        price = response.meta.get("price")
        manufacturer = response.meta.get("manufacturer")
        key_features = response.meta.get("key_features")

        # falls alle vorkommenden Bewertungen uebersetzt sind werden diese nicht mit einbezogen (da schlechte Qualität)
        # https://www.thomann.de/de/esp_e_ii_viper_baritone_chms_reviews.htm wird jetzt nicht mehr aufgenommen
        count_all_comments = len(response.xpath('//div[contains(@class,"rs-prod review textrating-no")]'))
        count_foreign_comments = len(response.xpath('//div[@class="autotranslate clearfix"]'))

        if  count_all_comments != count_foreign_comments :
            # REVIEWEBENE: Schleife über die verschiedenen Reviews
            for sel in response.xpath('//div[contains(@class,"rs-prod review textrating-no")]'):
                author = sel.xpath('.//div[@class="author"]/text()').extract()
                review_text = sel.xpath('.//div[@class="inner js-replace-text"]/text()').extract()
                stars = sel.xpath('.//div[@class="review-widget"]//span[@class="rs-stars skin-small "]/span[@class="overlay-wrapper"]/@style')

                item["categorie"] = categorie
                item["guitar_type"] = guitar_type
                item["guitar"] = guitar
                item["price"] = price
                item["manufacturer"] = manufacturer
                item["author"] = author
                item["review"] = review_text
                item["key_features"] = key_features
                # Auf harte weise gelernt, dass einzelne Bewertungen doch keine Pflichfelder sind
                # https://www.thomann.de/de/harley_benton_kahuna_clu_bass_ukulele_fl_reviews.htm
                try:
                    item["stars_gesamt"] = stars[0].re('[.0-9]+')
                except IndexError:
                    item["stars_gesamt"] = np.nan
                try:
                    item["stars_features"] = stars[1].re('[.0-9]+')
                except IndexError:
                    item["stars_features"] = np.nan
                try:
                    item["stars_sound"] = stars[2].re('[.0-9]+')
                except IndexError:
                    item["stars_sound"] = np.nan
                try:
                    item["stars_verarbeitung"] = stars[3].re('[.0-9]+')
                except IndexError:
                    item["stars_verarbeitung"] = np.nan
                
                yield item
            # ist stabiler als der nach vorne Pfeil
            next_page_check = response.xpath('//*[text() = "Mehr anzeigen"]').get()
            if next_page_check is not None:

                current_page = int(response.xpath('//span[@class="current page rs-btn"]/text()').extract_first())
                art_nr = response.xpath('//div[@class="reviews-list"]//*[@name="ar"]/@value').extract_first()
                addition = "?ar=" + art_nr + "&page=" + str(current_page + 1) + "&order=0&rating=0&reviewlang%5B%5D=1"
                url = response.urljoin(addition)
                
                request = scrapy.Request(url, callback=self.parse_reviews)
                # setzte Meta erneut, da diese bei erneutem Funktionsaufruf "vergessen" werden
                request.meta['categorie'] = categorie
                request.meta['guitar_type'] = guitar_type
                request.meta['guitar'] = guitar
                request.meta['price'] = price
                request.meta['manufacturer'] = manufacturer
                request.meta['key_features'] = key_features

                yield request

        
    




