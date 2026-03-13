from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup
import re
import pandas as pd
SMCI = "C:\\Users\\adams\\Python Projects\\sec-edgar-filings\\SMCI\\10-K\\0001193125-07-190775\\full-submission.txt"
email = "adamsheb414@gmail.com"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

#dl = Downloader(email,user_agent)
#dl.get("10-K", "SMCI")

with open(SMCI, "r", encoding = "utf-8") as file:
    soup = BeautifulSoup(file,'html.parser')
    
text = soup.get_text()

item_1 = re.search(r'Item\s1\.\s+Business(.*?)Item\s1A\.', text, re.DOTALL | re.IGNORECASE)

if item_1:
    item_1_text = item_1.group(1).strip()
    print("Item 1 Text:")
    print(item_1_text)
