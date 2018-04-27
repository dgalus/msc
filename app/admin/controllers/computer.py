from .. import *

@app.route('/computer/aliases', methods=['GET'])
def aliases():
    return render_template('computer/aliases.html')

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
