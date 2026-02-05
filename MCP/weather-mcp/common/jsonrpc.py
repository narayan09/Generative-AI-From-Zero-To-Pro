import json

def request(method, params, req_id=1):
    return json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": req_id
    })

def result(data, req_id):
    return json.dumps({
        "jsonrpc": "2.0",
        "result": data,
        "id": req_id
    })

def error(msg, req_id):
    return json.dumps({
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": msg},
        "id": req_id
    })
