
def status_dict(date=None, result=True, status=0, message=None, **kwargs):
    if data is None:
        ret = {
            "result": False,
            "status": status if status != 0 else -1,
            "message": message if message is not None else "request error!"
        }
    else:
        ret = {
            "result": result,
            "data": data,
            "status":status,
        }
        if message is not None:
            ret["message"] = message
        ret.update(kwargs)
    return ret