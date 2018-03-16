
def status_dict(data=None, result=True, status=0, message=None, **kwargs):
    if data is None:
        ret = {
            "result": result,
        }
        if ret is False:
            ret["status"] = status if status != 0 else -1
            ret["message"] = message if message is not None\
                else "request error!"
        else:
            ret["status"] = status
            if message is not None:
                ret["message"] = message
    else:
        ret = {
            "result": result,
            "data": data,
            "status": status,
        }
        if message is not None:
            ret["message"] = message
        ret.update(kwargs)
    return ret
