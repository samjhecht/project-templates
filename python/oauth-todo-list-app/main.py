import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="*")

_TODOS = {}

@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    print(request.headers)
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("manifest.json") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")

@app.get("/oauth")
async def oauth():
    query_string = request.query_string.decode('utf-8')
    parts = query_string.split('&')
    kvps = {}
    for part in parts:
        k, v = part.split('=')
        v = v.replace("%2F", "/").replace("%3A", ":")
        kvps[k] = v
    print("OAuth key value pairs from the ChatGPT Request: ", kvps)
    url = kvps["redirect_uri"] + f"?code={OPENAI_CODE}"
    print("URL: ", url)
    return quart.Response(
        f'<a href="{url}">Click to authorize</a>'
    )

# Sample names
OPENAI_CLIENT_ID = "id"
OPENAI_CLIENT_SECRET = "secret"
OPENAI_CODE = "abc123"
OPENAI_TOKEN = "def456"

@app.post("/auth/oauth_exchange")
async def oauth_exchange():
    request = await quart.request.get_json(force=True)
    print(f"oauth_exchange {request=}")

    if request["client_id"] != OPENAI_CLIENT_ID:
        raise RuntimeError("bad client ID")
    if request["client_secret"] != OPENAI_CLIENT_SECRET:
        raise RuntimeError("bad client secret")
    if request["code"] != OPENAI_CODE:
        raise RuntimeError("bad code")

    return {
        "access_token": OPENAI_TOKEN,
        "token_type": "bearer"
    }

def main():
    app.run(debug=True, host="0.0.0.0", port=5002)

if __name__ == "__main__":
    main()