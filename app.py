import os
import requests

from flask import Flask, Response, request
from werkzeug.datastructures import Headers

app = Flask(__name__)


cmc_header = Headers([{'Source', 'CMC'}]) #coinmarketcap
lcw_header = Headers([{'Source', 'LCW'}]) #livecoinwatch

@app.route('/')
def hello():
    return "GET url/<coinname> -> icon.png", 404


@app.route('/<path>', methods=['GET', 'POST'])
def index(path):
    if request.method == 'GET':
        print(path)
        file = get_icon(path)
        return file
    else:
        return "GET url/<coinname> -> icon.png", 400


def icons_directory():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'icons')

    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)
        path_cmc = os.path.join(dirname, 'icons', 'CMC')
        path_lcw = os.path.join(dirname, 'icons', 'LCW')
        os.makedirs(path_cmc)
        os.makedirs(path_lcw)

        print("The \"icons\" is created!")

    return path


# Look locally for the icon
def get_icon(icon: str):
    filename = icon.lower()
    path = os.path.join(icons_directory(), "CMC", "%s.png" % filename)

    if os.path.exists(path):
        f = open(path, "rb")
        image = f.read()
        f.close()
        return Response(response=image, status=200, mimetype="image/png", headers=cmc_header)
    else:
        path = os.path.join(icons_directory(), "LCW", "%s.png" % filename)
        if os.path.exists(path):
            f = open(path, "rb")
            image = f.read()
            f.close()
            print("Statically served LCW")
            return Response(response=image, status=200, mimetype="image/png", headers=lcw_header)
        else:
            return download_icon_lcw(icon)


# Download icon from www.livecoinwatch.com
def download_icon_lcw(icon: str):
    url = "https://lcw.nyc3.cdn.digitaloceanspaces.com/production/currencies/64{}.png"
    # url = "https://s2.coinmarketcap.com/static/img/coins/128x128/18639.png"
    r = requests.get(url.format(icon), allow_redirects=True)

    if r.status_code == requests.codes.ok:
        _, filename, *_ = icon.split("/")

        path = os.path.join(icons_directory(), "LCW", "%s.png" % filename)

        f = open(path, "wb")
        f.write(r.content)
        print("%s icon downloaded and saved from livecoinwatch" %filename)
        f.close()
        image = r.content
        return Response(response=image, status=200, mimetype="image/png", headers=lcw_header)
    else:
        print("Icon for \"%s\" not found on livecoinwatch server" % icon)
        return 'Icon not found!', 404
