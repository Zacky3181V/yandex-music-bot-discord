from yandex_music import Best, Client, Search
import config as aut
import yandex_music

client = Client.from_token(aut.OAUTH)
def download(url):

    url_parts=url.split('/')


    trackID = url_parts[-1]
    track = client.tracks([trackID])[0]
    trackDownloadInfo = track.get_download_info()[0]

    track.download('as', 'mp3', 192)
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