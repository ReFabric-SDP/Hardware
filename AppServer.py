from flask import request
from flask import Flask
import match_to_bin
import distance_sensor

app = Flask(__name__)


@app.route("/app_sync", methods=['POST'])
def on_app_sync():
    """Sync the buckets from POSTed json from desktop app"""
    sync_data = request.get_json(force=True)
    match_to_bin.from_app = sync_data
    return "OK, server for vision got data"


@app.route("/do_classification")
def on_do_classification():
    """The arm should call this and use the returned value as bucket number
    Webcam should take a picture, do all the processing"""
    bucket_number = match_to_bin.match_to_bin()
    print("bucket classified:", bucket_number)
    return str(bucket_number)


@app.route("/get_pickup_action")
def on_get_pickup_action():
    """The arm should call this and use the returned value as action for arduino"""
    action = sensor.get_pickup_action()
    print("decided pickup action:", action.name)
    return str(int(action))


if __name__ == '__main__':
    sensor = distance_sensor.Sensor()
    app.run(host='0.0.0.0')
