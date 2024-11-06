import requests
from lxml import etree

url = r'https://clashgithub.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

res = requests.get(url=url, headers=headers)
et = etree.HTML(res.text)
detail_urls = et.xpath('//*[@id="posts"]/div[1]//h3/a/@href')[0] or None
print(detail_urls)

if detail_urls:
    detail_res = requests.get(url=detail_urls, headers=headers)
    detail_et = etree.HTML(detail_res.text)
    final_url = detail_et.xpath('//p[strong="clash订阅链接:"]/following-sibling::p[1]/text()')[0] or None
    if final_url:
        clash_detail = requests.get(url=final_url, headers=headers)
        with open('./tmp.yaml', 'wb') as f:
            f.write(clash_detail.content)
    else:
        with open('./tmp.yaml', 'w', encoding='utf-8') as f:
            f.write('error: do not get any information')
