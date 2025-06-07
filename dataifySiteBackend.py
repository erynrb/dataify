import json
import pandas as pd
from collections import Counter
import numpy as np
from prettytable import PrettyTable

def run(data, year, num, method):
    # choose what year to look at from all data
    data = [dataPoint for dataPoint in data if dataPoint['ts'].startswith(str(year))]
    print("got to backend")
    # get all songs played and their play times and artists - essentially simplify the data to what we want to analyse
    allSongs = []
    playTime = []
    artist = []
    totalListeningMin = 0;
    for dataPoint in data:
        allSongs = allSongs + [dataPoint['master_metadata_track_name']]
        playTime = playTime + [dataPoint['ms_played']]
        artist = artist + [dataPoint['master_metadata_album_artist_name']]
        totalListeningMin = totalListeningMin + dataPoint['ms_played']
    print("checkpoint 1")
    totalListeningMin = round((totalListeningMin)/60000)
    print('total listening time: ' + str(totalListeningMin))

    #convert to an array
    songsAndPT = [allSongs, playTime, artist]
    songsAndPT = np.array(songsAndPT)
    songsAndPT = songsAndPT[:, np.where(songsAndPT[0] != None)[0]]
    print("checkpoint 2")

    # find the total play times for each unique song and sort from most to least
    uniqueSongs, counts = np.unique(songsAndPT[0], return_counts=True) # find unique songs
    mostPlayedData = [] #initialize lists
    for songTitle in uniqueSongs:
        indicies = np.where((songsAndPT[0] == songTitle)&(songsAndPT[1]>= 30000)) # find where the song was played
        numberOfPlays = len(indicies[0])
        if numberOfPlays != 0:
            artist = songsAndPT[2][indicies[0][0]]
            totalPT = sum(songsAndPT[1][indicies[0]])/60000 # find total play time
            dataPoint = (songTitle, numberOfPlays, totalPT, artist)
            mostPlayedData = mostPlayedData+ [dataPoint] #store
    dtype = [('songTitle', 'U40'), ('plays', int), ('totalPlayTime', int), ('artist', 'U40')]
    mostPlayedData = np.array(mostPlayedData, dtype=dtype) #convert to array
    mostPlayedCount = np.sort(mostPlayedData, order='plays')[::-1]
    mostPlayedTime = np.sort(mostPlayedData, order='totalPlayTime')[::-1]
    print("checkpoint 3")

    print(method)
    # # get top num songs
    if method == 'plays':
        return mostPlayedCount[:num]
    if method == 'time':
        return mostPlayedTime[:num]
    

    del displaytable
    del mostPlayedCount
    del mostPlayedTime

    # ### --------- ARTISTS --------- ###

    # # find top 5 artists (analagous to top 5 songs)
    # uniqueArtists, counts = np.unique(songsAndPT[2], return_counts=True) # find unique songs
    # mostPlayedData = []
    # for artist in uniqueArtists:
    #     indicies = np.where((songsAndPT[2] == artist)&(songsAndPT[1]>= 30000)) # find where the artist was played
    #     numberOfPlays = len(indicies[0])
    #     if numberOfPlays != 0:
    #         totalPT = sum(songsAndPT[1][indicies[0]]) # find total play time
    #         dataPoint = (artist, numberOfPlays, totalPT)
    #         mostPlayedData = mostPlayedData+ [dataPoint] #store
    # dtype = [('artist', 'U40'), ('plays', int), ('totalPlayTime', int)]
    # mostPlayedData = np.array(mostPlayedData, dtype=dtype) #convert to array
    # mostPlayedCount = np.sort(mostPlayedData, order='plays')[::-1]
    # mostPlayedTime = np.sort(mostPlayedData, order='totalPlayTime')[::-1]

    # # get top 5 artists
    # mostPlayedCount = mostPlayedCount[:5]
    # mostPlayedTime = mostPlayedTime[:5]