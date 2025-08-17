from rest_framework.response import Response
import json


class ApiManager:
    """

    """

    def __init__(self):
        self.request = None
        self.body = None
        self.session = None

    def getBAFromSession(self):
        try:
            ba_id = self.session["user_context"]["ba_id"]
            return ba_id
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Yor are not registered as BA")
            raise e

    def getPhoneFromSession(self):
        try:
            return self.session["phone"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Could not fetch phone exists in session")
            raise e

    def getEmailFromSession(self):
        try:
            return self.session["email"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(e, "Yor are not Authenticated")
            raise e

    def getNameFromSession(self):
        try:
            return self.session["name"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Could not fetch name exists in session")
            raise e

    def getUserIdFromSession(self):
        try:
            user_id = self.session["user_id"]
            return user_id
        except KeyError as e:
            e.message = self.getKeyErrorMessage(e, "Yor are not Authenticated")
            raise e

    def setJsonEncodedBody(self, request):
        try:
            self.body = request.data
            self.session = request.session
        except Exception as e:
            
            raise KeyError()

    def returnSuccessResponse(self, message, status_code):
        return {"success": True, "status_code": 200, "message": message}

    def returnErrorResponse(self, message, status_code):
        return {
            "success": True,
            "status_code": status_code,
            "message": message}

    def getKeyErrorMessage(self, e, msg="Ops Somethings Went Wrong "):
        message = {
            "error": {
                "message": msg,
                "code": 4004,
                "status_code": 400,
                "developer_message": "Key error " + str(e)
            },
            "success": False
        }
        return message

    def getValueError(self, e, msg='Not Provided'):
        message = {"error": {
            "message": msg,
            "developer_message": "Value error " + str(e),
            "code": 4014,
            "status_code": 400
        },
            "success": False
        }
        return message

    def getIntegrityError(self, e, msg="Not Provided"):
        message = {"error": {
            "message": msg,
            "developer_message": str(e),
            "code": 4019,
            "status_code": 400
        },
            "success": False
        }
        return message

    def getObjNotExistError(self, e, msg="Not Provided"):
        message = {"error": {
            "message": msg,
            "developer_message": str(e),
            "code": 4010,
            "status_code": 400
        },
            "success": False
        }
        return message

    def getObjAlreadyExist(self, e, msg="Not Provided"):
        message = {"error": {
            "message": msg,
            "developer_message": str(e),
            "code": 4021,
            "status_code": 403
        },
            "success": False
        }
        return message

    def getRetailerFromSession(self, request):
        try:
            return request.session["user_context"]["retailer_id"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Yor are not registered as Retailer")
            raise e

    def getMandiFromSession(self, request):
        try:
            return request.session["user_context"]["retailer_id"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Yor are not registered as Retailer")
            raise e
