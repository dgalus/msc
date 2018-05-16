from .. import *
import uuid
import numpy as np
import matplotlib.pyplot as plt

@app.route('/layer3/overall_traffic', methods=['GET'])
def l3_overall_traffic():
    res = db.session.query(Counter.l3_traffic, Counter.l3_frames).order_by(Counter.id.desc()).all()
    traffic = []
    frames = []
    for r in res:
        traffic.append(r[0]/1000)
        frames.append(r[1]/1000)
    season_length = config["system"]["traffic_amount_anomaly_detection_model"]["season_length"]
    if len(traffic) > season_length:
        traffic = traffic[-season_length:]
    if len(frames) > season_length:
        frames = frames[-season_length:]
        
    x = range(len(traffic))
    y = traffic
    filename1 = str(uuid.uuid4()) + '.svg'
    plt.xlabel('Time')
    plt.ylabel('Traffic amount [kbps]')
    plt.plot(x, y, linewidth=0.5)
    plt.savefig(UPLOAD_FOLDER + filename1, format='svg')
    plt.clf()
    
    x = range(len(frames))
    y = frames
    filename2 = str(uuid.uuid4()) + '.svg'
    plt.xlabel('Time')
    plt.ylabel('Packets')
    plt.plot(x, y, linewidth=0.5)
    plt.savefig(UPLOAD_FOLDER + filename2, format='svg')
    plt.clf()
    return render_template('layer3/overall_traffic.html', 
                l3_traffic="img/" + filename1,
                l3_frames="img/" + filename2)

@app.route('/layer3/ip', methods=['GET'])
def ip():
    res = db.session.query(Counter.ip).order_by(Counter.id.desc()).all()
    packets = []
    for r in res:
        packets.append(r[0]/1000)
    season_length = config["system"]["traffic_amount_anomaly_detection_model"]["season_length"]
    if len(packets) > season_length:
        packets = packets[-season_length:]
        
    x = range(len(packets))
    y = packets
    filename1 = str(uuid.uuid4()) + '.svg'
    plt.xlabel('Time')
    plt.ylabel('Packets amount')
    plt.plot(x, y, linewidth=0.5)
    plt.savefig(UPLOAD_FOLDER + filename1, format='svg')
    plt.clf()
    return render_template('layer3/ip.html', img="img/" + filename1)

@app.route('/layer3/other', methods=['GET'])
def other():
    res = db.session.query(Counter.arp).order_by(Counter.id.desc()).all()
    packets = []
    for r in res:
        packets.append(r[0]/1000)
    season_length = config["system"]["traffic_amount_anomaly_detection_model"]["season_length"]
    if len(packets) > season_length:
        packets = packets[-season_length:]
        
    x = range(len(packets))
    y = packets
    filename1 = str(uuid.uuid4()) + '.svg'
    plt.xlabel('Time')
    plt.ylabel('Packets amount')
    plt.plot(x, y, linewidth=0.5)
    plt.savefig(UPLOAD_FOLDER + filename1, format='svg')
    plt.clf()
    return render_template('layer3/other.html', img="img/" + filename1)