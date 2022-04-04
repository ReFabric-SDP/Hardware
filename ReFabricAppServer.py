from flask import request
from flask import Flask
import ReFabric
from sys import argv

app = Flask(__name__)


@app.route("/app_sync", methods=['POST'])
def on_app_sync():
    """Sync the buckets from POSTed json from desktop app"""
    sync_data = request.get_json(force=True)
    ReFabric.on_app_sync(sync_data)
    return "synced!"


@app.route("/app_start")
def on_app_start():
    """Starts the whole system, this would effectively be the entry point"""
    ReFabric.start()
    return "Hello, World! ReFabric started"


@app.route("/app_stop")
def on_app_stop():
    ReFabric.stop()
    return "ReFabric stopped"


if __name__ == '__main__':
    ev3_addr = argv[1]
    vision_pi_addr = argv[2]
    ReFabric = ReFabric.ReFabric(ev3_addr, vision_pi_addr)
    app.run(host='0.0.0.0')
