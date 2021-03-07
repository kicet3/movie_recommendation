import numpy as np 
import pandas as pd
import json
import openpyxl
import os
import tensorflow as tf
import re
from collections import OrderedDict

meta = pd.read_csv('new dataset/movie.csv',low_memory=False,error_bad_lines=True,dtype={'CODE':np.str})
print('영화 데이터 읽어오기 성공')


meta = meta[['original_title','Genres']]

ratings = pd.read_csv('new dataset/movie rating.csv',low_memory=False)
print('평점 데이터 읽어오기 성공')
ratings = ratings[['original_title', 'Username', 'rating']]
ratings.describe()


def parse_genres(genres_str):
	genres = json.loads(genres_str.replace('\'', '"'))
    
	genres_list = []
	for g in genres:
		genres_list.append(g['name'])

	return genres_list

meta['Genres'] = meta['Genres'].apply(parse_genres)
data = pd.merge(ratings, meta, on='original_title', how='inner')
matrix = data.pivot_table(index='Username', columns='original_title', values='rating')
GENRE_WEIGHT = 0.1

def pearsonR(s1, s2):
	s1_c = s1 - s1.mean()
	s2_c = s2 - s2.mean()
	return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

def recommend(input_movie, matrix, n, similar_genre=True):
	input_genres = meta[meta['original_title'].str.lower() == input_movie.lower()]['Genres'].iloc(0)[0]
	result = []
	for title in matrix.columns:
		if title == input_movie:
			continue
        # rating comparison
		cor = pearsonR(matrix[input_movie], matrix[title])
        
        # genre comparison
		if similar_genre and len(input_genres) > 0:
			temp_genres = meta[meta['original_title'] == title]['Genres'].iloc(0)[0]

			same_count = np.sum(np.isin(input_genres, temp_genres))
			cor += (GENRE_WEIGHT * same_count)
        
		if np.isnan(cor):
			continue
		else:
			result.append((title, '{:.2f}'.format(cor), temp_genres))
            
	result.sort(key=lambda r: r[1], reverse=True)

	return result[:n]


if __name__ == "__main__":
	recommend_result = recommend('The Dark Knight', matrix, 10, similar_genre=True)
	data = pd.DataFrame(recommend_result, columns = ['Title', 'Correlation', 'Genre'])
	print(data)