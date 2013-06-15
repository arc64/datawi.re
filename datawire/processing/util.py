import dateutil.parser
from urlparse import urlparse


def parse_datetime(text):
    try:
        dt = dateutil.parser.parse(text)
        return dt
    except Exception:
        return


def parse_url(url):
    try:
        parsed = urlparse(url)
        if len(parsed.scheme):
            return url
    except Exception:
        return
