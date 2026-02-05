# common/protocol.py

def mcp_request(tool, params):
    return {
        "type": "request",
        "tool": tool,
        "params": params
    }


def mcp_response(status, data):
    return {
        "type": "response",
        "status": status,
        "data": data
    }
