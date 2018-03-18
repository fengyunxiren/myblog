from itertools import chain


def status_dict(data=None, result=True, status=0, message=None, **kwargs):
    if data is None:
        ret = {
            "result": result,
        }
        if result is False:
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


def model_to_dict(instance, fields=None, exclude=None):
    """
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        value = f.value_from_object(instance)
        if hasattr(value, "_meta"):
            data[f.name] = model_to_dict(value, exclude=exclude)
        elif isinstance(value, list):
            tmp_list = []
            for v in value:
                if hasattr(v, "_meta"):
                    tmp_list.append(model_to_dict(v, exclude=exclude))
                else:
                    tmp_list.append(v)
            data[f.name] = tmp_list
        else:
            data[f.name] = value
    return data
