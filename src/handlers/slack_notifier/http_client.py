import urllib.request


def post(url, data, headers={}):
    req = urllib.request.Request(url, data, headers)
    return urllib.request.urlopen(req)
