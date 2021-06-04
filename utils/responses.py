from datetime import datetime
import json
import uuid

from django.http import HttpResponse


class UUJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, uuid.UUID):
            return o.hex
        elif isinstance(o, datetime):
            return o.timestamp()
        return super(UUJSONEncoder, self).default(o)


class HttpJsonResponse(HttpResponse):

    def __init__(self, data=None, encoder=None, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json; charset=utf-8')
        kwargs.setdefault('status', 200)
        encoder = encoder if encoder else UUJSONEncoder
        data = json.dumps(data, cls=encoder) if data is not None else ''
        super(HttpJsonResponse, self).__init__(content=data, *args, **kwargs)
