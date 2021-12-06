from rest_framework.response import Response
import re


def validate_keys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys


def validate_empty_str(value):
    return len(value.strip()) > 0


def http_response(msg, status, data=None, error_code=None):

    if data is None:
        data = {}
    success = True
    responseData = dict(
        success=success,
        message=msg,
        data=data,
    )
    if error_code:
        success = False
        responseData['success'] = success
        responseData['error_code'] = error_code

    return Response(responseData, status=status)


def validate_email_format(email):
    emailPattern = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'

    if re.search(emailPattern, email):
        return True

    return False
