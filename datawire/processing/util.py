
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
