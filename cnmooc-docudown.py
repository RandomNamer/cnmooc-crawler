'''
How to use cnmooc DocuScraper:
step I: Download and install Chrome extension "EditThisCookie"  Link: https://chrome.google.com/webstore/detail/editthiscookie
step II: Login to cnmooc.org, copy the site link of the course you want to scrap and paste it to variable "nav_page".
step III: use EditThisCookie to export all cookies to clipboard
step IV: run this python utility, you may install these dependency python packages first.
  简言之，将变量nav_page的值改为课程导航页链接->复制cookies（如果使用上述工具导出，则用函数import_cookie_from_json解析，也可手动修改cookie的键值->运行后会将文件链接导入剪贴板，大家可以按需下载（以后会有下载并重命名功能）。可能需要pip安装下列库。
'''

import requests
import re
from bs4 import BeautifulSoup
import clipboard
import json
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}

nav_page = 'https://www.cnmooc.org/portal/session/unitNavigation/13311.mooc'

#cookie = 'moocvk=03eeb7ac49c8436282903c24f7f2e16b; moocsk=0b7e512631f546a5a69133f00f72a37f; JSESSIONID=E76BD7D01001E12B41A3C466AA29AF9B.tomcat-host1-1; Hm_lvt_ed399044071fc36c6b711fa9d81c2d1c=1571238986,1571238997,1571369492,1571369507; Hm_lpvt_ed399044071fc36c6b711fa9d81c2d1c=1571409177; BEC=f6c42c24d0c76e7acea242791ab87e34|1571409176|1571369491'
res_links = []
itemid = []
titles = []

'''    
def extract_cookies(cookie):
    
   cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
   return cookies
cookies=extract_cookies(cookie)
'''
def import_cookie_from_json(raw):
    raw=raw.replace('[\n',''); raw=raw.replace(']','');raw=raw.replace(',\n',',');raw=raw.replace('{\n','{');raw=raw.replace('\n}','}')
    #raw=raw.replace('[',''); raw=raw.replace(']','');raw=raw.replace('"{',"{");raw=raw.replace('}"',"}");raw=raw.replace('\\"','"')
    json_list=raw.split("},")
    data=[]
    c=0;
    for entry in json_list:
        if c<9: entry=entry+'}'
        print(entry)
        try:
             data.append(json.loads(entry))
        except json.JSONDecodeError:
            print("Error processing json #")
        else:
            print("json read.")
        c=c+1
    cookies={};
    for item in data:
        name=item["name"]
        value=item["value"]
        cookies[name]=value
    return cookies

cookies=import_cookie_from_json(clipboard.paste())


def get_all_links(cookies):
    s = requests.session()
    r = s.get(nav_page, headers=headers, cookies=cookies)
    html = r.text
    soup = BeautifulSoup(html)
    a = soup.find_all('a', "lecture-action linkPlay", title=re.compile("pdf"))
    
    for item in a:
        itemid.append(item['itemid'])
        titles.append(item['title'])
    return itemid, titles

get_all_links(cookies)


def get_resource_links(cookies, unitid):
    url = 'https://cnmooc.org/study/play.mooc'
    base = 'https://cnmooc.org'
    c=-1
    for id in unitid:
        c=c+1
        data = {'itemId': id, 'itemType': '20', 'testPaperId':''}
        s = requests.session()
        r = s.post(url, data, cookies=cookies)
        try:
            res_links.append(base + re.search('/repositry/.*\.pdf',r.text).group())
            print("successfully got the link of ")
            print(titles[c])
        except AttributeError:
            print("not found")
    return res_links

get_resource_links(cookies, itemid)

def CopyToClipboard(res_links):
    cnt=-1;
    b=""
    c=""
    for title in titles:
        cnt=cnt+1
        c=c+res_links[cnt]+'\n'
        a=title+':'+res_links[cnt]
        b=b+a+'\n'
    clipboard.copy(b)
    return b
    #b is the list with both links and their corresponding file name attached ahead, which can't be parsed by download tools.
    #c is the list with only links, which is download-ready. You may disable multi-thread downloading to ensure all files in right chronological order. 
b=CopyToClipboard(res_links)
print("Links copied to clipboard.You can download all of them using third-party tools. ")
print(" ")
print(b)
