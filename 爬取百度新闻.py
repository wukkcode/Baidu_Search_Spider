'''
新闻关键词每一页有10条新闻
每一页网页的格式相同对每一页采取相同的解析方式即可


网页数据比较复杂，我是用re正则解析

'''
import re
from selenium import webdriver
import pymysql

browser = webdriver.Chrome()


db = pymysql.connect(host='localhost',
                     user='root',
                     db='python_spider',
                     password='2019',
                     port=3306,
                     charset='utf8')

cursor = db.cursor()



def get_baidu(keyword, page_num):
    search_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word={}&pn={}'.format(
        keyword, page_num)
    # print(search_url)
    browser.get(search_url)
    return browser.page_source


def analyze_target(target_page):
    target_re = re.compile(
        '<div.*?id="(\d+)".*?>.*?c-title">.*?href="(.*?)".*?_blank">(.*?)<em>(.*?)</em>(.*?)</a>.*?c-author">(.*?)</p>(.*?)<span',
        re.S)
    target_list = re.findall(target_re, target_page)
    return target_list


def main():
    num = 0
    keyword = input('请输入关键词：')
    page_num = int(input('请输入页数：')) * 10
    for page in range(0, page_num, 10):
        target_page = get_baidu(keyword, page)
        for target_tuple in analyze_target(target_page):
            # print(target_tuple)
            news_id = target_tuple[0]
            news_url = target_tuple[1]
            news_title = (target_tuple[2]+target_tuple[3]+target_tuple[4]).replace('\n', '').replace(' ', '')
            # print(news_title)
            news_from = target_tuple[5].replace('\n', '').replace('"', '').replace('\t', '').replace('<img class=source-icon src=', '').replace('alt=>', '').replace('&nbsp;', '').replace(' ', '')[0:-16]
            news_time = target_tuple[5].replace('\n', '').replace('"', '').replace('\t', '').replace('<img class=source-icon src=', '').replace('alt=>', '').replace('&nbsp;', '').replace(' ', '')[-16:]
            #print(news_from, news_time)
            some_string = '</div><style>.se_com_irregular_gallery{position:relative;margin-bottom:2px}.se_com_irregular_galleryli{display:inline}.se_com_irregular_gallerya{display:inline-block;line-height:0}.se_com_irregular_galleryliimg{height:91px;}.se_com_irregular_galleryspan{position:absolute;left:0;top:0;}.se_com_irregular_gallery_linkhover{box-shadow:rgb(100,100,100)0010px;z-index:1;display:none;position:absolute;overflow:hidden;}.se_com_irregular_gallery_linkhovera{float:none;}.se_com_irregular_gallery_linkhoveraimg.op_realtime_image_img{width:100%;height:100%}</style><divclass="se_com_irregular_galleryc-gap-top-small"><ul><li><ahref="http://news.xinhuanet.com/talking/character/2019101604.htm"target="_blank"><imgsrc="https://dss0.baidu.com/73x1bjeh1BF3odCf/it/u=1481399992,1459304726&amp;fm=85&amp;s=B222C1A74E433CD660A549360300C040"title=""></a></li><li><ahref="http://news.xinhuanet.com/talking/character/2019101604.htm"target="_blank"><imgsrc="https://dss0.baidu.com/73x1bjeh1BF3odCf/it/u=2161983766,569181649&amp;fm=85&amp;s=B200DC4F8678219610ECCC2B0300A053"title=""></a></li><listyle="padding-right:0"><ahref="http://news.xinhuanet.com/talking/character/2019101604.htm"target="_blank"><imgsrc="https://dss0.baidu.com/73x1bjeh1BF3odCf/it/u=2986282615,1714790650&amp;fm=85&amp;s=F83A0CD70E72109610B4CC370300F044"title=""></a></li></ul><divclass="se_com_irregular_gallery_linkhover"target="_blank"></div></div>'
            news_content = target_tuple[6].replace('\n', '').replace(' ', '').replace('<em>', '').replace('</em>', '').replace('\t', '').replace(some_string, '').replace('\\', '').replace("'", '')
            print(news_title)
            cursor.execute("INSERT INTO spider2 VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(news_id, news_url, news_title, news_from, news_time, news_content))
            num += 1;
            print('总共插入{}条数据'.format(num))
            db.commit()
            
        
if __name__ == '__main__':
    main()
