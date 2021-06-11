from bson import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, ObjectId):
            return str(object)
        return json.JSONEncoder.default(self, object)
