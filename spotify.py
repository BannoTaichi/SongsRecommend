# pip install spotipy (2.24.0)
# conda install pandas (2.2.2)
# 参考資料
# https://qiita.com/Prgckwb/items/21ec6cdbfa7fcf5aa466（getByIdArtist, getTopSongsId）
# https://qiita.com/sayuyuyu/items/4ca06a851fca41f6b270（getToPlaylist, getTrackFeatures, id_to_csv）

import spotipy, requests
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd

MY_ID = "07b0d9d93df64ced88fb8756932f8345"
MY_SECRET = "d16468dc91264cfc90e372ab37e73115"
ccm = SpotifyClientCredentials(client_id=MY_ID, client_secret=MY_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=ccm)

url = "https://accounts.spotify.com/api/token"
res = requests.post(
    url,
    {
        "grant_type": "client_credentials",
        "client_id": MY_ID,
        "client_secret": MY_SECRET,
    },
)


# [IN]アーティスト名 => [OUT]アーティストID
def getIdByArtist(artist_name):
    results = spotify.search(q="artist:" + artist_name, type="artist")
    items = results["artists"]["items"]
    artist = items[0]
    artist_id = artist["id"]
    return artist_id


# [IN]アーティスト名 => [OUT]上位曲とID
def getTopSongsIds(artist_name):
    try:
        search_id = getIdByArtist(artist_name)
        artist_top_tracks = spotify.artist_top_tracks(search_id, country="JP")["tracks"]

        songs_ids = []

        print(artist_name + f" Top10 Songs")
        for i, artist_top_track in enumerate(artist_top_tracks):
            songs_ids.append(artist_top_track["id"])
            print(i + 1, artist_top_track["id"], artist_top_track["name"])
        return songs_ids
    except IndexError:
        print("IndexError has occurred!")
    except AttributeError:
        print("AttributeError has occurred!")


# アーティスト名から全ての楽曲のIDと曲名を取得
def musicIds_from_artist(artist_name):
    artist_id = getIdByArtist(artist_name)
    # アルバムのリスト作成
    albums = []
    results = spotify.artist_albums(artist_id, album_type="album,single", limit=50)
    albums.extend(results["items"])
    # アルバムIDを収集
    album_ids = [album["id"] for album in albums]
    # アルバムトラックのリストを作成
    track_ids = []
    for album_id in album_ids:
        results = spotify.album_tracks(album_id, limit=50)
        track_ids.extend(results["items"])
    # 楽曲IDのリストを作成（重複排除）
    musicIds = []
    seen = set()
    for track_id in track_ids:
        if track_id["name"] not in seen:
            music_dict = {}
            music_dict["name"] = track_id["name"]
            music_dict["id"] = track_id["id"]
            musicIds.append(music_dict)
            seen.add(track_id["name"])
    return musicIds


# [IN]プレイリストID => [OUT]各楽曲のIDリスト
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


# [ID]楽曲ID => [OUT]特徴量リスト
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


# [IN]楽曲IDリスト => [OUT]各楽曲についての特徴量CSVファイル
def id_to_csv(song_ids):
    songs = []
    for song_id in song_ids:
        song = getTrackFeatures(song_id)
        songs.append(song)
    df = pd.DataFrame(
        songs,
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
    df.to_csv("songs.csv", encoding="utf-8", index=False)
    print("CSVファイルが作成されました。")
    return df


if __name__ == "__main__":
    artist = "Mrs. GREEN APPLE"
    topsong_ids = getTopSongsIds(artist)
    id_to_csv(topsong_ids)
    musicIds = musicIds_from_artist(artist)
    pprint(musicIds)
