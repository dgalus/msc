from .. import *

@app.route('/', methods=['GET'])
def index():
    sessions = db.session.query(TCPSession).filter(TCPSession.is_active == True).count()
    l2_traffic = db.session.query(Counter.l2_traffic).order_by(Counter.id.desc()).first()[0]
    alerts = db.session.query(Alert).filter(Alert.admin_delete==False).count()
    
    current_tasks = []
    apt = db.session.query(AdminPendingTask).filter(AdminPendingTask.decision == None).order_by(AdminPendingTask.id.desc()).all()
    for at in apt:
        d = {}
        d['timestamp'] = at.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        task = json.loads(at.task)
        if task['task'] == 'add_new_safe_port':
            d['type'] = 'Add new safe port'
            d['description'] = 'Do you want to add port ' + str(task['port']) + ' to list of safe ports?'
        elif task['task'] == 'add_new_safe_geolocation':
            d['type'] = 'Add new safe geolocation'
            d['description'] = 'Do you want to add ' + str(task['geolocation']) + ' to list of safe geolocations?'
        current_tasks.append(d)
    
    archived_tasks_db = db.session.query(AdminPendingTask).filter(AdminPendingTask.decision != None).all()
    archived_tasks = []
    for at in archived_tasks_db:
        d = {}
        d['finished'] = at.finished_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        task = json.loads(at.task)
        if task['task'] == 'add_new_safe_port':
            d['type'] = 'Add new safe port'
            d['description'] = 'Do you want to add port ' + str(task['port']) + ' to list of safe ports?'
        elif task['task'] == 'add_new_safe_geolocation':
            d['type'] = 'Add new safe geolocation'
            d['description'] = 'Do you want to add ' + str(task['port']) + ' to list of safe geolocations?'
        d['decision'] = "YES" if at.decision == True else "NO"
        archived_tasks.append(d)
    
    return render_template('index/index.html', 
                sessions=sessions, 
                l2_traffic=l2_traffic/1000, 
                alerts=alerts, 
                apt=len(apt),
                current_tasks=current_tasks,
                archived_tasks=archived_tasks
            )