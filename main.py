import requests
from lxml import etree
import yaml


def remove_ss_type_entries(yaml_text):
    # 将 YAML 格式的文本加载为 Python 对象
    data = yaml.safe_load(yaml_text)

    # 过滤掉包含 "type: ss" 的代理条目
    if "proxies" in data:
        data["proxies"] = [proxy for proxy in data["proxies"] if proxy.get("type") != "ss"]

    # 将过滤后的数据转换回 YAML 格式文本
    return yaml.safe_dump(data, allow_unicode=True)

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
        result = remove_ss_type_entries(clash_detail.text)
        with open('./tmp.yaml', 'w') as f:
            f.write(result)
    else:
        with open('./tmp.yaml', 'w', encoding='utf-8') as f:
            f.write('error: do not get any information')


