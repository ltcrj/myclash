from urllib.parse import urljoin
import requests
from lxml import etree



url = r'https://free.datiya.com'
res = requests.get(url)
et = etree.HTML(res.text)
tail_url = et.xpath('//section[1]/div[1]//h1/a/@href')[0] or None

if tail_url:
    full_url = urljoin(url, tail_url)
    sub_res = requests.get(full_url)
    sub_et = etree.HTML(sub_res.text)
    sub_url = sub_et.xpath('//pre[1]/code/text()')[0] or None
    if sub_url:
        result = requests.get(sub_url)
        with open('./tmp.yaml', 'wb') as f:
            f.write(result.content)
    else:
        with open('./tmp.yaml', 'w', encoding='utf-8') as f:
            f.write('error: do not get any information')
