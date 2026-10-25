from collections import defaultdict, deque
from threading import Lock
from time import time

from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)

# Vercel Functions have a 4.5 MB request/response payload limit.
# Keep each transfer below that limit.
DOWNLOAD_BYTES = 4 * 1024 * 1024  # 4 MiB
DOWNLOAD_DATA = bytes((i % 251 for i in range(DOWNLOAD_BYTES)))
MAX_UPLOAD_BYTES = 4 * 1024 * 1024
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

# Basic per-instance rate limiting only. Serverless instances do not share this memory.
request_times = defaultdict(deque)
rate_lock = Lock()
MAX_API_REQUESTS = 30
WINDOW_SECONDS = 60


@app.before_request
def limit_api_requests():
    if not request.path.startswith("/api/"):
        return None

    client_ip = request.remote_addr or "unknown"
    now = time()

    with rate_lock:
        events = request_times[client_ip]
        while events and now - events[0] > WINDOW_SECONDS:
            events.popleft()
        if len(events) >= MAX_API_REQUESTS:
            response = jsonify({"error": "Too many test requests. Wait a minute and try again."})
            response.status_code = 429
            return response
        events.append(now)
    return None


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/ping")
def ping():
    response = make_response(jsonify({"ok": True}))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.get("/api/download")
def download_test():
    response = make_response(DOWNLOAD_DATA)
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Length"] = str(len(DOWNLOAD_DATA))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.post("/api/upload")
def upload_test():
    body = request.get_data(cache=False)
    return jsonify({"received_bytes": len(body)})


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": "Upload test is limited to 4 MiB."}), 413


@app.errorhandler(429)
def too_many_requests(_error):
    return jsonify({"error": "Too many requests. Please wait and try again."}), 429


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
