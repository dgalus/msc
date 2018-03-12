import redis


try:
    conn = redis.StrictRedis(host='127.0.0.1', port=6379, password='foobared')
    print('Set Record:', conn.set("best_car_ever", "Tesla Model S"))
    print('Get Record:', conn.get("best_car_ever"))
    print('Delete Record:', conn.delete("best_car_ever"))
    print('Get Deleted Record:', conn.get("best_car_ever"))
except Exception as ex:
    print('Error:', ex)