from .. import *

@app.route('/computer/aliases', methods=['GET'])
def aliases():
    computers = db.session.query(Computer).all()
    return render_template('computer/aliases.html', computers=computers)

@app.route('/computer/show', methods=['GET'])
def show():
    comps = db.session.query(Computer).all()
    computers = []
    for c in comps:
        d = {}
        d["alias"] = c.alias
        d['ip'] = c.ip
        if c.geolocations:
            d['geolocations'] = str(json.loads(c.geolocations)["geolocations"])
        d['open_ports'] = c.open_ports
        d['closed_ports'] = c.closed_ports
        d['last_active'] = c.last_active
        d['last_ping'] = c.last_ping_response_timestamp
        d['last_port_scan'] = c.last_port_scan
        if c.most_connected_ports:
            d['most_connected'] = str(json.loads(c.most_connected_ports)["ports"])
        computers.append(d)
    return render_template('computer/show.html', computers=computers)

@app.route('/computer/most_visited', methods=['GET'])
def most_visited():
    return render_template('computer/most_visited.html')

@app.route('/computer/geolocations', methods=['GET'])
def geolocations():
    return render_template('computer/geolocations.html')

@app.route('/computer/protocols', methods=['GET'])
def protocols():
    return render_template('computer/protocols.html')

@app.route('/computer/active_use_times', methods=['GET'])
def active_use_times():
    return render_template('computer/active_use_times.html')

@app.route('/computer/test', methods=['GET'])
def test():
    return render_template('computer/test.html')