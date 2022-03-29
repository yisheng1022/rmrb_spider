import random,time,os,pickle,json,requests,re
from bs4 import BeautifulSoup as BS
import pandas as pd
import datetime

def get_all_paper(input_date):
	all_news_url = []
	target_paper = "http://paper.people.com.cn/rmrb/html/{}/{}/nbs.D110000renmrb_01.htm".format(input_date.split(" ")[0],input_date.split(" ")[1])
	# print(target_paper)
	first_ban = requests.get(target_paper)
	first_ban.encoding = "utf-8"
	first_source = BS(first_ban.text,"html.parser")
	ban_num = first_source.select("div.swiper-container div.swiper-slide a#pageLink")
	first_ban.close()
	ban_count = 1
	for no_ban in ban_num:
		one_ban = "http://paper.people.com.cn/rmrb/html/{}/{}/{}".format(input_date.split(" ")[0],input_date.split(" ")[1],no_ban["href"].replace("./",""))
		print("Now at ban No.",ban_count)
		many_news = requests.get(one_ban)
		many_news.encoding = "utf-8"
		many_source = BS(many_news.text,"html.parser")
		news_url_raw = many_source.select("ul.news-list li a")
		for news_url in news_url_raw:
			one_news = "http://paper.people.com.cn/rmrb/html/{}/{}/{}".format(input_date.split(" ")[0],input_date.split(" ")[1],news_url["href"])
			all_news_url.append(one_news)
		many_news.close()
		time.sleep(random.randint(5,7))
		ban_count += 1
	return all_news_url


def get_each_news(news_list):
	url_l,date_l,page_l,ban_l,aut_l,tit_l,content_l = list(),list(),list(),list(),list(),list(),list()
	for one_news_url in news_list:
		print("Now at:",one_news_url)
		one_news_req = requests.get(one_news_url)
		one_news_req.encoding = "utf-8"
		one_source = BS(one_news_req.text,"html.parser")

		date_raw = one_source.select("div.date-box p.date.left")
		page_raw = one_source.select("div.paper-bot p.left.ban")
		aut_raw = one_source.select("div.article p.sec")
		tit_raw = one_source.select("h1")
		cont_raw = one_source.select("div#ozoom")

		url_l.append(one_news_url)  #網址

		if len(date_raw) > 0:  #日期
			clean_date = re.sub(r'\s+',"",date_raw[0].text).split("星")[0].split("报")[1].replace("年","-").replace("月","-").replace("日","")
			date_l.append(clean_date)

		if len(page_raw) > 0:  #版&版名
			clean_page = int(page_raw[0].text.split(":")[0].replace("第","").replace("版",""))
			clean_ban = page_raw[0].text.split(":")[1]
			ban_l.append(clean_ban)
			page_l.append(str(clean_page))

		if len(aut_raw) > 0:  #作者
			clean_aut = re.sub(r'\s+',"",aut_raw[0].text.split("《")[0])
			if clean_aut != "":
				aut_l.append(clean_aut)
			else:
				clean_aut = "No"
				aut_l.append(clean_aut)

		if len(tit_raw) > 0:  #標題
			tit_l.append(tit_raw[0].text)

		if len(cont_raw) > 0:
			clean_cont = re.sub(r'\s+',"",cont_raw[0].text)
			content_l.append(clean_cont)
		time.sleep(random.randint(3,7))

	return url_l,date_l,page_l,ban_l,aut_l,tit_l,content_l	



def main(Today_is = "2022/03 23"):
	today_is = Today_is
	os.system("cls")
	print("Now processing: ",Today_is)
	all_news_list = get_all_paper(today_is)
	print("Done Fetching news' url\n----------")
	print("Wait to start getting news info")
	time.sleep(random.randint(10,20))
	os.system("cls")
	url_l,date_l,page_l,ban_l,aut_l,tit_l,content_l = get_each_news(all_news_list)
	news_pd = pd.DataFrame()
	news_pd["GUID"] = url_l;news_pd["date"] = date_l;news_pd["page"] = page_l;news_pd["ban_name"] = ban_l;news_pd["author"] = aut_l
	news_pd["title"] = tit_l;news_pd["content"] = content_l


	if os.path.isfile(str(today_is).replace("-","").replace(" ","")+".csv"):
		news_pd.to_csv(str(today_is).replace("-","").replace(" ","")+".csv",mode = "a+",index = False,header = False,encoding = "utf-8")
	else:
		news_pd.to_csv(str(today_is).replace("-","").replace(" ","")+".csv",mode = "a+",index = False,header = True,encoding = "utf-8")

def date_creater(date_start = None,date_end = None):
	if date_start is None:
		datestart = '2021-12-31'
	if date_end is None:
		date_end = datetime.datetime.now().strftime('%Y%m%d')

	date_start = datetime.datetime.strptime(date_start,'%Y%m%d')
	date_end = datetime.datetime.strptime(date_end,'%Y%m%d')
	date_list = []
	while date_start < date_end:
		date_list.append(date_start.strftime('%Y-%m %d'))
		date_start += datetime.timedelta(days=+1)
	date_list.append(date_end.strftime('%Y-%m %d'))
	return date_list
		


print("★★★★★Welcome to RMRB fetching program.★★★★★")
print("Please choose which function would u like to execute.(1:Today's news 2:Past news")
old_new = input("Function: ")
if old_new == "1":
	main(datetime.datetime.now().strftime('%Y-%m %d'))
elif old_new == "2":
	old_day = input("Plz input which day you want to catch (format:20220101):")
	old_day = time.strptime(old_day,'%Y%m%d')
	old_day = time.strftime('%Y-%m %d',old_day)
	main(old_new,old_day)
elif old_new == "3":
	start_from = input("Start from:")
	end_at = input("End at:")
	day_list = date_creater(start_from,end_at)
	for day_day in day_list:
		main(day_day)
		time.sleep(random.randint(30,60))
