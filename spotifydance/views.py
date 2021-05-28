from django.shortcuts import render
import math
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.

def dancer(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = 'Angel Olsen'
    #[song_id,song_name,popularity,640heightimage,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo]
    #    0       1        2                3            4         5    6     7       8         9      10               11            12       13      14        
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    def get_audio_data_100_most_popular_songs(search_artist):
        #get artist_id
        artist_result = sp.search(q=search_artist,type='artist')  
        artist_id = artist_result['artists']['items'][0]['id']
        artist_picture = artist_result['artists']['items'][0]['images'][0]['url']
        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            for record in song['artists']:
                if record['id'] == artist_id:
                    by_search_artist = True
            
            if by_search_artist:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])


                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                for record in song['artists']:
                    if record['id'] == artist_id:
                        by_search_artist = True
                
                if by_search_artist:
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = sorted(song_list, key = lambda x: x[2], reverse=True)
        first_100_sorted = song_list_sorted[:99]
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)





        for i in range(0,99):
            first_100_sorted[i].append(audio_feature_search[i]['danceability'])
            first_100_sorted[i].append(audio_feature_search[i]['energy'])
            first_100_sorted[i].append(audio_feature_search[i]['key'])
            first_100_sorted[i].append(audio_feature_search[i]['loudness'])
            first_100_sorted[i].append(audio_feature_search[i]['mode'])
            first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
            first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
            first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
            first_100_sorted[i].append(audio_feature_search[i]['liveness'])
            first_100_sorted[i].append(audio_feature_search[i]['valence'])
            first_100_sorted[i].append(audio_feature_search[i]['tempo'])

        return first_100_sorted, artist_picture

    song_list = get_audio_data_100_most_popular_songs(search_artist)[0]
    artist_picture = get_audio_data_100_most_popular_songs(search_artist)[1]

    valence_sort = sorted(song_list, key = lambda x: x[13], reverse=True)
    acoustic_sort = sorted(song_list, key = lambda x: x[10], reverse=True)

    
    happy_sort = []

    for song in valence_sort:
        if song[13] > .8:
            happy_sort.append(song)
    print(happy_sort)
    random.shuffle(happy_sort)
    if len(happy_sort) < 20:
        happy_sort = valence_sort[:19]
        random.shuffle(happy_sort)


    sad_sort = []

    for song in valence_sort:
        if song[13] < .25:
            sad_sort.append(song)
    
    random.shuffle(sad_sort)

    
    if len(sad_sort) < 20:
        sad = sorted(song_list, key = lambda x: x[13], reverse=False)
        sad_sort = sad[:19]
        random.shuffle(sad_sort)
    


    print("starting here skljhdflkasjdlfkjasldfjlajlkdjafl")
    print(song_list)

    for i in song_list:
        print(len(i))




    return render(request, 'spotifydance/dancer.html', {'song_list':song_list, 'search_artist':search_artist, 'artist_picture':artist_picture, 'valence_sort':valence_sort, 'acoustic_sort':acoustic_sort, 'happy_sort':happy_sort, 'sad_sort':sad_sort})



def viewer(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    import requests
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = request.GET['search_artist']
    #search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,song_url, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7         8    9     10     11       12          13          14               15     16      17        18,     19          
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    

    #get artist_id
    artist_result = sp.search(q=search_artist,type='artist')
    if artist_result['artists']['total'] == 0:
        return redirect('empty_search')
    artist_name_site = artist_result['artists']['items'][0]['name']
    
    artist_id = artist_result['artists']['items'][0]['id']
    artist_picture = artist_result['artists']['items'][0]['images'][0]['url']


    
    def get_audio_data_100_most_popular_songs(search_artist):

        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])
                interlist.append(song['external_urls']['spotify'])



                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    print(song)
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])
                    interlist.append(song['external_urls']['spotify'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])

        else:
            for i in range(0,len(id_list)):
       
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
           


        return first_100_sorted, artist_picture

    song_list = get_audio_data_100_most_popular_songs(artist_name_site)[0]
    artist_picture = get_audio_data_100_most_popular_songs(artist_name_site)[1]

    valence_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
    acoustic_sort = list(sorted(song_list, key = lambda x: x[13], reverse=True))
    dance_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
    
    high_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=True))
    low_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=False))

    high_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=True))
    low_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=False))

    loud_sort = list(sorted(song_list, key = lambda x: x[10], reverse=True))
    quiet_sort = list(sorted(song_list, key = lambda x: x[10], reverse=False))

    popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

    acoustic_sort = acoustic_sort[:19]
    dance_sort = dance_sort[:19]

    high_tempo_sort = high_energy_sort[:19]
    low_tempo_sort = low_tempo_sort[:19]

    high_energy_sort = high_energy_sort[:19]
    low_energy_sort = low_energy_sort[:19]

    loud_sort = loud_sort[:19]
    quiet_sort = quiet_sort[:19]


  
    
    happy_sort = []

    for song in valence_sort:
        if song[15] > .8:
            happy_sort.append(song)
    random.shuffle(happy_sort)
    if len(happy_sort) < 20:
        happy_sort = valence_sort[:19]
        random.shuffle(happy_sort)


    sad_sort = []

    for song in valence_sort:
        if song[15] < .2:
            sad_sort.append(song)
    
    random.shuffle(sad_sort)

    
    if len(sad_sort) < 20:
        sad = list(sorted(song_list, key = lambda x: x[16], reverse=False))
        sad_sort = sad[:19]
        random.shuffle(sad_sort)
    







    #add unique ids to each song in each list so that doubling does not mess up jquery hover play

    happy_sort_new = []
    for x in happy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        happy_sort_new.append(interlist)
    
    for a in happy_sort_new:
        a.append(a[0]+"hap")
    
    random.shuffle(happy_sort_new)
   
    sad_sort_new = []
    for x in sad_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        sad_sort_new.append(interlist)
    
    for a in sad_sort_new:
        a.append(a[0] + "sad")
    
    random.shuffle(sad_sort_new)
  
    acoustic_sort_new = []
    for x in acoustic_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        acoustic_sort_new.append(interlist)
   
    for a in acoustic_sort_new:
        a.append(a[0] + "acoustic" ) 

    random.shuffle(acoustic_sort_new)
    
    dance_sort_new = []
    for x in dance_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        dance_sort_new.append(interlist)
    
    for a in dance_sort_new:
       a.append(a[0] + "dance")
    
    random.shuffle(dance_sort_new)
    high_tempo_sort_new = []
    for x in high_tempo_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        high_tempo_sort_new.append(interlist)
    
    for a in high_tempo_sort_new:
        a.append(a[0] + "ht")  
    random.shuffle(high_tempo_sort_new)
    
    low_tempo_sort_new = []
    for x in low_tempo_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        low_tempo_sort_new.append(interlist)
    
    for a in low_tempo_sort_new:
        a.append(a[0] + "lt")  
    random.shuffle(low_tempo_sort_new)

    high_energy_sort_new = []
    for x in high_energy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        high_energy_sort_new.append(interlist)
    
    
    for a in high_energy_sort_new:
        a.append(a[0] + "he") 
    random.shuffle(high_energy_sort_new)

    low_energy_sort_new = []
    for x in low_energy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        low_energy_sort_new.append(interlist)
    
    for a in low_energy_sort_new:
        a.append(a[0] + "le")
    random.shuffle(low_energy_sort_new)

    loud_sort_new = []
    for x in loud_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        loud_sort_new.append(interlist)
    
    for a in loud_sort_new:
        a.append(a[0] + "loud") 

    random.shuffle(loud_sort_new)
    quiet_sort_new = []
    for x in quiet_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        quiet_sort_new.append(interlist)
    
    for a in quiet_sort_new:
        a.append(a[0] + "quiet")
    
    random.shuffle(quiet_sort_new)

    popular_sort_new = []
    for x in popular_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        popular_sort_new.append(interlist)
    
    for a in popular_sort_new:
        a.append(a[0]+"pop")


        



   
    temp_dict = {'song_list':song_list, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new, 'artist_name_site': artist_name_site}
    
    if 'fail_search' in request.GET:
        fail_search_term = request.GET['fail_search']
        temp_dict['fail_search_term'] = fail_search_term
    
    return render(request, 'spotifydance/viewer.html', temp_dict)



def start(request):
  

        



    
    return render(request, 'spotifydance/start.html', {})



def safari(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7     8     9     10      11            12             13          14       15     16      17          18          
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    def get_audio_data_100_most_popular_songs(search_artist):
        #get artist_id
        artist_result = sp.search(q=search_artist,type='artist')  
        artist_id = artist_result['artists']['items'][0]['id']
        artist_picture = artist_result['artists']['items'][0]['images'][0]['url']
        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])


                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])

        else:
            for i in range(0,len(id_list)):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
           


        return first_100_sorted, artist_picture

    song_list = get_audio_data_100_most_popular_songs(search_artist)[0]
    artist_picture = get_audio_data_100_most_popular_songs(search_artist)[1]

    print(song_list)
    valence_sort = list(sorted(song_list, key = lambda x: x[15], reverse=True))
    acoustic_sort = list(sorted(song_list, key = lambda x: x[12], reverse=True))
    dance_sort = list(sorted(song_list, key = lambda x: x[6], reverse=True))
    
    high_tempo_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
    low_tempo_sort = list(sorted(song_list, key = lambda x: x[16], reverse=False))

    high_energy_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
    low_energy_sort = list(sorted(song_list, key = lambda x: x[7], reverse=False))

    loud_sort = list(sorted(song_list, key = lambda x: x[9], reverse=True))
    quiet_sort = list(sorted(song_list, key = lambda x: x[9], reverse=False))

    popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

    acoustic_sort = acoustic_sort[:19]
    dance_sort = dance_sort[:19]

    high_tempo_sort = high_energy_sort[:19]
    low_tempo_sort = low_tempo_sort[:19]

    high_energy_sort = high_energy_sort[:19]
    low_energy_sort = low_energy_sort[:19]

    loud_sort = loud_sort[:19]
    quiet_sort = quiet_sort[:19]


  
    
    happy_sort = []

    for song in valence_sort:
        if song[15] > .8:
            happy_sort.append(song)
    print(happy_sort)
    random.shuffle(happy_sort)
    if len(happy_sort) < 20:
        happy_sort = valence_sort[:19]
        random.shuffle(happy_sort)


    sad_sort = []

    for song in valence_sort:
        if song[15] < .2:
            sad_sort.append(song)
    
    random.shuffle(sad_sort)

    
    if len(sad_sort) < 20:
        sad = list(sorted(song_list, key = lambda x: x[15], reverse=False))
        sad_sort = sad[:19]
        random.shuffle(sad_sort)
    


    print("starting here skljhdflkasjdlfkjasldfjlajlkdjafl")
    print(song_list)

    for i in song_list:
        print(len(i))


    print(happy_sort)


    #add unique ids to each song in each list so that doubling does not mess up jquery hover play

    happy_sort_new = []
    for x in happy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        happy_sort_new.append(interlist)
    
    for a in happy_sort_new:
        a.append(a[0]+"hap")
    
    random.shuffle(happy_sort_new)
   
    sad_sort_new = []
    for x in sad_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        sad_sort_new.append(interlist)
    
    for a in sad_sort_new:
        a.append(a[0] + "sad")
    
    random.shuffle(sad_sort_new)
  
    acoustic_sort_new = []
    for x in acoustic_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        acoustic_sort_new.append(interlist)
   
    for a in acoustic_sort_new:
        a.append(a[0] + "acoustic" ) 

    random.shuffle(acoustic_sort_new)
    
    dance_sort_new = []
    for x in dance_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        dance_sort_new.append(interlist)
    
    for a in dance_sort_new:
       a.append(a[0] + "dance")
    
    random.shuffle(dance_sort_new)
    high_tempo_sort_new = []
    for x in high_tempo_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        high_tempo_sort_new.append(interlist)
    
    for a in high_tempo_sort_new:
        a.append(a[0] + "ht")  
    random.shuffle(high_tempo_sort_new)
    
    low_tempo_sort_new = []
    for x in low_tempo_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        low_tempo_sort_new.append(interlist)
    
    for a in low_tempo_sort_new:
        a.append(a[0] + "lt")  
    random.shuffle(low_tempo_sort_new)

    high_energy_sort_new = []
    for x in high_energy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        high_energy_sort_new.append(interlist)
    
    
    for a in high_energy_sort_new:
        a.append(a[0] + "he") 
    random.shuffle(high_energy_sort_new)

    low_energy_sort_new = []
    for x in low_energy_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        low_energy_sort_new.append(interlist)
    
    for a in low_energy_sort_new:
        a.append(a[0] + "le")
    random.shuffle(low_energy_sort_new)

    loud_sort_new = []
    for x in loud_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        loud_sort_new.append(interlist)
    
    for a in loud_sort_new:
        a.append(a[0] + "loud") 

    random.shuffle(loud_sort_new)
    quiet_sort_new = []
    for x in quiet_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        quiet_sort_new.append(interlist)
    
    for a in quiet_sort_new:
        a.append(a[0] + "quiet")
    
    random.shuffle(quiet_sort_new)

    popular_sort_new = []
    for x in popular_sort:
        interlist = []
        for y in x:
            interlist.append(y)
        popular_sort_new.append(interlist)
    
    for a in popular_sort_new:
        a.append(a[0]+"pop")


        



    
    return render(request, 'spotifydance/safari.html', {'song_list':song_list, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new})





def land(request):




    
    return render(request, 'spotifydance/land.html', {})


def land2(request):



        



    
    return render(request, 'spotifydance/land2.html', {})


def empty_search(request):



        



    
    return render(request, 'spotifydance/empty_search.html', {})




def viewer2(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    import requests
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = request.GET['search_artist']
    

    if 'search_artist2' not in request.GET:
        base_url = reverse('viewer')  # 1 /products/

        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}'.format(base_url, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4
      

    search_artist2 = request.GET['search_artist2']
    
    #search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,song_url, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, artist_name, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7         8    9     10     11       12          13          14               15     16      17        18,     19              20   
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    

    #get artist_id
    artist_result = sp.search(q=search_artist,type='artist')
    if artist_result['artists']['total'] == 0:
        return redirect('empty_search')
    artist_name_site = artist_result['artists']['items'][0]['name']
    
    artist_id = artist_result['artists']['items'][0]['id']
    artist_picture = artist_result['artists']['items'][0]['images'][0]['url']

    #check if second artist is searchable
    artist_result2 = sp.search(q=search_artist2,type='artist')
    if artist_result2['artists']['total'] == 0:
        base_url = reverse('viewer')  # 1 /products/
        query_string =  urlencode({'fail_search': search_artist2})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist2_name_site = artist_result2['artists']['items'][0]['name']
    
    artist2_id = artist_result2['artists']['items'][0]['id']
    artist2_picture = artist_result2['artists']['items'][0]['images'][0]['url']

    
    def get_audio_data_100_most_popular_songs(search_artist,artist_id_var):

        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id_var:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])
                interlist.append(song['external_urls']['spotify'])



                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id_var:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    print(song)
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])
                    interlist.append(song['external_urls']['spotify'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])
                first_100_sorted[i].append(search_artist)


        else:
            for i in range(0,len(id_list)):
       
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
                first_100_sorted[i].append(search_artist)
      


        return first_100_sorted, artist_picture

    def sort_100_songs_into_lists(top_100_function_result): #use artist_name_site in inner function

        song_list = top_100_function_result[0]
        artist_picture = top_100_function_result[1]

        valence_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
        acoustic_sort = list(sorted(song_list, key = lambda x: x[13], reverse=True))
        dance_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
        
        high_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=True))
        low_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=False))

        high_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=True))
        low_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=False))

        loud_sort = list(sorted(song_list, key = lambda x: x[10], reverse=True))
        quiet_sort = list(sorted(song_list, key = lambda x: x[10], reverse=False))

        popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

        acoustic_sort = acoustic_sort[:19]
        dance_sort = dance_sort[:19]

        high_tempo_sort = high_energy_sort[:19]
        low_tempo_sort = low_tempo_sort[:19]

        high_energy_sort = high_energy_sort[:19]
        low_energy_sort = low_energy_sort[:19]

        loud_sort = loud_sort[:19]
        quiet_sort = quiet_sort[:19]


    
        
        happy_sort = []

        for song in valence_sort:
            if song[15] > .8:
                happy_sort.append(song)
    
        if len(happy_sort) < 20:
            happy_sort = valence_sort[:19]
        


        sad_sort = []

        for song in valence_sort:
            if song[15] < .2:
                sad_sort.append(song)
        


        
        if len(sad_sort) < 20:
            sad = list(sorted(song_list, key = lambda x: x[16], reverse=False))
            sad_sort = sad[:19]
        
        







        #add unique ids to each song in each list so that doubling does not mess up jquery hover play

        happy_sort_new = []
        for x in happy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            happy_sort_new.append(interlist)
        
        for a in happy_sort_new:
            a.append(a[0]+"hap")
        
    
    
        sad_sort_new = []
        for x in sad_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            sad_sort_new.append(interlist)
        
        for a in sad_sort_new:
            a.append(a[0] + "sad")
        

    
        acoustic_sort_new = []
        for x in acoustic_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            acoustic_sort_new.append(interlist)
    
        for a in acoustic_sort_new:
            a.append(a[0] + "acoustic" ) 

    
        
        dance_sort_new = []
        for x in dance_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            dance_sort_new.append(interlist)
        
        for a in dance_sort_new:
            a.append(a[0] + "dance")
        
    
        high_tempo_sort_new = []
        for x in high_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_tempo_sort_new.append(interlist)
        
        for a in high_tempo_sort_new:
            a.append(a[0] + "ht")  
    
        
        low_tempo_sort_new = []
        for x in low_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_tempo_sort_new.append(interlist)
        
        for a in low_tempo_sort_new:
            a.append(a[0] + "lt")  
    

        high_energy_sort_new = []
        for x in high_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_energy_sort_new.append(interlist)
        
        
        for a in high_energy_sort_new:
            a.append(a[0] + "he") 
    

        low_energy_sort_new = []
        for x in low_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_energy_sort_new.append(interlist)
        
        for a in low_energy_sort_new:
            a.append(a[0] + "le")


        loud_sort_new = []
        for x in loud_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            loud_sort_new.append(interlist)
        
        for a in loud_sort_new:
            a.append(a[0] + "loud") 


        quiet_sort_new = []
        for x in quiet_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            quiet_sort_new.append(interlist)
        
        for a in quiet_sort_new:
            a.append(a[0] + "quiet")
        


        popular_sort_new = []
        for x in popular_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            popular_sort_new.append(interlist)
        
        for a in popular_sort_new:
            a.append(a[0]+"pop")


            

        return song_list, artist_picture, loud_sort_new, quiet_sort_new, high_tempo_sort_new, low_tempo_sort_new, popular_sort_new, high_energy_sort_new, low_energy_sort_new, happy_sort_new, sad_sort_new, dance_sort_new, acoustic_sort_new
    
    search_artist1_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist_name_site,artist_id))

    song_list_1 = search_artist1_result[0]
    artist_picture_1 = search_artist1_result[1]
    loud_sort_new_1 = search_artist1_result[2]
    quiet_sort_new_1 = search_artist1_result[3]
    high_tempo_sort_new_1 = search_artist1_result[4]
    low_tempo_sort_new_1 = search_artist1_result[5]
    popular_sort_new_1 = search_artist1_result[6]
    high_energy_sort_new_1 = search_artist1_result[7]
    low_energy_sort_new_1 = search_artist1_result[8]
    happy_sort_new_1 = search_artist1_result[9]
    sad_sort_new_1 = search_artist1_result[10]
    dance_sort_new_1 = search_artist1_result[11]
    acoustic_sort_new_1 = search_artist1_result[12]

 
    search_artist2_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist2_name_site,artist2_id))

    song_list_2 = search_artist2_result[0]
    artist_picture_2 = search_artist2_result[1]
    loud_sort_new_2 = search_artist2_result[2]
    quiet_sort_new_2 = search_artist2_result[3]
    high_tempo_sort_new_2 = search_artist2_result[4]
    low_tempo_sort_new_2 = search_artist2_result[5]
    popular_sort_new_2 = search_artist2_result[6]
    high_energy_sort_new_2 = search_artist2_result[7]
    low_energy_sort_new_2 = search_artist2_result[8]
    happy_sort_new_2 = search_artist2_result[9]
    sad_sort_new_2 = search_artist2_result[10]
    dance_sort_new_2 = search_artist2_result[11]
    acoustic_sort_new_2 = search_artist2_result[12]

    random.shuffle(loud_sort_new_1)
    random.shuffle(loud_sort_new_2)
    loud_sort_new_1 = loud_sort_new_1[:15]
    loud_sort_new_2 = loud_sort_new_2[:15]
    loud_sort_new = loud_sort_new_1 + loud_sort_new_2
    random.shuffle(loud_sort_new)

    random.shuffle(quiet_sort_new_1)
    random.shuffle(quiet_sort_new_2)
    quiet_sort_new_1 = quiet_sort_new_1[:15]
    quiet_sort_new_2 = quiet_sort_new_2[:15]
    quiet_sort_new = quiet_sort_new_1 + quiet_sort_new_2
    random.shuffle(quiet_sort_new)

    random.shuffle(high_tempo_sort_new_1)
    random.shuffle(high_tempo_sort_new_2)
    high_tempo_sort_new_1 = high_tempo_sort_new_1[:15]
    high_tempo_sort_new_2 = high_tempo_sort_new_2[:15]
    high_tempo_sort_new = high_tempo_sort_new_1 + high_tempo_sort_new_2
    random.shuffle(high_tempo_sort_new)

    random.shuffle(low_tempo_sort_new_1)
    random.shuffle(low_tempo_sort_new_2)
    low_tempo_sort_new_1 = low_tempo_sort_new_1[:15]
    low_tempo_sort_new_2 = low_tempo_sort_new_2[:15]
    low_tempo_sort_new = low_tempo_sort_new_1 + low_tempo_sort_new_2
    random.shuffle(low_tempo_sort_new)

    random.shuffle(high_energy_sort_new_1)
    random.shuffle(high_energy_sort_new_2)
    high_energy_sort_new_1 = high_energy_sort_new_1[:15]
    high_energy_sort_new_2 = high_energy_sort_new_2[:15]
    high_energy_sort_new = high_energy_sort_new_1 + high_energy_sort_new_2
    random.shuffle(high_energy_sort_new)

    random.shuffle(low_energy_sort_new_1)
    random.shuffle(low_energy_sort_new_2)
    low_energy_sort_new_1 = low_energy_sort_new_1[:15]
    low_energy_sort_new_2 = low_energy_sort_new_2[:15]
    low_energy_sort_new = low_energy_sort_new_1 + low_energy_sort_new_2
    random.shuffle(low_energy_sort_new)

    random.shuffle(happy_sort_new_1)
    random.shuffle(happy_sort_new_2)
    happy_sort_new_1 = happy_sort_new_1[:15]
    happy_sort_new_2 = happy_sort_new_2[:15]
    happy_sort_new = happy_sort_new_1 + happy_sort_new_2
    random.shuffle(happy_sort_new)

    random.shuffle(sad_sort_new_1)
    random.shuffle(sad_sort_new_2)
    sad_sort_new_1 = sad_sort_new_1[:15]
    sad_sort_new_2 = sad_sort_new_2[:15]
    sad_sort_new = sad_sort_new_1 + sad_sort_new_2
    random.shuffle(sad_sort_new)

    random.shuffle(dance_sort_new_1)
    random.shuffle(dance_sort_new_2)
    dance_sort_new_1 = dance_sort_new_1[:15]
    dance_sort_new_2 = dance_sort_new_2[:15]
    dance_sort_new = dance_sort_new_1 + dance_sort_new_2
    random.shuffle(dance_sort_new)

    random.shuffle(acoustic_sort_new_1)
    random.shuffle(acoustic_sort_new_2)
    acoustic_sort_new_1 = acoustic_sort_new_1[:15]
    acoustic_sort_new_2 = acoustic_sort_new_2[:15]
    acoustic_sort_new = acoustic_sort_new_1 + acoustic_sort_new_2
    random.shuffle(acoustic_sort_new)


    popular_sort_new_1 = popular_sort_new_1[:15]
    popular_sort_new_2 = popular_sort_new_2[:15]
    popular_sort_new = popular_sort_new_1 + popular_sort_new_2
    random.shuffle(popular_sort_new)
 
    
    return render(request, 'spotifydance/viewer2.html', { 'artist2_name_site':artist2_name_site, 'artist2_picture': artist2_picture, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new, 'artist_name_site': artist_name_site})







def viewer3(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    import requests
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = request.GET['search_artist']

    if 'search_artist2' not in request.GET:
        base_url = reverse('viewer')  # 1 /products/

        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}'.format(base_url, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist2 = request.GET['search_artist2']
    

    if 'search_artist3' not in request.GET:
        base_url = reverse('viewer2')  # 1 /products/
        query_string1 =  urlencode({'search_artist2': search_artist2})
        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string1, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist3 = request.GET['search_artist3']
    
    #search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,song_url, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, artist_name, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7         8    9     10     11       12          13          14               15     16      17        18,     19              20   
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    

    #get artist_id
    artist_result = sp.search(q=search_artist,type='artist')
    if artist_result['artists']['total'] == 0:
        return redirect('empty_search')
    artist_name_site = artist_result['artists']['items'][0]['name']
    
    artist_id = artist_result['artists']['items'][0]['id']
    artist_picture = artist_result['artists']['items'][0]['images'][0]['url']

    #check if second artist is searchable
    artist_result2 = sp.search(q=search_artist2,type='artist')
    if artist_result2['artists']['total'] == 0:
        base_url = reverse('viewer')  # 1 /products/
        query_string =  urlencode({'fail_search': search_artist2})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist2_name_site = artist_result2['artists']['items'][0]['name']
    
    artist2_id = artist_result2['artists']['items'][0]['id']
    artist2_picture = artist_result2['artists']['items'][0]['images'][0]['url']


    #check if third artist is searchable
    artist_result3 = sp.search(q=search_artist3,type='artist')
    if artist_result3['artists']['total'] == 0:
        base_url = reverse('viewer2')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist3})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 

        url = '{}?{}&{}&{}'.format(base_url, query_string, query_string2,query_string3)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist3_name_site = artist_result3['artists']['items'][0]['name']
    
    artist3_id = artist_result3['artists']['items'][0]['id']
    artist3_picture = artist_result3['artists']['items'][0]['images'][0]['url']

    
    def get_audio_data_100_most_popular_songs(search_artist,artist_id_var):

        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id_var:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])
                interlist.append(song['external_urls']['spotify'])



                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id_var:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    print(song)
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])
                    interlist.append(song['external_urls']['spotify'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])
                first_100_sorted[i].append(search_artist)


        else:
            for i in range(0,len(id_list)):
       
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
                first_100_sorted[i].append(search_artist)
      


        return first_100_sorted, artist_picture

    def sort_100_songs_into_lists(top_100_function_result): #use artist_name_site in inner function

        song_list = top_100_function_result[0]
        artist_picture = top_100_function_result[1]

        valence_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
        acoustic_sort = list(sorted(song_list, key = lambda x: x[13], reverse=True))
        dance_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
        
        high_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=True))
        low_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=False))

        high_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=True))
        low_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=False))

        loud_sort = list(sorted(song_list, key = lambda x: x[10], reverse=True))
        quiet_sort = list(sorted(song_list, key = lambda x: x[10], reverse=False))

        popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

        acoustic_sort = acoustic_sort[:19]
        dance_sort = dance_sort[:19]

        high_tempo_sort = high_energy_sort[:19]
        low_tempo_sort = low_tempo_sort[:19]

        high_energy_sort = high_energy_sort[:19]
        low_energy_sort = low_energy_sort[:19]

        loud_sort = loud_sort[:19]
        quiet_sort = quiet_sort[:19]


    
        
        happy_sort = []

        for song in valence_sort:
            if song[15] > .8:
                happy_sort.append(song)
    
        if len(happy_sort) < 20:
            happy_sort = valence_sort[:19]
        


        sad_sort = []

        for song in valence_sort:
            if song[15] < .2:
                sad_sort.append(song)
        


        
        if len(sad_sort) < 20:
            sad = list(sorted(song_list, key = lambda x: x[16], reverse=False))
            sad_sort = sad[:19]
        
        







        #add unique ids to each song in each list so that doubling does not mess up jquery hover play

        happy_sort_new = []
        for x in happy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            happy_sort_new.append(interlist)
        
        for a in happy_sort_new:
            a.append(a[0]+"hap")
        
    
    
        sad_sort_new = []
        for x in sad_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            sad_sort_new.append(interlist)
        
        for a in sad_sort_new:
            a.append(a[0] + "sad")
        

    
        acoustic_sort_new = []
        for x in acoustic_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            acoustic_sort_new.append(interlist)
    
        for a in acoustic_sort_new:
            a.append(a[0] + "acoustic" ) 

    
        
        dance_sort_new = []
        for x in dance_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            dance_sort_new.append(interlist)
        
        for a in dance_sort_new:
            a.append(a[0] + "dance")
        
    
        high_tempo_sort_new = []
        for x in high_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_tempo_sort_new.append(interlist)
        
        for a in high_tempo_sort_new:
            a.append(a[0] + "ht")  
    
        
        low_tempo_sort_new = []
        for x in low_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_tempo_sort_new.append(interlist)
        
        for a in low_tempo_sort_new:
            a.append(a[0] + "lt")  
    

        high_energy_sort_new = []
        for x in high_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_energy_sort_new.append(interlist)
        
        
        for a in high_energy_sort_new:
            a.append(a[0] + "he") 
    

        low_energy_sort_new = []
        for x in low_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_energy_sort_new.append(interlist)
        
        for a in low_energy_sort_new:
            a.append(a[0] + "le")


        loud_sort_new = []
        for x in loud_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            loud_sort_new.append(interlist)
        
        for a in loud_sort_new:
            a.append(a[0] + "loud") 


        quiet_sort_new = []
        for x in quiet_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            quiet_sort_new.append(interlist)
        
        for a in quiet_sort_new:
            a.append(a[0] + "quiet")
        


        popular_sort_new = []
        for x in popular_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            popular_sort_new.append(interlist)
        
        for a in popular_sort_new:
            a.append(a[0]+"pop")


            

        return song_list, artist_picture, loud_sort_new, quiet_sort_new, high_tempo_sort_new, low_tempo_sort_new, popular_sort_new, high_energy_sort_new, low_energy_sort_new, happy_sort_new, sad_sort_new, dance_sort_new, acoustic_sort_new
    
    search_artist1_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist_name_site,artist_id))

    song_list_1 = search_artist1_result[0]
    artist_picture_1 = search_artist1_result[1]
    loud_sort_new_1 = search_artist1_result[2]
    quiet_sort_new_1 = search_artist1_result[3]
    high_tempo_sort_new_1 = search_artist1_result[4]
    low_tempo_sort_new_1 = search_artist1_result[5]
    popular_sort_new_1 = search_artist1_result[6]
    high_energy_sort_new_1 = search_artist1_result[7]
    low_energy_sort_new_1 = search_artist1_result[8]
    happy_sort_new_1 = search_artist1_result[9]
    sad_sort_new_1 = search_artist1_result[10]
    dance_sort_new_1 = search_artist1_result[11]
    acoustic_sort_new_1 = search_artist1_result[12]

 
    search_artist2_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist2_name_site,artist2_id))

    song_list_2 = search_artist2_result[0]
    artist_picture_2 = search_artist2_result[1]
    loud_sort_new_2 = search_artist2_result[2]
    quiet_sort_new_2 = search_artist2_result[3]
    high_tempo_sort_new_2 = search_artist2_result[4]
    low_tempo_sort_new_2 = search_artist2_result[5]
    popular_sort_new_2 = search_artist2_result[6]
    high_energy_sort_new_2 = search_artist2_result[7]
    low_energy_sort_new_2 = search_artist2_result[8]
    happy_sort_new_2 = search_artist2_result[9]
    sad_sort_new_2 = search_artist2_result[10]
    dance_sort_new_2 = search_artist2_result[11]
    acoustic_sort_new_2 = search_artist2_result[12]

    search_artist3_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist3_name_site,artist3_id))

    song_list_3 = search_artist3_result[0]
    artist_picture_3 = search_artist3_result[1]
    loud_sort_new_3 = search_artist3_result[2]
    quiet_sort_new_3 = search_artist3_result[3]
    high_tempo_sort_new_3 = search_artist3_result[4]
    low_tempo_sort_new_3 = search_artist3_result[5]
    popular_sort_new_3 = search_artist3_result[6]
    high_energy_sort_new_3 = search_artist3_result[7]
    low_energy_sort_new_3 = search_artist3_result[8]
    happy_sort_new_3 = search_artist3_result[9]
    sad_sort_new_3 = search_artist3_result[10]
    dance_sort_new_3 = search_artist3_result[11]
    acoustic_sort_new_3 = search_artist3_result[12]



    random.shuffle(loud_sort_new_1)
    random.shuffle(loud_sort_new_2)
    random.shuffle(loud_sort_new_3)
    loud_sort_new_1 = loud_sort_new_1[:15]
    loud_sort_new_2 = loud_sort_new_2[:15]
    loud_sort_new_3 = loud_sort_new_3[:15]
    loud_sort_new = loud_sort_new_1 + loud_sort_new_2 + loud_sort_new_3
    random.shuffle(loud_sort_new)

    random.shuffle(quiet_sort_new_1)
    random.shuffle(quiet_sort_new_2)
    random.shuffle(quiet_sort_new_3)
    quiet_sort_new_1 = quiet_sort_new_1[:15]
    quiet_sort_new_2 = quiet_sort_new_2[:15]
    quiet_sort_new_3 = quiet_sort_new_3[:15]
    quiet_sort_new = quiet_sort_new_1 + quiet_sort_new_2 + quiet_sort_new_3
    random.shuffle(quiet_sort_new)

    random.shuffle(high_tempo_sort_new_1)
    random.shuffle(high_tempo_sort_new_2)
    random.shuffle(high_tempo_sort_new_3)
    high_tempo_sort_new_1 = high_tempo_sort_new_1[:15]
    high_tempo_sort_new_2 = high_tempo_sort_new_2[:15]
    high_tempo_sort_new_3 = high_tempo_sort_new_3[:15]
    high_tempo_sort_new = high_tempo_sort_new_1 + high_tempo_sort_new_2 + high_tempo_sort_new_3
    random.shuffle(high_tempo_sort_new)

    random.shuffle(low_tempo_sort_new_1)
    random.shuffle(low_tempo_sort_new_2)
    random.shuffle(low_tempo_sort_new_3)
    low_tempo_sort_new_1 = low_tempo_sort_new_1[:15]
    low_tempo_sort_new_2 = low_tempo_sort_new_2[:15]
    low_tempo_sort_new_3 = low_tempo_sort_new_3[:15]
    low_tempo_sort_new = low_tempo_sort_new_1 + low_tempo_sort_new_2 + low_tempo_sort_new_3
    random.shuffle(low_tempo_sort_new)

    random.shuffle(high_energy_sort_new_1)
    random.shuffle(high_energy_sort_new_2)
    random.shuffle(high_energy_sort_new_3)
    high_energy_sort_new_1 = high_energy_sort_new_1[:15]
    high_energy_sort_new_2 = high_energy_sort_new_2[:15]
    high_energy_sort_new_3 = high_energy_sort_new_3[:15]
    high_energy_sort_new = high_energy_sort_new_1 + high_energy_sort_new_2 + high_energy_sort_new_3
    random.shuffle(high_energy_sort_new)

    random.shuffle(low_energy_sort_new_1)
    random.shuffle(low_energy_sort_new_2)
    random.shuffle(low_energy_sort_new_3)
    low_energy_sort_new_1 = low_energy_sort_new_1[:15]
    low_energy_sort_new_2 = low_energy_sort_new_2[:15]
    low_energy_sort_new_3 = low_energy_sort_new_3[:15]
    low_energy_sort_new = low_energy_sort_new_1 + low_energy_sort_new_2 + low_energy_sort_new_3
    random.shuffle(low_energy_sort_new)

    random.shuffle(happy_sort_new_1)
    random.shuffle(happy_sort_new_2)
    random.shuffle(happy_sort_new_3)
    happy_sort_new_1 = happy_sort_new_1[:15]
    happy_sort_new_2 = happy_sort_new_2[:15]
    happy_sort_new_3 = happy_sort_new_3[:15]
    happy_sort_new = happy_sort_new_1 + happy_sort_new_2 + happy_sort_new_3
    random.shuffle(happy_sort_new)

    random.shuffle(sad_sort_new_1)
    random.shuffle(sad_sort_new_2)
    random.shuffle(sad_sort_new_3)
    sad_sort_new_1 = sad_sort_new_1[:15]
    sad_sort_new_2 = sad_sort_new_2[:15]
    sad_sort_new_3 = sad_sort_new_3[:15]
    sad_sort_new = sad_sort_new_1 + sad_sort_new_2 + sad_sort_new_3
    random.shuffle(sad_sort_new)

    random.shuffle(dance_sort_new_1)
    random.shuffle(dance_sort_new_2)
    random.shuffle(dance_sort_new_3)
    dance_sort_new_1 = dance_sort_new_1[:15]
    dance_sort_new_2 = dance_sort_new_2[:15]
    dance_sort_new_3 = dance_sort_new_3[:15]
    dance_sort_new = dance_sort_new_1 + dance_sort_new_2 + dance_sort_new_3
    random.shuffle(dance_sort_new)

    random.shuffle(acoustic_sort_new_1)
    random.shuffle(acoustic_sort_new_2)
    random.shuffle(acoustic_sort_new_3)
    acoustic_sort_new_1 = acoustic_sort_new_1[:15]
    acoustic_sort_new_2 = acoustic_sort_new_2[:15]
    acoustic_sort_new_3 = acoustic_sort_new_3[:15]
    acoustic_sort_new = acoustic_sort_new_1 + acoustic_sort_new_2 + acoustic_sort_new_3
    random.shuffle(acoustic_sort_new)


    popular_sort_new_1 = popular_sort_new_1[:15]
    popular_sort_new_2 = popular_sort_new_2[:15]
    popular_sort_new_3 = popular_sort_new_3[:15]
    popular_sort_new = popular_sort_new_1 + popular_sort_new_2 + popular_sort_new_3
    random.shuffle(popular_sort_new)
 
    
    return render(request, 'spotifydance/viewer3.html', { 'artist3_name_site':artist3_name_site, 'artist3_picture': artist3_picture,'artist2_name_site':artist2_name_site, 'artist2_picture': artist2_picture, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new, 'artist_name_site': artist_name_site})


def land3(request):



        



    
    return render(request, 'spotifydance/land3.html', {})



def land4(request):



        



    
    return render(request, 'spotifydance/land4.html', {})


def viewer4(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    import requests
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = request.GET['search_artist']

    if 'search_artist2' not in request.GET:
        base_url = reverse('viewer')  # 1 /products/

        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}'.format(base_url, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist2 = request.GET['search_artist2']
    

    if 'search_artist3' not in request.GET:
        base_url = reverse('viewer2')  # 1 /products/
        query_string2 =  urlencode({'search_artist2': search_artist2})
        query_string1 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string1, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist3 = request.GET['search_artist3']


    if 'search_artist4' not in request.GET:
        base_url = reverse('viewer3')  # 1 /products/
        query_string3 =  urlencode({'search_artist3': search_artist3})
        query_string2 =  urlencode({'search_artist2': search_artist2})
        query_string1 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}&{}'.format(base_url, query_string1, query_string2,query_string3)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    search_artist4 = request.GET['search_artist4']

    
    #search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,song_url, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, artist_name, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7         8    9     10     11       12          13          14               15     16      17        18,     19              20   
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    

    #get artist_id
    artist_result = sp.search(q=search_artist,type='artist')
    if artist_result['artists']['total'] == 0:
        return redirect('empty_search')
    artist_name_site = artist_result['artists']['items'][0]['name']
    
    artist_id = artist_result['artists']['items'][0]['id']
    artist_picture = artist_result['artists']['items'][0]['images'][0]['url']

    #check if second artist is searchable
    artist_result2 = sp.search(q=search_artist2,type='artist')
    if artist_result2['artists']['total'] == 0:
        base_url = reverse('viewer')  # 1 /products/
        query_string =  urlencode({'fail_search': search_artist2})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist2_name_site = artist_result2['artists']['items'][0]['name']
    
    artist2_id = artist_result2['artists']['items'][0]['id']
    artist2_picture = artist_result2['artists']['items'][0]['images'][0]['url']


    #check if third artist is searchable
    artist_result3 = sp.search(q=search_artist3,type='artist')
    if artist_result3['artists']['total'] == 0:
        base_url = reverse('viewer2')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist3})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 

        url = '{}?{}&{}&{}'.format(base_url, query_string, query_string2,query_string3)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist3_name_site = artist_result3['artists']['items'][0]['name']
    
    artist3_id = artist_result3['artists']['items'][0]['id']
    artist3_picture = artist_result3['artists']['items'][0]['images'][0]['url']

    #check if fourth artist is searchable
    artist_result4 = sp.search(q=search_artist4,type='artist')
    if artist_result4['artists']['total'] == 0:
        base_url = reverse('viewer3')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist4})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 
        query_string4 = urlencode({'search_artist3': search_artist3}) 

        url = '{}?{}&{}&{}&{}'.format(base_url, query_string, query_string2,query_string3, query_string4)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist4_name_site = artist_result4['artists']['items'][0]['name']
    
    artist4_id = artist_result4['artists']['items'][0]['id']
    artist4_picture = artist_result4['artists']['items'][0]['images'][0]['url']

    
    def get_audio_data_100_most_popular_songs(search_artist,artist_id_var):

        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id_var:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])
                interlist.append(song['external_urls']['spotify'])



                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id_var:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    print(song)
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])
                    interlist.append(song['external_urls']['spotify'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])
                first_100_sorted[i].append(search_artist)


        else:
            for i in range(0,len(id_list)):
       
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
                first_100_sorted[i].append(search_artist)
      


        return first_100_sorted, artist_picture

    def sort_100_songs_into_lists(top_100_function_result): #use artist_name_site in inner function

        song_list = top_100_function_result[0]
        artist_picture = top_100_function_result[1]

        valence_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
        acoustic_sort = list(sorted(song_list, key = lambda x: x[13], reverse=True))
        dance_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
        
        high_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=True))
        low_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=False))

        high_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=True))
        low_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=False))

        loud_sort = list(sorted(song_list, key = lambda x: x[10], reverse=True))
        quiet_sort = list(sorted(song_list, key = lambda x: x[10], reverse=False))

        popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

        acoustic_sort = acoustic_sort[:19]
        dance_sort = dance_sort[:19]

        high_tempo_sort = high_energy_sort[:19]
        low_tempo_sort = low_tempo_sort[:19]

        high_energy_sort = high_energy_sort[:19]
        low_energy_sort = low_energy_sort[:19]

        loud_sort = loud_sort[:19]
        quiet_sort = quiet_sort[:19]


    
        
        happy_sort = []

        for song in valence_sort:
            if song[15] > .8:
                happy_sort.append(song)
    
        if len(happy_sort) < 20:
            happy_sort = valence_sort[:19]
        


        sad_sort = []

        for song in valence_sort:
            if song[15] < .2:
                sad_sort.append(song)
        


        
        if len(sad_sort) < 20:
            sad = list(sorted(song_list, key = lambda x: x[16], reverse=False))
            sad_sort = sad[:19]
        
        







        #add unique ids to each song in each list so that doubling does not mess up jquery hover play

        happy_sort_new = []
        for x in happy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            happy_sort_new.append(interlist)
        
        for a in happy_sort_new:
            a.append(a[0]+"hap")
        
    
    
        sad_sort_new = []
        for x in sad_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            sad_sort_new.append(interlist)
        
        for a in sad_sort_new:
            a.append(a[0] + "sad")
        

    
        acoustic_sort_new = []
        for x in acoustic_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            acoustic_sort_new.append(interlist)
    
        for a in acoustic_sort_new:
            a.append(a[0] + "acoustic" ) 

    
        
        dance_sort_new = []
        for x in dance_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            dance_sort_new.append(interlist)
        
        for a in dance_sort_new:
            a.append(a[0] + "dance")
        
    
        high_tempo_sort_new = []
        for x in high_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_tempo_sort_new.append(interlist)
        
        for a in high_tempo_sort_new:
            a.append(a[0] + "ht")  
    
        
        low_tempo_sort_new = []
        for x in low_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_tempo_sort_new.append(interlist)
        
        for a in low_tempo_sort_new:
            a.append(a[0] + "lt")  
    

        high_energy_sort_new = []
        for x in high_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_energy_sort_new.append(interlist)
        
        
        for a in high_energy_sort_new:
            a.append(a[0] + "he") 
    

        low_energy_sort_new = []
        for x in low_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_energy_sort_new.append(interlist)
        
        for a in low_energy_sort_new:
            a.append(a[0] + "le")


        loud_sort_new = []
        for x in loud_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            loud_sort_new.append(interlist)
        
        for a in loud_sort_new:
            a.append(a[0] + "loud") 


        quiet_sort_new = []
        for x in quiet_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            quiet_sort_new.append(interlist)
        
        for a in quiet_sort_new:
            a.append(a[0] + "quiet")
        


        popular_sort_new = []
        for x in popular_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            popular_sort_new.append(interlist)
        
        for a in popular_sort_new:
            a.append(a[0]+"pop")


            

        return song_list, artist_picture, loud_sort_new, quiet_sort_new, high_tempo_sort_new, low_tempo_sort_new, popular_sort_new, high_energy_sort_new, low_energy_sort_new, happy_sort_new, sad_sort_new, dance_sort_new, acoustic_sort_new
    
    search_artist1_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist_name_site,artist_id))

    song_list_1 = search_artist1_result[0]
    artist_picture_1 = search_artist1_result[1]
    loud_sort_new_1 = search_artist1_result[2]
    quiet_sort_new_1 = search_artist1_result[3]
    high_tempo_sort_new_1 = search_artist1_result[4]
    low_tempo_sort_new_1 = search_artist1_result[5]
    popular_sort_new_1 = search_artist1_result[6]
    high_energy_sort_new_1 = search_artist1_result[7]
    low_energy_sort_new_1 = search_artist1_result[8]
    happy_sort_new_1 = search_artist1_result[9]
    sad_sort_new_1 = search_artist1_result[10]
    dance_sort_new_1 = search_artist1_result[11]
    acoustic_sort_new_1 = search_artist1_result[12]

 
    search_artist2_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist2_name_site,artist2_id))

    song_list_2 = search_artist2_result[0]
    artist_picture_2 = search_artist2_result[1]
    loud_sort_new_2 = search_artist2_result[2]
    quiet_sort_new_2 = search_artist2_result[3]
    high_tempo_sort_new_2 = search_artist2_result[4]
    low_tempo_sort_new_2 = search_artist2_result[5]
    popular_sort_new_2 = search_artist2_result[6]
    high_energy_sort_new_2 = search_artist2_result[7]
    low_energy_sort_new_2 = search_artist2_result[8]
    happy_sort_new_2 = search_artist2_result[9]
    sad_sort_new_2 = search_artist2_result[10]
    dance_sort_new_2 = search_artist2_result[11]
    acoustic_sort_new_2 = search_artist2_result[12]

    search_artist3_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist3_name_site,artist3_id))

    song_list_3 = search_artist3_result[0]
    artist_picture_3 = search_artist3_result[1]
    loud_sort_new_3 = search_artist3_result[2]
    quiet_sort_new_3 = search_artist3_result[3]
    high_tempo_sort_new_3 = search_artist3_result[4]
    low_tempo_sort_new_3 = search_artist3_result[5]
    popular_sort_new_3 = search_artist3_result[6]
    high_energy_sort_new_3 = search_artist3_result[7]
    low_energy_sort_new_3 = search_artist3_result[8]
    happy_sort_new_3 = search_artist3_result[9]
    sad_sort_new_3 = search_artist3_result[10]
    dance_sort_new_3 = search_artist3_result[11]
    acoustic_sort_new_3 = search_artist3_result[12]


    search_artist4_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist4_name_site,artist4_id))

    song_list_4 = search_artist4_result[0]
    artist_picture_4 = search_artist4_result[1]
    loud_sort_new_4 = search_artist4_result[2]
    quiet_sort_new_4 = search_artist4_result[3]
    high_tempo_sort_new_4 = search_artist4_result[4]
    low_tempo_sort_new_4 = search_artist4_result[5]
    popular_sort_new_4 = search_artist4_result[6]
    high_energy_sort_new_4 = search_artist4_result[7]
    low_energy_sort_new_4 = search_artist4_result[8]
    happy_sort_new_4 = search_artist4_result[9]
    sad_sort_new_4 = search_artist4_result[10]
    dance_sort_new_4 = search_artist4_result[11]
    acoustic_sort_new_4 = search_artist4_result[12]


    random.shuffle(loud_sort_new_1)
    random.shuffle(loud_sort_new_2)
    random.shuffle(loud_sort_new_3)
    random.shuffle(loud_sort_new_4)
    loud_sort_new_1 = loud_sort_new_1[:15]
    loud_sort_new_2 = loud_sort_new_2[:15]
    loud_sort_new_3 = loud_sort_new_3[:15]
    loud_sort_new_4 = loud_sort_new_4[:15]
    loud_sort_new = loud_sort_new_1 + loud_sort_new_2 + loud_sort_new_3 + loud_sort_new_4
    random.shuffle(loud_sort_new)

    random.shuffle(quiet_sort_new_1)
    random.shuffle(quiet_sort_new_2)
    random.shuffle(quiet_sort_new_3)
    random.shuffle(quiet_sort_new_4)

    quiet_sort_new_1 = quiet_sort_new_1[:15]
    quiet_sort_new_2 = quiet_sort_new_2[:15]
    quiet_sort_new_3 = quiet_sort_new_3[:15]
    quiet_sort_new_4 = quiet_sort_new_4[:15]

    quiet_sort_new = quiet_sort_new_1 + quiet_sort_new_2 + quiet_sort_new_3 + quiet_sort_new_4
    random.shuffle(quiet_sort_new)

    random.shuffle(high_tempo_sort_new_1)
    random.shuffle(high_tempo_sort_new_2)
    random.shuffle(high_tempo_sort_new_3)
    random.shuffle(high_tempo_sort_new_4)
    high_tempo_sort_new_1 = high_tempo_sort_new_1[:15]
    high_tempo_sort_new_2 = high_tempo_sort_new_2[:15]
    high_tempo_sort_new_3 = high_tempo_sort_new_3[:15]
    high_tempo_sort_new_4 = high_tempo_sort_new_4[:15]
    high_tempo_sort_new = high_tempo_sort_new_1 + high_tempo_sort_new_2 + high_tempo_sort_new_3 + high_tempo_sort_new_4
    random.shuffle(high_tempo_sort_new)

    random.shuffle(low_tempo_sort_new_1)
    random.shuffle(low_tempo_sort_new_2)
    random.shuffle(low_tempo_sort_new_3)
    random.shuffle(low_tempo_sort_new_4)
    low_tempo_sort_new_1 = low_tempo_sort_new_1[:15]
    low_tempo_sort_new_2 = low_tempo_sort_new_2[:15]
    low_tempo_sort_new_3 = low_tempo_sort_new_3[:15]
    low_tempo_sort_new_4 = low_tempo_sort_new_4[:15]
    low_tempo_sort_new = low_tempo_sort_new_1 + low_tempo_sort_new_2 + low_tempo_sort_new_3 + low_tempo_sort_new_4
    random.shuffle(low_tempo_sort_new)

    random.shuffle(high_energy_sort_new_1)
    random.shuffle(high_energy_sort_new_2)
    random.shuffle(high_energy_sort_new_3)
    random.shuffle(high_energy_sort_new_4)
    high_energy_sort_new_1 = high_energy_sort_new_1[:15]
    high_energy_sort_new_2 = high_energy_sort_new_2[:15]
    high_energy_sort_new_3 = high_energy_sort_new_3[:15]
    high_energy_sort_new_4 = high_energy_sort_new_4[:15]
    high_energy_sort_new = high_energy_sort_new_1 + high_energy_sort_new_2 + high_energy_sort_new_3 + high_energy_sort_new_4
    random.shuffle(high_energy_sort_new)

    random.shuffle(low_energy_sort_new_1)
    random.shuffle(low_energy_sort_new_2)
    random.shuffle(low_energy_sort_new_3)
    random.shuffle(low_energy_sort_new_4)
    low_energy_sort_new_1 = low_energy_sort_new_1[:15]
    low_energy_sort_new_2 = low_energy_sort_new_2[:15]
    low_energy_sort_new_3 = low_energy_sort_new_3[:15]
    low_energy_sort_new_4 = low_energy_sort_new_4[:15]
    low_energy_sort_new = low_energy_sort_new_1 + low_energy_sort_new_2 + low_energy_sort_new_3 + low_energy_sort_new_4
    random.shuffle(low_energy_sort_new)

    random.shuffle(happy_sort_new_1)
    random.shuffle(happy_sort_new_2)
    random.shuffle(happy_sort_new_3)
    random.shuffle(happy_sort_new_4)
    happy_sort_new_1 = happy_sort_new_1[:15]
    happy_sort_new_2 = happy_sort_new_2[:15]
    happy_sort_new_3 = happy_sort_new_3[:15]
    happy_sort_new_4 = happy_sort_new_4[:15]
    happy_sort_new = happy_sort_new_1 + happy_sort_new_2 + happy_sort_new_3 + happy_sort_new_4
    random.shuffle(happy_sort_new)

    random.shuffle(sad_sort_new_1)
    random.shuffle(sad_sort_new_2)
    random.shuffle(sad_sort_new_3)
    random.shuffle(sad_sort_new_4)
    sad_sort_new_1 = sad_sort_new_1[:15]
    sad_sort_new_2 = sad_sort_new_2[:15]
    sad_sort_new_3 = sad_sort_new_3[:15]
    sad_sort_new_4 = sad_sort_new_4[:15]
    sad_sort_new = sad_sort_new_1 + sad_sort_new_2 + sad_sort_new_3 + sad_sort_new_4
    random.shuffle(sad_sort_new)

    random.shuffle(dance_sort_new_1)
    random.shuffle(dance_sort_new_2)
    random.shuffle(dance_sort_new_3)
    random.shuffle(dance_sort_new_4)
    dance_sort_new_1 = dance_sort_new_1[:15]
    dance_sort_new_2 = dance_sort_new_2[:15]
    dance_sort_new_3 = dance_sort_new_3[:15]
    dance_sort_new_4= dance_sort_new_4[:15]
    dance_sort_new = dance_sort_new_1 + dance_sort_new_2 + dance_sort_new_3 + dance_sort_new_4
    random.shuffle(dance_sort_new)

    random.shuffle(acoustic_sort_new_1)
    random.shuffle(acoustic_sort_new_2)
    random.shuffle(acoustic_sort_new_3)
    random.shuffle(acoustic_sort_new_4)
    acoustic_sort_new_1 = acoustic_sort_new_1[:15]
    acoustic_sort_new_2 = acoustic_sort_new_2[:15]
    acoustic_sort_new_3 = acoustic_sort_new_3[:15]
    acoustic_sort_new_4 = acoustic_sort_new_4[:15]
    acoustic_sort_new = acoustic_sort_new_1 + acoustic_sort_new_2 + acoustic_sort_new_3 + acoustic_sort_new_4
    random.shuffle(acoustic_sort_new)


    popular_sort_new_1 = popular_sort_new_1[:15]
    popular_sort_new_2 = popular_sort_new_2[:15]
    popular_sort_new_3 = popular_sort_new_3[:15]
    popular_sort_new_4 = popular_sort_new_4[:15]

    popular_sort_new = popular_sort_new_1 + popular_sort_new_2 + popular_sort_new_3 + popular_sort_new_4
    random.shuffle(popular_sort_new)
 
    
    return render(request, 'spotifydance/viewer4.html', { 'artist4_name_site':artist4_name_site, 'artist4_picture': artist4_picture,'artist3_name_site':artist3_name_site, 'artist3_picture': artist3_picture,'artist2_name_site':artist2_name_site, 'artist2_picture': artist2_picture, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new, 'artist_name_site': artist_name_site})


def land5(request):



        



    
    return render(request, 'spotifydance/land5.html', {})


def viewer5(request):
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import json
    import random
    import requests
    
    #set up api credentials
    cid = 'efbd704e955543d5a3d9d9ca45426daf'
    secret = '697dc1ecaef1431bbbc7f8a9506e6198'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    

    search_artist = request.GET['search_artist']

    if 'search_artist2' not in request.GET:
        base_url = reverse('viewer')  # 1 /products/

        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}'.format(base_url, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist2 = request.GET['search_artist2']
    

    if 'search_artist3' not in request.GET:
        base_url = reverse('viewer2')  # 1 /products/
        query_string2 =  urlencode({'search_artist2': search_artist2})
        query_string1 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string1, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4



    search_artist3 = request.GET['search_artist3']


    if 'search_artist4' not in request.GET:
        base_url = reverse('viewer3')  # 1 /products/
        query_string3 =  urlencode({'search_artist3': search_artist3})
        query_string2 =  urlencode({'search_artist2': search_artist2})
        query_string1 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}&{}'.format(base_url, query_string1, query_string2,query_string3)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    search_artist4 = request.GET['search_artist4']


    if 'search_artist5' not in request.GET:
        base_url = reverse('viewer4')  # 1 /products/
        query_string4 =  urlencode({'search_artist4': search_artist4})
        query_string3 =  urlencode({'search_artist3': search_artist3})
        query_string2 =  urlencode({'search_artist2': search_artist2})
        query_string1 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}&{}${}'.format(base_url, query_string1, query_string2,query_string3,query_string4)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    search_artist5 = request.GET['search_artist5']

    
    #search_artist = 'Jack White'
    #[song_id,song_name,popularity,640heightimage,album_name,preview_url,song_url, danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,track_uri, artist_name, jquery_unique_id,]
    #    0       1        2                3           4         5           6           7         8    9     10     11       12          13          14               15     16      17        18,     19              20   
    
    #function getting all audio feature data for top 100 most popular songs by searched artist
    

    #get artist_id
    artist_result = sp.search(q=search_artist,type='artist')
    if artist_result['artists']['total'] == 0:
        return redirect('empty_search')
    artist_name_site = artist_result['artists']['items'][0]['name']
    
    artist_id = artist_result['artists']['items'][0]['id']
    artist_picture = artist_result['artists']['items'][0]['images'][0]['url']

    #check if second artist is searchable
    artist_result2 = sp.search(q=search_artist2,type='artist')
    if artist_result2['artists']['total'] == 0:
        base_url = reverse('viewer')  # 1 /products/
        query_string =  urlencode({'fail_search': search_artist2})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        url = '{}?{}&{}'.format(base_url, query_string, query_string2)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist2_name_site = artist_result2['artists']['items'][0]['name']
    
    artist2_id = artist_result2['artists']['items'][0]['id']
    artist2_picture = artist_result2['artists']['items'][0]['images'][0]['url']


    #check if third artist is searchable
    artist_result3 = sp.search(q=search_artist3,type='artist')
    if artist_result3['artists']['total'] == 0:
        base_url = reverse('viewer2')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist3})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 

        url = '{}?{}&{}&{}'.format(base_url, query_string, query_string2,query_string3)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist3_name_site = artist_result3['artists']['items'][0]['name']
    
    artist3_id = artist_result3['artists']['items'][0]['id']
    artist3_picture = artist_result3['artists']['items'][0]['images'][0]['url']

    #check if fourth artist is searchable
    artist_result4 = sp.search(q=search_artist4,type='artist')
    if artist_result4['artists']['total'] == 0:
        base_url = reverse('viewer3')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist4})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 
        query_string4 = urlencode({'search_artist3': search_artist3}) 

        url = '{}?{}&{}&{}&{}'.format(base_url, query_string, query_string2,query_string3, query_string4)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist4_name_site = artist_result4['artists']['items'][0]['name']
    
    artist4_id = artist_result4['artists']['items'][0]['id']
    artist4_picture = artist_result4['artists']['items'][0]['images'][0]['url']


    #check if fifth artist is searchable
    artist_result5 = sp.search(q=search_artist5,type='artist')
    if artist_result5['artists']['total'] == 0:
        base_url = reverse('viewer4')  # 1 /products/
        
        query_string =  urlencode({'fail_search': search_artist5})  # 2 category=42
        query_string2 =  urlencode({'search_artist': search_artist}) 
        query_string3 =  urlencode({'search_artist2': search_artist2}) 
        query_string4 = urlencode({'search_artist3': search_artist3}) 
        query_string5 = urlencode({'search_artist4': search_artist4}) 

        url = '{}?{}&{}&{}&{}&{}'.format(base_url, query_string, query_string2,query_string3, query_string4, query_string5)  # 3 /products/?category=42
        return redirect(url)  # 4
    
    artist5_name_site = artist_result5['artists']['items'][0]['name']
    
    artist5_id = artist_result5['artists']['items'][0]['id']
    artist5_picture = artist_result5['artists']['items'][0]['images'][0]['url']

    
    def get_audio_data_100_most_popular_songs(search_artist,artist_id_var):

        
        #get tracks
        result = sp.search(q='artist:'+search_artist,type='track')
        song_records = result['tracks']['items']
        
        song_list = []
        
        #verify song artist is our artist by using id
        for song in song_records:
            by_search_artist = False
            not_commentary = True
            for record in song['artists']:
                if record['id'] == artist_id_var:
                    by_search_artist = True
            if "Track-by-Track Commentary" in song['album']['name']:
                not_commentary = False
                

            
            
            if by_search_artist and not_commentary:
                interlist = []
                interlist.append(song['id'])
                interlist.append(song['name'])
                interlist.append(song['popularity'])
                interlist.append(song['album']['images'][0]['url'])
                interlist.append(song['album']['name'])
                interlist.append(song['preview_url'])
                interlist.append(song['external_urls']['spotify'])



                song_list.append(interlist)
        
        #limited to 10 so get offset
        total_tracks = result['tracks']['total']
        total_tracks_pages = math.ceil(total_tracks/10)
        

        offsetter = 10
        total_tracks_pages -= 1
        while total_tracks_pages > 0 and offsetter < 300:
            result = sp.search(q='artist:'+search_artist,type='track',offset=offsetter)
            song_records = result['tracks']['items']
            for song in song_records:
                by_search_artist = False
                not_commentary = True
                for record in song['artists']:
                    if record['id'] == artist_id_var:
                        by_search_artist = True
                if "Track-by-Track Commentary" in song['album']['name']:
                    not_commentary = False
            
                
                if by_search_artist and not_commentary:
                    print(song)
                    interlist = []
                    interlist.append(song['id'])
                    interlist.append(song['name'])
                    interlist.append(song['popularity'])
                    interlist.append(song['album']['images'][0]['url'])
                    interlist.append(song['album']['name'])
                    interlist.append(song['preview_url'])
                    interlist.append(song['external_urls']['spotify'])

                    song_list.append(interlist)

                
            total_tracks_pages -= 1
            offsetter += 10
            



        song_list_sorted = list(sorted(song_list, key = lambda x: x[2], reverse=True))
        if len(song_list_sorted) >= 100:
            first_100_sorted = song_list_sorted[:99]
        else:
            first_100_sorted = song_list_sorted
        id_list = []
        for song_record in first_100_sorted:
            id_list.append(song_record[0])
        

        audio_feature_search = sp.audio_features(id_list)



        if len(id_list) >= 100:

            for i in range(0,99):
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])
                first_100_sorted[i].append(search_artist)


        else:
            for i in range(0,len(id_list)):
       
                first_100_sorted[i].append(audio_feature_search[i]['danceability'])
                first_100_sorted[i].append(audio_feature_search[i]['energy'])
                first_100_sorted[i].append(audio_feature_search[i]['key'])
                first_100_sorted[i].append(audio_feature_search[i]['loudness'])
                first_100_sorted[i].append(audio_feature_search[i]['mode'])
                first_100_sorted[i].append(audio_feature_search[i]['speechiness'])
                first_100_sorted[i].append(audio_feature_search[i]['acousticness'])
                first_100_sorted[i].append(audio_feature_search[i]['instrumentalness'])
                first_100_sorted[i].append(audio_feature_search[i]['liveness'])
                first_100_sorted[i].append(audio_feature_search[i]['valence'])
                first_100_sorted[i].append(audio_feature_search[i]['tempo'])
                first_100_sorted[i].append(audio_feature_search[i]['uri'])           
                first_100_sorted[i].append(search_artist)
      


        return first_100_sorted, artist_picture

    def sort_100_songs_into_lists(top_100_function_result): #use artist_name_site in inner function

        song_list = top_100_function_result[0]
        artist_picture = top_100_function_result[1]

        valence_sort = list(sorted(song_list, key = lambda x: x[16], reverse=True))
        acoustic_sort = list(sorted(song_list, key = lambda x: x[13], reverse=True))
        dance_sort = list(sorted(song_list, key = lambda x: x[7], reverse=True))
        
        high_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=True))
        low_tempo_sort = list(sorted(song_list, key = lambda x: x[17], reverse=False))

        high_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=True))
        low_energy_sort = list(sorted(song_list, key = lambda x: x[8], reverse=False))

        loud_sort = list(sorted(song_list, key = lambda x: x[10], reverse=True))
        quiet_sort = list(sorted(song_list, key = lambda x: x[10], reverse=False))

        popular_sort = sorted(song_list, key= lambda x: x[2], reverse=True)

        acoustic_sort = acoustic_sort[:19]
        dance_sort = dance_sort[:19]

        high_tempo_sort = high_energy_sort[:19]
        low_tempo_sort = low_tempo_sort[:19]

        high_energy_sort = high_energy_sort[:19]
        low_energy_sort = low_energy_sort[:19]

        loud_sort = loud_sort[:19]
        quiet_sort = quiet_sort[:19]


    
        
        happy_sort = []

        for song in valence_sort:
            if song[15] > .8:
                happy_sort.append(song)
    
        if len(happy_sort) < 20:
            happy_sort = valence_sort[:19]
        


        sad_sort = []

        for song in valence_sort:
            if song[15] < .2:
                sad_sort.append(song)
        


        
        if len(sad_sort) < 20:
            sad = list(sorted(song_list, key = lambda x: x[16], reverse=False))
            sad_sort = sad[:19]
        
        







        #add unique ids to each song in each list so that doubling does not mess up jquery hover play

        happy_sort_new = []
        for x in happy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            happy_sort_new.append(interlist)
        
        for a in happy_sort_new:
            a.append(a[0]+"hap")
        
    
    
        sad_sort_new = []
        for x in sad_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            sad_sort_new.append(interlist)
        
        for a in sad_sort_new:
            a.append(a[0] + "sad")
        

    
        acoustic_sort_new = []
        for x in acoustic_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            acoustic_sort_new.append(interlist)
    
        for a in acoustic_sort_new:
            a.append(a[0] + "acoustic" ) 

    
        
        dance_sort_new = []
        for x in dance_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            dance_sort_new.append(interlist)
        
        for a in dance_sort_new:
            a.append(a[0] + "dance")
        
    
        high_tempo_sort_new = []
        for x in high_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_tempo_sort_new.append(interlist)
        
        for a in high_tempo_sort_new:
            a.append(a[0] + "ht")  
    
        
        low_tempo_sort_new = []
        for x in low_tempo_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_tempo_sort_new.append(interlist)
        
        for a in low_tempo_sort_new:
            a.append(a[0] + "lt")  
    

        high_energy_sort_new = []
        for x in high_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            high_energy_sort_new.append(interlist)
        
        
        for a in high_energy_sort_new:
            a.append(a[0] + "he") 
    

        low_energy_sort_new = []
        for x in low_energy_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            low_energy_sort_new.append(interlist)
        
        for a in low_energy_sort_new:
            a.append(a[0] + "le")


        loud_sort_new = []
        for x in loud_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            loud_sort_new.append(interlist)
        
        for a in loud_sort_new:
            a.append(a[0] + "loud") 


        quiet_sort_new = []
        for x in quiet_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            quiet_sort_new.append(interlist)
        
        for a in quiet_sort_new:
            a.append(a[0] + "quiet")
        


        popular_sort_new = []
        for x in popular_sort:
            interlist = []
            for y in x:
                interlist.append(y)
            popular_sort_new.append(interlist)
        
        for a in popular_sort_new:
            a.append(a[0]+"pop")


            

        return song_list, artist_picture, loud_sort_new, quiet_sort_new, high_tempo_sort_new, low_tempo_sort_new, popular_sort_new, high_energy_sort_new, low_energy_sort_new, happy_sort_new, sad_sort_new, dance_sort_new, acoustic_sort_new
    
    search_artist1_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist_name_site,artist_id))

    song_list_1 = search_artist1_result[0]
    artist_picture_1 = search_artist1_result[1]
    loud_sort_new_1 = search_artist1_result[2]
    quiet_sort_new_1 = search_artist1_result[3]
    high_tempo_sort_new_1 = search_artist1_result[4]
    low_tempo_sort_new_1 = search_artist1_result[5]
    popular_sort_new_1 = search_artist1_result[6]
    high_energy_sort_new_1 = search_artist1_result[7]
    low_energy_sort_new_1 = search_artist1_result[8]
    happy_sort_new_1 = search_artist1_result[9]
    sad_sort_new_1 = search_artist1_result[10]
    dance_sort_new_1 = search_artist1_result[11]
    acoustic_sort_new_1 = search_artist1_result[12]

 
    search_artist2_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist2_name_site,artist2_id))

    song_list_2 = search_artist2_result[0]
    artist_picture_2 = search_artist2_result[1]
    loud_sort_new_2 = search_artist2_result[2]
    quiet_sort_new_2 = search_artist2_result[3]
    high_tempo_sort_new_2 = search_artist2_result[4]
    low_tempo_sort_new_2 = search_artist2_result[5]
    popular_sort_new_2 = search_artist2_result[6]
    high_energy_sort_new_2 = search_artist2_result[7]
    low_energy_sort_new_2 = search_artist2_result[8]
    happy_sort_new_2 = search_artist2_result[9]
    sad_sort_new_2 = search_artist2_result[10]
    dance_sort_new_2 = search_artist2_result[11]
    acoustic_sort_new_2 = search_artist2_result[12]

    search_artist3_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist3_name_site,artist3_id))

    song_list_3 = search_artist3_result[0]
    artist_picture_3 = search_artist3_result[1]
    loud_sort_new_3 = search_artist3_result[2]
    quiet_sort_new_3 = search_artist3_result[3]
    high_tempo_sort_new_3 = search_artist3_result[4]
    low_tempo_sort_new_3 = search_artist3_result[5]
    popular_sort_new_3 = search_artist3_result[6]
    high_energy_sort_new_3 = search_artist3_result[7]
    low_energy_sort_new_3 = search_artist3_result[8]
    happy_sort_new_3 = search_artist3_result[9]
    sad_sort_new_3 = search_artist3_result[10]
    dance_sort_new_3 = search_artist3_result[11]
    acoustic_sort_new_3 = search_artist3_result[12]


    search_artist4_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist4_name_site,artist4_id))

    song_list_4 = search_artist4_result[0]
    artist_picture_4 = search_artist4_result[1]
    loud_sort_new_4 = search_artist4_result[2]
    quiet_sort_new_4 = search_artist4_result[3]
    high_tempo_sort_new_4 = search_artist4_result[4]
    low_tempo_sort_new_4 = search_artist4_result[5]
    popular_sort_new_4 = search_artist4_result[6]
    high_energy_sort_new_4 = search_artist4_result[7]
    low_energy_sort_new_4 = search_artist4_result[8]
    happy_sort_new_4 = search_artist4_result[9]
    sad_sort_new_4 = search_artist4_result[10]
    dance_sort_new_4 = search_artist4_result[11]
    acoustic_sort_new_4 = search_artist4_result[12]



    search_artist5_result = sort_100_songs_into_lists(get_audio_data_100_most_popular_songs(artist5_name_site,artist5_id))

    song_list_5 = search_artist5_result[0]
    artist_picture_5 = search_artist5_result[1]
    loud_sort_new_5 = search_artist5_result[2]
    quiet_sort_new_5 = search_artist5_result[3]
    high_tempo_sort_new_5 = search_artist5_result[4]
    low_tempo_sort_new_5 = search_artist5_result[5]
    popular_sort_new_5 = search_artist5_result[6]
    high_energy_sort_new_5 = search_artist5_result[7]
    low_energy_sort_new_5 = search_artist5_result[8]
    happy_sort_new_5 = search_artist5_result[9]
    sad_sort_new_5 = search_artist5_result[10]
    dance_sort_new_5 = search_artist5_result[11]
    acoustic_sort_new_5 = search_artist5_result[12]


    random.shuffle(loud_sort_new_1)
    random.shuffle(loud_sort_new_2)
    random.shuffle(loud_sort_new_3)
    random.shuffle(loud_sort_new_4)
    random.shuffle(loud_sort_new_5)
    loud_sort_new_1 = loud_sort_new_1[:15]
    loud_sort_new_2 = loud_sort_new_2[:15]
    loud_sort_new_3 = loud_sort_new_3[:15]
    loud_sort_new_4 = loud_sort_new_4[:15]
    loud_sort_new_5 = loud_sort_new_5[:15]
    loud_sort_new = loud_sort_new_1 + loud_sort_new_2 + loud_sort_new_3 + loud_sort_new_4 + loud_sort_new_5
    random.shuffle(loud_sort_new)




    random.shuffle(quiet_sort_new_1)
    random.shuffle(quiet_sort_new_2)
    random.shuffle(quiet_sort_new_3)
    random.shuffle(quiet_sort_new_4)
    random.shuffle(quiet_sort_new_5)
    quiet_sort_new_1 = quiet_sort_new_1[:15]
    quiet_sort_new_2 = quiet_sort_new_2[:15]
    quiet_sort_new_3 = quiet_sort_new_3[:15]
    quiet_sort_new_4 = quiet_sort_new_4[:15]
    quiet_sort_new_5 = quiet_sort_new_5[:15]

    quiet_sort_new = quiet_sort_new_1 + quiet_sort_new_2 + quiet_sort_new_3 + quiet_sort_new_4 + quiet_sort_new_5
    random.shuffle(quiet_sort_new)

    random.shuffle(high_tempo_sort_new_1)
    random.shuffle(high_tempo_sort_new_2)
    random.shuffle(high_tempo_sort_new_3)
    random.shuffle(high_tempo_sort_new_4)
    random.shuffle(high_tempo_sort_new_5)
    high_tempo_sort_new_1 = high_tempo_sort_new_1[:15]
    high_tempo_sort_new_2 = high_tempo_sort_new_2[:15]
    high_tempo_sort_new_3 = high_tempo_sort_new_3[:15]
    high_tempo_sort_new_4 = high_tempo_sort_new_4[:15]
    high_tempo_sort_new_5 = high_tempo_sort_new_5[:15]
    high_tempo_sort_new = high_tempo_sort_new_1 + high_tempo_sort_new_2 + high_tempo_sort_new_3 + high_tempo_sort_new_4 + high_tempo_sort_new_5
    random.shuffle(high_tempo_sort_new)

    random.shuffle(low_tempo_sort_new_1)
    random.shuffle(low_tempo_sort_new_2)
    random.shuffle(low_tempo_sort_new_3)
    random.shuffle(low_tempo_sort_new_4)
    random.shuffle(low_tempo_sort_new_5)
    low_tempo_sort_new_1 = low_tempo_sort_new_1[:15]
    low_tempo_sort_new_2 = low_tempo_sort_new_2[:15]
    low_tempo_sort_new_3 = low_tempo_sort_new_3[:15]
    low_tempo_sort_new_4 = low_tempo_sort_new_4[:15]
    low_tempo_sort_new_5 = low_tempo_sort_new_5[:15]
    low_tempo_sort_new = low_tempo_sort_new_1 + low_tempo_sort_new_2 + low_tempo_sort_new_3 + low_tempo_sort_new_4 + low_tempo_sort_new_5
    random.shuffle(low_tempo_sort_new)

    random.shuffle(high_energy_sort_new_1)
    random.shuffle(high_energy_sort_new_2)
    random.shuffle(high_energy_sort_new_3)
    random.shuffle(high_energy_sort_new_4)
    random.shuffle(high_energy_sort_new_5)
    high_energy_sort_new_1 = high_energy_sort_new_1[:15]
    high_energy_sort_new_2 = high_energy_sort_new_2[:15]
    high_energy_sort_new_3 = high_energy_sort_new_3[:15]
    high_energy_sort_new_4 = high_energy_sort_new_4[:15]
    high_energy_sort_new_5 = high_energy_sort_new_5[:15]
    high_energy_sort_new = high_energy_sort_new_1 + high_energy_sort_new_2 + high_energy_sort_new_3 + high_energy_sort_new_4 + high_energy_sort_new_5
    random.shuffle(high_energy_sort_new)

    random.shuffle(low_energy_sort_new_1)
    random.shuffle(low_energy_sort_new_2)
    random.shuffle(low_energy_sort_new_3)
    random.shuffle(low_energy_sort_new_4)
    random.shuffle(low_energy_sort_new_5)
    low_energy_sort_new_1 = low_energy_sort_new_1[:15]
    low_energy_sort_new_2 = low_energy_sort_new_2[:15]
    low_energy_sort_new_3 = low_energy_sort_new_3[:15]
    low_energy_sort_new_4 = low_energy_sort_new_4[:15]
    low_energy_sort_new_5 = low_energy_sort_new_5[:15]
    low_energy_sort_new = low_energy_sort_new_1 + low_energy_sort_new_2 + low_energy_sort_new_3 + low_energy_sort_new_4 + low_energy_sort_new_5
    random.shuffle(low_energy_sort_new)

    random.shuffle(happy_sort_new_1)
    random.shuffle(happy_sort_new_2)
    random.shuffle(happy_sort_new_3)
    random.shuffle(happy_sort_new_4)
    random.shuffle(happy_sort_new_4)

    happy_sort_new_1 = happy_sort_new_1[:15]
    happy_sort_new_2 = happy_sort_new_2[:15]
    happy_sort_new_3 = happy_sort_new_3[:15]
    happy_sort_new_4 = happy_sort_new_4[:15]
    happy_sort_new_5 = happy_sort_new_5[:15]
    happy_sort_new = happy_sort_new_1 + happy_sort_new_2 + happy_sort_new_3 + happy_sort_new_4 + happy_sort_new_5
    random.shuffle(happy_sort_new)

    random.shuffle(sad_sort_new_1)
    random.shuffle(sad_sort_new_2)
    random.shuffle(sad_sort_new_3)
    random.shuffle(sad_sort_new_4)
    random.shuffle(sad_sort_new_5)
    sad_sort_new_1 = sad_sort_new_1[:15]
    sad_sort_new_2 = sad_sort_new_2[:15]
    sad_sort_new_3 = sad_sort_new_3[:15]
    sad_sort_new_4 = sad_sort_new_4[:15]
    sad_sort_new_5 = sad_sort_new_5[:15]
    sad_sort_new = sad_sort_new_1 + sad_sort_new_2 + sad_sort_new_3 + sad_sort_new_4 + sad_sort_new_5
    random.shuffle(sad_sort_new)

    random.shuffle(dance_sort_new_1)
    random.shuffle(dance_sort_new_2)
    random.shuffle(dance_sort_new_3)
    random.shuffle(dance_sort_new_4)
    random.shuffle(dance_sort_new_5)
    dance_sort_new_1 = dance_sort_new_1[:15]
    dance_sort_new_2 = dance_sort_new_2[:15]
    dance_sort_new_3 = dance_sort_new_3[:15]
    dance_sort_new_4= dance_sort_new_4[:15]
    dance_sort_new_4= dance_sort_new_5[:15]
    dance_sort_new = dance_sort_new_1 + dance_sort_new_2 + dance_sort_new_3 + dance_sort_new_4 + dance_sort_new_5
    random.shuffle(dance_sort_new)

    random.shuffle(acoustic_sort_new_1)
    random.shuffle(acoustic_sort_new_2)
    random.shuffle(acoustic_sort_new_3)
    random.shuffle(acoustic_sort_new_4)
    random.shuffle(acoustic_sort_new_5)
    acoustic_sort_new_1 = acoustic_sort_new_1[:15]
    acoustic_sort_new_2 = acoustic_sort_new_2[:15]
    acoustic_sort_new_3 = acoustic_sort_new_3[:15]
    acoustic_sort_new_4 = acoustic_sort_new_4[:15]
    acoustic_sort_new_5 = acoustic_sort_new_5[:15]
    acoustic_sort_new = acoustic_sort_new_1 + acoustic_sort_new_2 + acoustic_sort_new_3 + acoustic_sort_new_4 + acoustic_sort_new_5
    random.shuffle(acoustic_sort_new)


    popular_sort_new_1 = popular_sort_new_1[:15]
    popular_sort_new_2 = popular_sort_new_2[:15]
    popular_sort_new_3 = popular_sort_new_3[:15]
    popular_sort_new_4 = popular_sort_new_4[:15]
    popular_sort_new_5 = popular_sort_new_5[:15]

    popular_sort_new = popular_sort_new_1 + popular_sort_new_2 + popular_sort_new_3 + popular_sort_new_4 + popular_sort_new_5
    random.shuffle(popular_sort_new)
 
    
    return render(request, 'spotifydance/viewer5.html', { 'artist5_name_site':artist5_name_site, 'artist5_picture': artist5_picture,'artist4_name_site':artist4_name_site, 'artist4_picture': artist4_picture,'artist3_name_site':artist3_name_site, 'artist3_picture': artist3_picture,'artist2_name_site':artist2_name_site, 'artist2_picture': artist2_picture, 'search_artist':search_artist, 'artist_picture':artist_picture,  'acoustic_sort_new':acoustic_sort_new, 'happy_sort_new':happy_sort_new, 'sad_sort_new':sad_sort_new, 'dance_sort_new':dance_sort_new, 'high_tempo_sort_new':high_tempo_sort_new, 'low_tempo_sort_new':low_tempo_sort_new, 'high_energy_sort_new':high_energy_sort_new, 'low_energy_sort_new':low_energy_sort_new, 'loud_sort_new':loud_sort_new, 'quiet_sort_new':quiet_sort_new, 'popular_sort_new':popular_sort_new, 'artist_name_site': artist_name_site})
