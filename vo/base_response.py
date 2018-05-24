# -*- coding: utf-8 -*-

from flask import Response
import json


class BaseResponse(Response):
    """
    BaseResponse
    """
    mimetype_json = 'application/json'
    response = None

    def __init__(self, response, status_code=200, message="success", mimetype=mimetype_json):
        response = {
            'status_code': status_code,
            'message': message,
            'data': response
        }
        self.response = json.dumps(response)
        json.loads(self.response)
        Response.__init__(self, response=self.response, status=200,
                          headers={"Content-type": mimetype})
