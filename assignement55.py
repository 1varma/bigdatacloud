from flask import Flask, request, jsonify
import pymysql
import time

app = Flask(__name__)

db_config = {
    'host': 'mysql.clarksonmsda.org',
    'port': 3306,
    'user': 'ia626',
    'password': 'ia626clarkson',
    'db': 'ia626',
    'autocommit': True
}

def validate_key(key):
    return key == "123"

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/getData', methods=['GET'])
def get_data():
    start_time = time.time()
    key = request.args.get('key')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if not validate_key(key):
        return jsonify({'code': 0, 'msg': 'Invalid Key', 'req': 'getData', 'sqltime': 0})

    if not start_date or not end_date:
        return jsonify({'code': 0, 'msg': 'Start and end date required', 'req': 'getData', 'sqltime': 0})

    query = """
        SELECT * FROM `class_datapoints` 
        WHERE `date_time` BETWEEN %s AND %s
        ORDER BY `date_time` LIMIT 500;
    """
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as curr:
            curr.execute(query, (start_date, end_date))
            result = curr.fetchall()
        return jsonify({
            "code": 1,
            "msg": 'Success',
            "req": "getData",
            "sqltime": round(time.time() - start_time, 4),
            "data": result
        })
    except pymysql.Error as err:
        return jsonify({'code': 0, 'msg': f'Database error: {err}', 'req': 'getData', 'sqltime': 0})
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/countInPolygon', methods=['GET'])
def count_in_polygon():
    start_time = time.time()
    key = request.args.get('key')
    polygon = request.args.get('polygon')

    if not validate_key(key):
        return jsonify({'code': 0, 'msg': 'Invalid Key', 'req': 'countInPolygon', 'sqltime': 0})

    if not polygon:
        return jsonify({'code': 0, 'msg': 'Polygon coordinates required', 'req': 'countInPolygon', 'sqltime': 0})

    print(polygon)

    polygon_wkt = f'Polygon(({polygon}))'

    query = """
        SELECT COUNT(*) as count FROM `class_datapoints` 
        WHERE ST_WITHIN(geo_point, ST_GeomFromText(%s, 0));
    """
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as curr:
            curr.execute(query, (polygon_wkt,))  
            result = curr.fetchone()
        return jsonify({
            "code": 1,
            "msg": 'Success',
            "req": "countInPolygon",
            "sqltime": round(time.time() - start_time, 4),
            "count": result['count']
        })
    except pymysql.Error as err:
        return jsonify({'code': 0, 'msg': f'Database error: {err}', 'req': 'countInPolygon', 'sqltime': 0})
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/getAvgSpeedByFlight', methods=['GET'])
def get_avg_speed_by_flight():
    start_time = time.time()
    key = request.args.get('key')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if not validate_key(key):
        return jsonify({'code': 0, 'msg': 'Invalid Key', 'req': 'getAvgSpeedByFlight', 'sqltime': 0})

    query = """
        SELECT AVG(gs) as avg_speed, `flight_num` 
        FROM `class_datapoints` 
        WHERE `date_time` BETWEEN %s AND %s 
        GROUP BY `flight_num` 
        ORDER BY `flight_num` 
        LIMIT 500;
    """
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as curr:
            curr.execute(query, (start_date, end_date))
            result = curr.fetchall()
        return jsonify({
            "code": 1,
            "msg": 'Success',
            "req": "getAvgSpeedByFlight",
            "sqltime": round(time.time() - start_time, 4),
            "data": result
        })
    except pymysql.Error as err:
        return jsonify({'code': 0, 'msg': f'Database error: {err}', 'req': 'getAvgSpeedByFlight', 'sqltime': 0})
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)