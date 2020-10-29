import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from searcher.trzpiders.trzpiders.items import TrzpidersItem

class GezatekSpider(CrawlSpider):
    """
        Spider que recolecta datos de la pagina www.gezatek.com.ar
    """
    name = 'gezatek' # Nombre de la araña
    custom_settings = {'FEEDS': {'gezatek.csv': {'format': 'csv'}}} # Forma de exportar los datos recolectados
    allowed_domains = ['www.gezatek.com.ar'] # Dominio que manejamos, del cual no puede salir
    # TODO: Hacer que reciba la palabra a buscar y la reemplace al final
    start_urls = ['https://www.gezatek.com.ar/tienda/?busqueda=nvidia'] # URL donde extraemos los datos
    # Reglas que debera respetar la spider
    rules = {
        # Entra en cada item (para extraer los datos) y luego vuelve a la pagina de extraccion
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="w-box product "]')),
             callback='parse_item', follow=False)
    }
    # En el caso de existir el archivo, lo elimina
    try:
        os.remove('gezatek.csv')
    except OSError:
        pass

    def parse_item(self, response):
        """
            Recolecta la informacion de cada item
        """
        item = TrzpidersItem()
        item['title'] = str(response.css(
            '.nombre h3::text').extract_first()).strip()
        item['price'] = str(response.css(
            '.precio_web h7::text').extract_first()).strip()
        item['category'] = str(response.css(
            '.col-md-5 h7::text').extract_first()).capitalize().strip()
        item['link'] = str(response.url)
        yield item

    def turn_on_spider(self):
        """
            Enciende el spider
        """
        process = CrawlerProcess(
            {'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
        process.crawl(GezatekSpider)
        process.start()