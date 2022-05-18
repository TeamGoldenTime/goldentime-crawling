from asyncore import write
from parse import *
from csv import writer
from turtle import reset
import requests
from bs4 import BeautifulSoup
import pandas as pd 
dataset = [] 

for i in range (1,457):
    res = requests.get("https://www.animal.go.kr/front/awtis/protection/protectionList.do?totalCount=4560&pageSize=10&boardId=&desertionNo=&menuNo=1000000060&searchSDate=2022-04-18&searchEDate=2022-05-18&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=417000&searchKindCd=&searchSexCd=&&page=" + str(i))
    bsObject = BeautifulSoup(res.content, 'html.parser')
            
    img_url =  bsObject.select('div > ul > li > div > div > a')
    post_num = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(1)>dd')
    date = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(2)>dd')
    kind = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(3)>dd')
    gender = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(4)>dd')
    place = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(5)>dd')
    remark = bsObject.select('ul:nth-child(2)>li>div:nth-child(2)>dl:nth-child(6)>dd')
    detail_link = bsObject.select('div > ul > li > div > a')

    detail_links = []
    for link in detail_link :
        result = parse("javascript:moveUrl('{}');", link["onclick"])
        #print(result[0])
        detail_links.append(result[0])

    for url, pnum, date, kind, gen, place, remark, link in zip( img_url, post_num, date, kind, gender, place, remark, detail_links):
        dataset.append(["https://www.animal.go.kr" + url["href"], pnum.text, date.text, kind.text, gen.text, place.text, remark.text, "https://www.animal.go.kr/front/awtis/protection/protectionDtl.do?desertionNo=" + link])
        #print("https://www.animal.go.kr" + url["src"], pnum.text, date.text, kind.text, gen.text, place.text, remark.text, "https://www.animal.go.kr/front/awtis/protection/protectionDtl.do?desertionNo=" + link)
        df = pd.DataFrame(dataset, columns=["경로","공고번호","접수일자", "품종", "성별", "분실장소", "특징", "상세링크"])
        df.to_csv('dog.csv', index=False, encoding="utf-8-sig")