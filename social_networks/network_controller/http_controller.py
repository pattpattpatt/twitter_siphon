# HTTP Server Interface for Dockerization

from flask import *
from social_networks.stream_controller.stream_interface import TweetStreamInterface

app = Flask(__name__)


@app.route('/stream/')
def rec_cmds():
    tsi = TweetStreamInterface()
    tsi.take_input(request.args)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
