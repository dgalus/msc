from .. import *

@app.route('/settings/web_panel', methods=['GET'])
def web_panel():
    config = json.load(open("config.json"))
    return render_template('settings/web_panel.html',
                           port=config['admin_panel']['port'],
                           username=config['admin_panel']['username'])

@app.route('/settings/email', methods=['GET'])
def email():
    config = json.load(open("config.json"))
    return render_template('settings/email.html')

@app.route('/settings/scanning', methods=['GET'])
def scanning():
    config = json.load(open("config.json"))
    return render_template('settings/scanning.html')

@app.route('/settings/websites', methods=['GET'])
def websites():
    config = json.load(open("config.json"))
    return render_template('settings/websites.html')

@app.route('/settings/zones', methods=['GET'])
def zones():
    config = json.load(open("config.json"))
    return render_template('settings/zones.html')

@app.route('/settings/system', methods=['GET'])
def system():
    config = json.load(open("config.json"))
    return render_template('settings/system.html')