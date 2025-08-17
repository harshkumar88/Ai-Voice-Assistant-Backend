


class DefaultException(Exception):
    def __init__(self, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": 4070,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg
            },
            "success": False}

        self.message = message


class DefaultExceptionWithCode(Exception):
    def __init__(self, code, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": code,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg
            },
            "success": False}

        self.message = message


class UnAuthorisedException(Exception):

    def __init__(self, msg="Ops Something went wrong"):
        message = {
            "error": {
                "message": msg,
                "status_code": 401,
                "code": 4036,
                "developer_message": msg
            },
            "success": False
        }
        self.message = message

    def __str__(self):
        return repr(self.message)


class PermissionException(Exception):

    def __init__(self, msg="Authorization failes"):
        message = {
            "success": False,
            "error": {
                "message": msg,
                "code": 4037,
                "developer_message": "",
                "status_code": 403
            }
        }
        self.message = message

    def __str__(self):
        return repr(self.message)


class AuthException(Exception):

    def __init__(self, e):
        message = {
            "success": False,
            "message": "Authentication Failed by server " + str(e)
        }
        self.message = message

    def __str__(self):
        return repr(self.message)


class DefaultExceptionWithData(Exception):
    def __init__(self, data, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": 7080,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg,
                "callback": data
            },
            "success": False}

        self.message = message


class OndException(Exception):
    def __init__(self, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": 5070,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg,
                "popup": "POPUP_DICT"
            },
            "success": False}

        self.message = message


class TicketRaiseException(Exception):
    def __init__(self, data, msg=""):
        message = {
            "error": {
                "message": msg,
                "code": 7080,
                "status_code": 400,
                "developer_message": "Default Exception: " + msg,
                "data": data
            },
            "success": False}

        self.message = message
