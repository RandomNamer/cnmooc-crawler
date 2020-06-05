# cnmooc-crawler
Scraping course resources of cnmooc.org
## How to use cnmooc DocuScraper:
- Download and install Chrome extension "EditThisCookie"  Link: https://chrome.google.com/webstore/detail/editthiscookie
- Login to cnmooc.org, copy the site link of the course you want to scrap and paste it to variable "nav_page".
- Use EditThisCookie to export all cookies to clipboard
- Run this python utility, you may install these dependency python packages first.
 ### 简言之，将变量nav_page的值改为课程导航页链接->复制cookies（如果使用上述工具导出，则用函数import_cookie_from_json解析，也可手动修改cookie的键值->运行后会将文件链接导入剪贴板，按需下载
