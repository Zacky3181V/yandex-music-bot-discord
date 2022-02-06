from yandex_music import Best, Client, Search
import config as aut
import yandex_music

def download(url):
    print(url)
    client = Client.from_token(aut.OAUTH)

    url_parts=url.split('/')


    trackID = url_parts[-1]
    track = client.tracks([trackID])[0]
    trackDownloadInfo = track.get_download_info()[0]

    track.download('as', 'mp3', 192)