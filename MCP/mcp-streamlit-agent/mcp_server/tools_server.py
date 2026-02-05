import sys, json, sqlite3, requests
from common.jsonrpc import result, error
from bs4 import BeautifulSoup

DB_PATH = "db/data.db"

TOOLS = [
    {
        "name": "db.search",
        "description": "Search employee information from SQLite database",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keyword like name, role, or location"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "web.search",
        "description": "Search information from the internet",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for internet lookup"
                }
            },
            "required": ["query"]
        }
    }
]

def list_tools(req_id):
    return result(TOOLS, req_id)


def db_search(params, req_id):
    keyword = params.get("query", "")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, role, location FROM employees
    WHERE name LIKE ? OR role LIKE ? OR location LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()
    conn.close()

    return result(rows, req_id)


def web_search(params, req_id):
    query = params.get("query", "")
    url = f"https://duckduckgo.com/html/?q={query}"

    html = requests.get(url, timeout=5).text
    soup = BeautifulSoup(html, "html.parser")
    print(f"html {html}")
    titles = [a.text for a in soup.select(".result__a")[:5]]

    return result(titles, req_id)



def main():
    raw = sys.stdin.read()
    req = json.loads(raw)

    method = req.get("method")
    params = req.get("params")
    req_id = req.get("id")

    if method == "tools.list":
        print(list_tools(req_id))
    elif method == "db.search":
        print(db_search(params, req_id))
    elif method == "web.search":
        print(web_search(params, req_id))
    else:
        print(error("Unknown tool", req_id))


if __name__ == "__main__":
    main()
