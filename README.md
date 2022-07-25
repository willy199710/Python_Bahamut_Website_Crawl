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

  在此我選擇擷取主題評論串第一頁的所有討論串，並獲取那個討論串內所有的評論。若該討論串內有47頁，則會爬取這47頁所有的評論內容。

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
![Github](https://github.com/willy199710/Python_Bahamut_Website_Crawl/blob/main/pic/pic1.JPG "爬蟲資料內容")

## 資料前處理

  在這邊我使用CkipLab進行資料前處理，對評論內容進行分詞斷句(tokens)並計算字詞的頻繁出現次數(freq)，freq可呈現出最常出現的字詞為何
![Github](https://github.com/willy199710/Python_Bahamut_Website_Crawl/blob/main/pic/pic2.JPG "資料內容")
    
  相關CkipLab程式碼如下所示:
```py
wd = os.getcwd()

model_path = wd + '\ckiplab-model-data'

ws = WS(model_path)
pos = POS(model_path)
ner = NER(model_path)
category_freq = []
word = []


pattern = re.compile(r'[\u4e00-\u9fa5]+')

tokens = ws(df.content)
tokens_list = []
tokens_str = []
drops = []

for idx,line in enumerate(tokens):
    # 刪除不屬於中文字元、標點符號、特殊符號、英文、與數字
    line_list = [x for x in line if pattern.match(x)]
    line_str = " ".join(line_list) # 合併成字串 以空格分隔
    # 過濾之後，有些留言可能會變成空值 需要進一步刪除該筆
    if len(line_str)==0:
        #print(idx, ':skip a blank line跳開這筆空白內容')
        drops.append(idx)
        continue
    tokens_list.append(line_list)
    tokens_str.append(line_str)

tokens_pos = pos(tokens_list)

word_pos_pair = [list(zip(w,p)) for w, p in zip(tokens_list, tokens_pos)]

with open('stops_chinese_traditional.txt', 'r', encoding='utf8') as f:
    stops = f.read().split('\n') 

allowPOS=['Na','Nb','Nc','VA','VAC','VB','VC']

tokens_v2 =[]
for wp in word_pos_pair:
    tokens_v2.append([w for w,p in wp if w not in stops and (len(w) >= 2) and p in allowPOS])

tokens_pos = pos(tokens_v2)
word_pos_pair = [list(zip(w,p)) for w, p in zip(tokens_v2, tokens_pos)]
entity_list = ner(tokens_v2, tokens_pos)

category_freq = []
for wp in word_pos_pair:
    keyfreqs =[]
    filtered_words =[]
    word_frequency(wp)
    counter = Counter(filtered_words)
    keyfreqs.append(counter.most_common(200))
    category_freq.append(keyfreqs[0])

data = zip(commentDate, categories, contents, classifies, tokens_list, tokens_str, category_freq, entity_list, word_pos_pair)
df2 = pd.DataFrame(list(data), columns=['date', 'category', 'content', 'classify', 'tokens', 'tokens_str', 'freq', 'entities', 'token_pos'])


df2.head(5)
```