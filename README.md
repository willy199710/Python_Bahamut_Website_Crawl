# 資料爬蟲
    選擇三個巴哈姆特前10大主題討論串進行評論爬蟲，在這邊使用手動HEADERS，因為巴哈姆特擁
有反爬蟲的機制，需特別製作HEADERS才能獲取資料。
```py
bsn_links =['60030', '60001', '60559'] 
bsn_categories=['電腦應用綜合討論', '電視遊樂器綜合討論', '智慧型手機'] 
base_url = 'https://forum.gamer.com.tw/' 
HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36', }
```
## 獲取評論資料
    在此我選擇擷取主題評論串第一頁的所有討論串，並獲取那個討論串內所有的評論。
    若該討論串內有47頁，則會爬取這47頁所有的評論內容。

```py
def get_article_url_list(forum_url): 
    r = requests.get(forum_url, headers=HEADERS) 
    if r.status_code != requests.codes.ok: 
        print("載入失敗") 
        return []

    article_url_list = [] 
    soup = BeautifulSoup(r.text,'lxml') 
    item_blocks = soup.select('table.b-list > tr[class="b-list__row b-list-item b-imglist-item"]') 
    for item_block in item_blocks:
        title_block = item_block.select_one('.b-list__main__title') 
        article_url = f"https://forum.gamer.com.tw/{title_block.get('href')}" article_url_list.append(article_url) 

    return article_url_list 

def get_article_total_page(soup): 
    article_total_page = soup.select_one('.BH-pagebtnA > a:last-of-type').text return int(article_total_page)   

#主題頁面資訊 
def get_article_info(article_url): 
    soup = BeautifulSoup(requests.get(article_url, headers=HEADERS).text,'lxml')
    article_title = soup.select_one('h1.c-post__header__title').text
    article_total_page = get_article_total_page(soup) #獲得總樓層的數量
    reply_info_list = [] 
    for page in range(article_total_page): 
        crawler_url = f"{article_url}&page={page + 1}" reply_list = get_reply_info_list(crawler_url) reply_info_list.extend(reply_list) random.uniform(1, 3)
        article_info = { 
            'title': article_title,
            'url': article_url, 
            'reply': reply_info_list[0], 
            'category': category 
        } 
        return article_info

def get_reply_info_list(url): 
    reply_info_list = [] 
    soup = BeautifulSoup(requests.get(url, headers=HEADERS).text,'lxml') reply_blocks = soup.select('section[id^="post_"]') 
    for reply_block in reply_blocks: 
        reply_info = reply_block.select_one('.c-article__content').text reply_info = re.sub(r'\n+',"", reply_info) 
        reply_info_list.append(reply_info) 
    return reply_info_list
```

## 資料內容
    我使用dataframe來存取資料，相關爬取的內容如下
