import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req1 = urllib.request.Request("https://cdn.pixabay.com/audio/2023/10/24/audio_33af640700.mp3", headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req1, context=ctx) as r:
        with open("/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers/indy.mp3", "wb") as f:
            f.write(r.read())
except Exception as e:
    print(e)
