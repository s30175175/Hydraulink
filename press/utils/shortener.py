import shortuuid


def create_slug(length=6):
    return shortuuid.uuid()[:length]
