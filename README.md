#資料爬蟲
    選擇三個巴哈姆特前10大主題討論串進行評論爬蟲，在這邊使用手動HEADERS，因為巴哈姆特擁
    有反爬蟲的機制，需特別製作HEADERS才能獲取資料。
```py
bsn_links =['60030', '60001', '60559'] bsn_categories=['電腦應用綜合討論', '電視遊樂器綜合討論', '智慧型手機'] base_url = 'https://forum.gamer.com.tw/' HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36', }
```