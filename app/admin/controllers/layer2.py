from .. import *
import uuid
import numpy as np
import matplotlib.pyplot as plt

@app.route('/layer2/overall_traffic', methods=['GET'])
def l2_overall_traffic():
    res = db.session.query(Counter.l2_traffic, Counter.l2_frames).order_by(Counter.id.desc()).all()
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
    plt.ylabel('Frames')
    plt.plot(x, y, linewidth=0.5)
    plt.savefig(UPLOAD_FOLDER + filename2, format='svg')
    plt.clf()    
    return render_template('layer2/overall_traffic.html', 
                l2_traffic="img/" + filename1,
                l2_frames="img/" + filename2)