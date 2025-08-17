from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Every Exception will go here
    and if the exception i user defined Exception
    then ok
    otherwise we will make our message 
    """

    a = exc.__dict__

    if a and isinstance(a, dict):
        message = a['message']
        try:
            status_code = a['message']["error"]["status_code"]
        except KeyError as e:
            import sentry_sdk
            sentry_sdk.capture_exception(exc)
            message = {
                "error": {
                    "message": "Oops Something went Wrong",
                    "code": 5003,
                    "developer_message": str(exc),
                    "status_code": 503
                },
                "success": False
            }
            status_code = 503

    else:
        import sentry_sdk
        sentry_sdk.capture_exception(exc)
        message = {
            "error": {
                "message": "Oops Something went Wrong",
                "code": 5003,
                "developer_message": str(exc),
                "status_code": 503
            },
            "success": False
        }
        status_code = 503

    return Response(message, status_code)
