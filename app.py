import os

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
)


@app.route("/")
def hello():
    count = cache.incr("visitas")
    return f"A API foi acedida {count} vezes."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
