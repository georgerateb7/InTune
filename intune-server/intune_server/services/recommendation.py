from flask import make_response, session
# General Python Analysis Imports

"""
import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt 
from imblearn.over_sampling import SMOTE
import ast
from typing import List
from os import listdir
from datetime import datetime

# sklean ML imports
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# Models
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# Spotify
import spotipy
"""


def get_streamings(path: str = '../spotify_data/GrantListeningHistory/') -> [dict]:
    files = [path + x for x in listdir(path)
             if x.split('.')[0][:-1] == 'StreamingHistory']
    
    all_streamings = []
    
    for file in files: 
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming 
                               in new_streamings]
    
    print("SUCCESS: Loaded all song data")
    
    return all_streamings


def recommend(data):
    try:
        print(data)
        """
        streaming = get_streamings()
        df = pd.DataFrame(streaming)

        #df = pd.read_csv("StreamingHistory0.csv")
        df.head()

        #You can either have your streaming history downloaded or access your streaming history via the spotify api
        # Renaming the column names
        df = df.rename(columns={"artistName":"artist","endTime":"date","trackName":"track"})
        df_1 = df
        df_1["secPlayed"] = df["msPlayed"]/1000


        ax = df.groupby(['artist','track']).size().to_frame('count').reset_index().plot(kind='hist',bins=25)
        ax.set_xlim(0,70)
        ax.set_title("Choosing what is a 'favorite' song")

        # Find number of occurences of each song, and keep songs with 15 or more listnes
        df4 = df.groupby(['artist','track']).size().to_frame('count').reset_index()
        #df1.head()
        df3 = df.groupby(['artist','track'])['msPlayed'].sum().reset_index()

        extracted_col = df4["count"]
        df3 = df3.join(extracted_col)
        df3 = df3[df3['count']>=10]

        # Read-in Song Features dataset
        features = pd.read_csv("../spotify_data/200kSong.csv")
        # renaming columns
        features = features.rename(columns={"artist_name":"artist","track_name":"track"})

        print("SUCCESS: Read-in Song Features dataset")

        # The 'favorite' column will be the variable that we try to predict (y).
        # Create 'favorite' column (favorite = 1, not favorite = 0)
        features['same_artists'] = features.artist.isin(df3.artist) 
        features['same_track'] = features.track.isin(df3.track) 
        features["favorite"] = np.where((features["same_artists"] == True) & (features["same_track"] == True),1,0) # If both instances are True.
        features = features.drop(["same_artists","same_track"],axis=1)

        #Creating another metric to determine if a song is a favorite or not
        df2 = features[features['favorite']==1]
        df6  = pd.merge(df2, df3, on = ["track", "artist"], how = "inner")
        df6 = df6.drop_duplicates(subset=["track", "artist"], keep= 'first')
        df6["totalTimesPlayed"] = df6["msPlayed"]/df6["duration_ms"]
        df6["totalSecPlayed"] = df6["msPlayed"]/1000

        #all time percentage played
        df6['durationSec'] = df6['duration_ms']/1000
        df6["allTimePercent"] = df6["totalSecPlayed"]/(df6['durationSec']*df6['count'])

        #narrow the favorites even more
        df6 = df6[df6['allTimePercent']>=0.6]
        features['same_artists'] = features.artist.isin(df6.artist)
        features['same_track'] = features.track.isin(df6.track) 
        features['newFav'] = np.where((features["same_artists"] == True) & (features["same_track"] == True),1,0)
        features = features.drop(["same_artists","same_track", "favorite"],axis=1)


        # Low instrumentalness + high liveness and speechiness probably indicates this catergory has minimal songs 
        # Looks like the comedy songs are not actually songs so we get rid of it
        features = features[features.genre!='Comedy']

        # ### Balancing Classes with Oversampling (SMOTE) and Feature Selection
        # Clearly the classes are very imbalanced meaning that the model would probably just predict that every song is not a favorite which would not be very useful. Oversampling from the minority class helps take care of that issue

        # For future use
        future = features.copy(deep=True)

        # Shows how the classes are imbalanced
        features.newFav.value_counts()

        #For the SMOTE function to work, we need to drop any columuns that do not have strictly nubmers - this varies from dataset to dataset, so this part must be adjusted
        #X = features.drop(columns=['favorite','artist','key','mode','time_signature','album', 'album_id', 'artist_ids','track_number', 'disc_number', 'explicit', 'year' , 'release_date', 'id', 'track'])
        X = features.drop(columns=['artist','track','genre','track_id', 'key','mode','time_signature','duration_ms','newFav'])
        y = features.newFav
        oversample = SMOTE()
        X, y = oversample.fit_resample(X, y)
        X['newFav'] = y

        # Correlation Matrix of quantitative features. Looking at the bottom row we can see which features impact the chances that a song will be a favorite the most
        c = X.corr()
        corr = sns.heatmap(c,cmap="BrBG",annot=True)

        # ### Model Selection with Cross-validation and Hyperparameter Optimization
        # We now test out three different classifier algorithims:Random Forest Classifier, Decision Tree Classifier, and Logistic Regression. The F1 score is used as the accuracy measure. 

        # Train / Split Data
        # X is the oversampled data, while y is simply which songs are classfied as favorites
        X_train, X_test, y_train, y_test = train_test_split(X.drop(columns='newFav'), X.newFav,test_size = .20)
        #X.favorite

        print("SUCCESS: Prepper for Decision Tree, this may take a while")

        # Decision Tree
        dt = DecisionTreeClassifier(max_depth=30)
        dt_scores = cross_val_score(dt, X_train, y_train, cv=10, scoring="f1")
        np.mean(dt_scores)

        print("SUCCESS: Completed Decision Tree Classifier")

        # Cross-validation for RandomForestClassifier
        rf = Pipeline([('rf', RandomForestClassifier(n_estimators = 20, max_depth = 20))])
        rf_scores = cross_val_score(rf, X_train, y_train, cv=10, scoring="f1")
        np.mean(rf_scores)

        # ### Predicting Songs and Saving Dataset for Personal Use

        # Use the F1 score to determine which model is the best. For this particular instance, the decision tree works the best

        if np.mean(rf_scores) > np.mean(dt_scores):
            model = rf
        else: 
            model = dt
        model.fit(X_train, y_train)
        prediction = model.predict(future.drop(columns=['artist','track','genre','track_id', 'key','mode','time_signature','duration_ms','newFav']))  
        future['prediction'] = prediction  

        print("SUCCESS: Did model prediction")
        
        # Gets only songs that were not favorites but are predicted to be
        future = future[(future['newFav']==0) & (future['prediction'] == 1)]
        
        #sort by  user inputed variable (can sort by popularity, dancebility, etc.)
        sort = data["sortAttribute"]
        percentage = int(data["sortStrength"])
        print("Sorting by top " + str(( 100 - percentage *10)) + " percent of the " + str(sort) + " category" )
        
        #adjust df so that it is sorted by the user inputed variable
        sorted_future = future.sort_values(by = str(sort), ascending=False)
        sorted_future = sorted_future.head(int(len(sorted_future)*(((10 - percentage) * 10)/100)))
        sorted_future = sorted_future.drop_duplicates(subset=["track", "artist"], keep= 'first')

        new_future = sorted_future.drop(columns=['key','mode','time_signature','duration_ms', 'energy', 'danceability', 'loudness','liveness', 'valence','acousticness','speechiness', 'popularity','newFav','instrumentalness', 'tempo','prediction'])

        print("SUCCESS: Sorted recommendations")

        # Saving csv
        #future.to_csv("recommendations.csv")
        #sampled csv files since 1000s of recs are too much
        sampled = new_future.sample(75)
        #sampled.to_csv("100recs.csv")
        #sampled.genre.unique()

        username = data["userHistory"]

        # Create/Access Spotipy instance
        sp = spotipy.Spotify(session["token"])

        print("SUCCESS: logged into spotipy")

        # Create a new playlist for track recommendations
        # datetime object containing current date and time
        now = datetime.now()
        
        print("now =", now)

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)	

        # Create a new playlist for track recommendations
        playlist_name = data["playlistName"]
        playlist_recs = sp.user_playlist_create(username, 
                                                name='{} - {}'.format(playlist_name, dt_string))

        print("SUCCESS: Created new playlist")

        # Add each track's recommends to the new playlist
        for i in range(0,len(sampled)):
            sp.user_playlist_add_tracks(username, playlist_recs['id'], sampled['track_id'])

        # Change the playlist details
        results = sp.user_playlist_change_details(
            username, playlist_recs['id'],
            description='Playlist of recommended tracks based on user listening history!')

        print("SUCCESS: Playlist filled with recommended songs!")
        """
        
        return make_response({'message': 'Success'}, 201)
    
    except Exception as e:
        return make_response({'message': str(e)}, 404)