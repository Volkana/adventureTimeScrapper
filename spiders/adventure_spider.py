import scrapy
import w3lib.html

class adventureSpider(scrapy.Spider):
    name= "adventureTime"
    base_url = "https://adventuretime.fandom.com"
    def start_requests(self):
        urls = [
            "/wiki/Category:Transcripts",
        ]
        for url in urls:
            yield scrapy.Request(
                    url=self.base_url + url, 
                    callback=self.get_links
                )

    def get_links(self, response):
        all_links = sorted(set(response.xpath('//a[contains(@href, "/Transcript")]/@href').getall()))
        for num, link in enumerate(all_links):
            yield scrapy.Request(url= self.base_url + link, callback=self.parse_transcript, meta={"number": str(num)}) 

    def parse_transcript(self, response):
        num = response.meta["number"]
        # Retorna os transcritos inteiros, sem separar personagem da fala
        title = response.xpath('//title/text()').getall()[0].split("|")[0]
        all_transcripts = response.xpath('//dd').getall()
        '''
        yield {
            "title": title,
            "transcript": all_transcripts
        }
        '''
        filename = 'transcript- %s.txt' %num
        with open(filename, 'w') as f:
            f.write(title + "\n")
            for transcript in all_transcripts:
                transcript = w3lib.html.remove_tags(transcript)
                transcript = f.write(transcript)
        self.log('terminado')

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'teste-34.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
