# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 23:49:22 2023

@author: KIIT

Topic="Movie recommendation "using colaborative technique


"""
#import library

import pandas as pd

#Getting the data
column_names=['user_id','item_id','rating','timestamp']
df= pd.read_csv('u.data',sep='\t',names=column_names)
movies_names= pd.read_csv("Movie_Id_Titles")
df=pd.merge(df,movies_names,on="item_id")

#Virtualization

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

#mean and count is just for to see noting more here
mean_title_rating = df.groupby('title')['rating'].mean().sort_values(ascending = False)
count_title_rating = df.groupby('title')['rating'].count().sort_values(ascending = False)

#taking the rating into the code
#rating here the mean of rating with numbers of rating
ratings= pd.DataFrame(df.groupby('title')['rating'].mean())
#updating rating with a new column named "Num of ratings"
ratings['Num of ratings']=pd.DataFrame(df.groupby('title')['rating'].count().sort_values(ascending = False))

#histograms

plt.figure(figsize=(10,4))
ratings['Num of ratings'].hist(bins=70)

plt.figure(figsize=(10,4))
ratings['rating'].hist(bins=70)

sns.jointplot(x='rating',y='Num of ratings',data=ratings,alpha=0.5)

#Now recommending the movies
# Creating a main matrix that store users ratings to all movies
movie_mat= df.pivot_table(index=('user_id'),columns=('title'), values= 'rating')

ratings.sort_values('Num of ratings', ascending=0).head(10)
#Taking a example of star wars over here 
starwars_ratings=movie_mat['Star Wars (1977)']
#similar here is for the corelation of ratings which means the strength and direction of the 2 colums i.e. Star_wars_ratings and movie matrix

similar=movie_mat.corrwith(starwars_ratings)


corr_starwars = pd.DataFrame(similar,columns=['Correlation'])
corr_starwars.dropna(inplace=True)

#Creating a main suggestion list

similar_movies= corr_starwars.sort_values('Correlation',ascending=False)

corr_starwars = corr_starwars.join(ratings['Num of ratings'])
#Here we removie the movies which isnt watched more than 100 to make a stronger suggestion
suggestion = corr_starwars[corr_starwars['Num of ratings']>100].sort_values('Correlation',ascending=False)

print("If you watched the movie 'Star Wars 1977' then here are some more recommadation= ")
print(suggestion.head(3))

