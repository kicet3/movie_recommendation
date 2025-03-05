import numpy as np 
import pandas as pd
import json
import openpyxl
import os
import re
import requests
from collections import OrderedDict

movie_list = range(0,100000)
api_key=''
movie = "https://api.themoviedb.org/3/movie/{movies}?api_key={key}"
movie_review = "https://api.themoviedb.org/3/movie/{movies}/reviews?api_key={key}"

class Default(dict):
	def __missing__(self,key):
		return key
#api = "https://api.themoviedb.org/3/movie/550?api_key="+api_key
result_movie = []
result_rating = []
for name in movie_list:
	try:
		url1=movie.format_map(Default(movies=name,key=api_key))
		r1 = requests.get(url1)
		data1 = json.loads(r1.text)
		url2=movie_review.format_map(Default(movies=name,key=api_key))
		r2 = requests.get(url2)
		data2 = json.loads(r2.text)
		print("==============================================================================================")
		result_movie.append((data1["original_title"],data1["genres"]))
		try:
			for i in range(100):
				result_rating.append((data1["original_title"],data2["results"][i]["author_details"]["username"],data2["results"][i]["author_details"]["rating"]))
				print("유저 이름 :",data2["results"][i]["author_details"]["username"])
				print("영화 평점 :",data2["results"][i]["author_details"]["rating"])
		except:
			print("영화 "+data1["original_title"]+" 평점 데이터 없음")
	except:
		print("영화 번호 "+str(name)+"에 데이터 없음")

movie_data = pd.DataFrame(result_movie,columns=['original_title','Genres'])
rating_data = pd.DataFrame(result_rating,columns=['original_title','Username','rating'])

try:
	movie_data.to_excel('new dataset/movie.xlsx')
	rating_data.to_excel('new dataset/movie rating.xlsx')
	print("영화 데이터 저장 성공")
except:
	print("데이터 저장 실패")

#pd.DataFrame(recommend_result, columns = ['Title', 'Correlation', 'Genre'])
