from flask import request
from flask import Flask
import ReFabric
from sys import argv

app = Flask(__name__)


@app.route("/app_sync", methods=['POST', 'GET'])
def on_app_sync():
    """Sync the buckets from POSTed json from desktop app"""
    # sync_data = request.get_json(force=True)
    sync_data = {"buckets": [{"activated": True, "colours": ["#1b770e"], "is misc": False},{"activated": True, "colours": ["#db1f86"], "is misc": False},{"activated": True, "colours": ["#f4cc10"], "is misc": False},{"activated": True, "colours": ["#0044f0"], "is misc": False},{"activated": True, "colours": ["#f03000"], "is misc": False},{"activated": True, "colours": [], "is misc": True}],"colour diff": 20}
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
    ev3_addr = "192.168.244.29"
    vision_pi_addr = "192.168.244.203"
    try:
        hardcode = bool(argv[3])
    except:
        hardcode = True
    ReFabric = ReFabric.ReFabric(ev3_addr, vision_pi_addr, hardcode)
    app.run(host='0.0.0.0')
