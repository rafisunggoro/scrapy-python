import scrapy
import json

class SpiderprojectSpider(scrapy.Spider):
    name = "spiderproject"
    allowed_domains = ['searchcareers.stghavaspeople.com']

    def start_requests(self):
        yield scrapy.Request(
            url = f'https://searchcareers.stghavaspeople.com/umbraco/api/jobsearchapi/getoracledata/?nodeId=6789&page=1&franchisejobactivity=job-result&site=%2Fen&internaljobs=False',
            method='GET',
            callback=self.parse
        )

    def parse(self, response):          
        respon = json.loads(response.body)
        job = respon.get('jobs')
        page = respon.get('page')

        for jobs in job:
            if job:
                yield {
                    'Title': jobs.get('title'),
                    'URL': jobs.get('applyUrl'),
                    'Location': jobs.get('location')
                }

        if job: 
            page += 1
            yield scrapy.Request(
                url = f'https://searchcareers.stghavaspeople.com/umbraco/api/jobsearchapi/getoracledata/?nodeId=6789&page={page}&franchisejobactivity=job-result&site=%2Fen&internaljobs=False',
                method='GET',
                callback=self.parse
            )