from uuid import uuid1


def new_uuid():
    uuid = uuid1()
    return str(uuid)


if __name__ == '__main__':
    new_uuid()
