from rest_framework import status
from rest_framework.response import Response


def success_response(key="object", data=None, status=status.HTTP_200_OK):
    return Response(
        {"status": "success", "data": ({key: data} if data else None)}, status=status
    )


def fail_response(errors, status=status.HTTP_400_BAD_REQUEST):
    valid_errors = {
        key: value if type(value) != list and len(value) != 1 else value[0]
        for key,value in errors.items()
    }

    return Response({"status": "fail", "data": valid_errors}, status=status)


def error_response(message, status=status.HTTP_404_NOT_FOUND):
    return Response({"status": "error", "message": message}, status=status)
