import dateutil.parser
from urlparse import urlparse


def itervalues(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for ik, iv in itervalues(v, path + '.' + k):
                yield ik, iv
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for ik, iv in itervalues(v, path + '[' + i + ']'):
                yield ik, iv
    else:
        yield path, obj


def parse_datetime(text):
    try:
        dt = dateutil.parser.parse(text)
        return dt.isoformat()
    except Exception:
        return


def parse_url(url):
    try:
        parsed = urlparse(url)
        if len(parsed.scheme):
            return url
    except Exception:
        return
