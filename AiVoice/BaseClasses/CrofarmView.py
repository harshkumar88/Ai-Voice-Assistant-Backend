from rest_framework.response import Response
from rest_framework.views import APIView


class CrofarmView(APIView):

    def getResKeyValue(self, key, data):
        return Response({
            "success": True,
            key: data
        }, 200)

    def getResWithData(self, data):
        data.update({"success": True})
        return Response(
            data
            , 200)

    def getFailureWithData(self, data, response_code=200):
        data.update({"success": False})
        return Response(
            data,
            response_code
        )

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

    def getAgentFromSession(self):
        try:
            return self.request.session["user_context"]["agent_id"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Yor are not registered as Agent")
            raise e

    def getEUserFromSession(self):
        try:
            return self.request.session["user_context"]["eid"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(
                e, "Yor are not registered as Agent")
            raise e

    def getRequestHeaderData(self):
        meta_data = self.request.META
        device_id = meta_data.get('HTTP_UNIQUE_ID', '')
        if 'HTTP_APP_CLIENT' in meta_data and 'HTTP_APP_VERSION' in meta_data:
            return {
                'app_client': meta_data['HTTP_APP_CLIENT'],
                'app_vesion': meta_data['HTTP_APP_VERSION'],
                'device_id': device_id
            }
        else:
            return {
                'app_client': '',
                'app_vesion': '0',
                'device_id': device_id
            }

    def setJsonEncodedBody(self):
        try:
            self.body = self.request.data
            self.session = self.request.session
        except Exception as e:
            e.message = self.getKeyErrorMessage(str(e))
            raise e

    def getConsumerFromSession(self):
        try:
            return self.request.session["user_context"]["consumer_id"]
        except KeyError as e:
            e.message = self.getKeyErrorMessage(e, "You are not registered as Consumer")
            raise e

    def getAccessToken(self):
        try:
            access_token = self.request.META.get('HTTP_ACCESS_TOKEN', "")
            return access_token
        except KeyError as e:
            e.message = self.getKeyErrorMessage(e, "You are not registered as Consumer")
            raise e
