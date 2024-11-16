import requests
from lxml import etree
import yaml



url = r'https://nodefree.org/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

res = requests.get(url=url, headers=headers)
et = etree.HTML(res.text)
detail_urls = et.xpath('//*[@id="wrap"]//li[1]//h2/a/@href')[0] or None
print(detail_urls)

if detail_urls:
    detail_res = requests.get(url=detail_urls, headers=headers)
    detail_et = etree.HTML(detail_res.text)
    final_url = detail_et.xpath('//div[@class="section"]/p[2]/text()')[0] or None
    print(final_url)
    if final_url:
        clash_detail = requests.get(url=final_url, headers=headers)
        with open('./tmp.yaml', 'wb') as f:
            f.write(clash_detail.content)
    else:
        with open('./tmp.yaml', 'w', encoding='utf-8') as f:
            f.write('error: do not get any information')


