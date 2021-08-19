import json

from chalice import Response

from chalicelib.utils.CustomJsonEncoder import CustomJsonEncoder


class Responder(object):
    @staticmethod
    def success(payload, status_code=200):
        """
        Returns a Response denoting success.
        :param payload: the response payload
        :param status_code: the http status code to return (default:200)
        :return: Response
        """
        json_dict = {
            "status": {
                "success": True,
            },
            "result": payload
        }
        json_body = json.dumps(json_dict, cls=CustomJsonEncoder)
        return Response(
            body=json_body,
            status_code=status_code,
            headers={'Content-Type': 'application/json'}
        )

    @staticmethod
    def error(status_code, error_message="", payload=None):
        """
        Returns a Response denoting failure.
        :param status_code: the http status code to return
        :param error_message:
        :param payload: a result if any (default: None)
        :return:
        """
        json_dict = {
            "status": {
                "success": False,
                "error_message": error_message
            },
            "result": payload
        }
        json_body = json.dumps(json_dict)
        return Response(
            body=json_body,
            status_code=status_code,
            headers={'Content-Type': 'application/json'}
        )
