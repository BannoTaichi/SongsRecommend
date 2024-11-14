# pip install spotipy (2.24.0)
# conda install pandas (2.2.2)
# 参考資料
# https://qiita.com/Prgckwb/items/21ec6cdbfa7fcf5aa466（getByIdArtist, getTopSongsId）
# https://qiita.com/sayuyuyu/items/4ca06a851fca41f6b270（getToPlaylist, getTrackFeatures, id_to_csv）

import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd

my_id = "07b0d9d93df64ced88fb8756932f8345"
my_secret = "d16468dc91264cfc90e372ab37e73115"
ccm = SpotifyClientCredentials(client_id=my_id, client_secret=my_secret)
spotify = spotipy.Spotify(client_credentials_manager=ccm)


# 入力されたアーティスト名からIDを返す
def getIdByArtist(artist_name):
    results = spotify.search(q="artist:" + artist_name, type="artist")
    items = results["artists"]["items"]
    artist = items[0]
    artist_id = artist["id"]
    return artist_id


# 入力されたアーティストの上位曲とそのIDを出力
def getTopSongsId(artist_name, num):
    try:
        search_id = getIdByArtist(artist_name)
        artist_top_tracks = spotify.artist_top_tracks(search_id, country="JP")["tracks"]

        songs_id = []

        print(artist_name + f" Top{num} Songs")
        for i, artist_top_track in enumerate(artist_top_tracks):
            songs_id.append(artist_top_track["id"])
            print(i + 1, artist_top_track["id"], artist_top_track["name"])
        return songs_id
    except IndexError:
        print("IndexError has occurred!")
    except AttributeError:
        print("AttributeError has occurred!")


# プレイリストから曲を取得
def get_to_playlist(playlist_id):
    playlist = spotify.playlist(playlist_id)
    track_ids = []
    for item in playlist["tracks"]["items"]:
        track = item["track"]
        if not track["id"] in track_ids:
            track_ids.append(track["id"])
        else:
            for item in playlist["tracks"]["items"]:
                track = item["track"]
                if not track["id"] in track_ids:
                    track_ids.append(track["id"])
    return track_ids


# 楽曲のIDから特徴量を取得
def getTrackFeatures(id):
    meta = spotify.track(id)
    features = spotify.audio_features(id)

    name = meta["name"]
    artist = meta["album"]["artists"][0]["name"]
    key = features[0]["key"]
    mode = features[0]["mode"]
    danceability = features[0]["danceability"]
    acousticness = features[0]["acousticness"]
    energy = features[0]["energy"]
    instrumentalness = features[0]["instrumentalness"]
    loudness = features[0]["loudness"]
    speechiness = features[0]["speechiness"]
    tempo = features[0]["tempo"]
    valence = features[0]["valence"]

    track = [
        name,
        artist,
        key,
        mode,
        danceability,
        acousticness,
        energy,
        instrumentalness,
        loudness,
        speechiness,
        tempo,
        valence,
    ]
    return track


# 楽曲のIDリストから各楽曲についての特徴量をCSV化
def id_to_csv(track_ids):
    tracks = []
    for track_id in track_ids:
        track = getTrackFeatures(track_id)
        tracks.append(track)
    df = pd.DataFrame(
        tracks,
        columns=[
            "name",
            "artist",
            "key",
            "mode",
            "danceability",
            "acousticness",
            "energy",
            "instrumentalness",
            "loudness",
            "speechiness",
            "tempo",
            "valence",
        ],
    )
    print(df)

    df.to_csv("songs.csv", encoding="utf-8", index=False)
    print("CSVファイルが作成されました。")
    return df


if __name__ == "__main__":
    num = 5
    songs_id = getTopSongsId("Mrs.GREEN APPLE", num)
    id_to_csv(songs_id)
