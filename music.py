from yandex_music import Best, Client, Search
import config as aut
import yandex_music

client = Client.from_token(aut.OAUTH)

def extractDirectLinkToTrack(track_id):
    track = client.tracks(track_id)[0]
    track_download_info = track.get_download_info()

    is_track_suitable = lambda info: all([
        info.codec == "mp3",
        info.bitrate_in_kbps == 192
    ])

    for info in track_download_info:
        if is_track_suitable(info):
            return info.get_direct_link()
            
def infoTrack(url):
    url_parts=url.split('/')
    trackID = url_parts[-1]
    albumID = url_parts[-3]
    track = client.tracks([trackID])[0]
    album = client.albums([albumID])[0]
    
    artists = ""
    for i in track.artists_name():
        artists = artists + f" {i}"
    s = {'name' : f'{track.title}', 'artists' : f'{artists}', 'album' : f'{album.title}', 'genre' : f'{album.genre}', 'duration' : f'{track.duration_ms / 1000}'}
    return s