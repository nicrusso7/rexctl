from threading import Thread

from flask import Flask, request, jsonify
from control_unit.rex_daemon import RexDaemon

from logging.config import dictConfig

# setup uwsgi logger
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)
# bootstrap rex daemons
rex_daemon = RexDaemon()


# ROUTES
@app.route('/status')
def status():
    global rex_daemon
    res = {}
    for d in rex_daemon.DAEMONS_MAP.keys():
        res[d] = 'active'
    return jsonify(res)


@app.route('/exec', methods=['POST'])
def exec():
    global rex_daemon
    cmd = request.json
    thread = Thread(target=rex_daemon.exec, args=(cmd,))
    thread.daemon = True
    thread.start()
    return jsonify({200: 'command sent.'})


@app.route('/stop_all')
def stop_all():
    global rex_daemon
    rex_daemon.stop_all()
    return jsonify({200: 'command sent.'})


@app.route('/debug_pose')
def debug_pose():
    global rex_daemon
    rex_daemon.debug_pose()
    return jsonify({200: 'command sent.'})


@app.route('/get_calibration')
def calibration():
    global rex_daemon
    data = rex_daemon.get_calibration()
    sys, gyro, accel, mag = data[0]
    mode = data[1]
    res = {'system': sys, 'gyroscope': gyro, 'accelerometer': accel, 'magnetometer': mag, 'mode': mode}
    return jsonify(res)


@app.route('/store_calibration')
def store_calibration():
    global rex_daemon
    rex_daemon.store_calibration()
    return jsonify({200: 'command sent.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
