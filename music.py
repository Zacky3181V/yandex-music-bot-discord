from yandex_music import Best, Client, Search
import authorise as aut
import yandex_music


client = Client.from_token(aut.OAUTH)

url = 'https://music.yandex.ru/album/7257985/track/51842422'
url_parts=url.split('/')


trackID = url_parts[-1]
track = client.tracks([trackID])[0]
trackDownloadInfo = track.get_download_info()[0]

track.download('as', 'mp3', 192)


