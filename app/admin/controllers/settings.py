from .. import *

@app.route('/settings/web_panel', methods=['GET'])
def web_panel():
    return render_template('settings/web_panel.html')

@app.route('/settings/email', methods=['GET'])
def email():
    return render_template('settings/email.html')

@app.route('/settings/scanning', methods=['GET'])
def scanning():
    return render_template('settings/scanning.html')

@app.route('/settings/websites', methods=['GET'])
def websites():
    return render_template('settings/websites.html')

@app.route('/settings/zones', methods=['GET'])
def zones():
    return render_template('settings/zones.html')