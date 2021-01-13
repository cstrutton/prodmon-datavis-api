import timeit

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    abort
)

from flask_mysql_connector import MySQL

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config['MYSQL_USER'] = 'stuser'
app.config['MYSQL_DATABASE'] = 'prodrptdb'
app.config['MYSQL_HOST'] = '10.4.1.224'
app.config['MYSQL_PASSWORD'] = 'stp383'
mysql = MySQL(app)


def tuple_list_to_list(tl):
    return [item for t in tl for item in t]


def quote_string_list(string):
    return '"{0}"'.format('", "'.join(list(string.split(","))))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/machine', methods=['GET'])
@app.route('/machine/<part_number>', methods=['GET'])
def machines(part_number=None):
    sql = 'SELECT DISTINCT(Machine) FROM GFxPRoduction'

    if part_number:
        sql = sql + ' WHERE Part LIKE "{}"'.format(part_number)

    result = mysql.execute_sql(sql)
    return jsonify(tuple_list_to_list(result))


@app.route('/part', methods=['GET'])
@app.route('/part/<machine_number>', methods=['GET'])
def parts(machine_number=None):
    sql = 'SELECT DISTINCT(Part) FROM GFxPRoduction'

    if machine_number:
        sql = sql + ' WHERE Machine LIKE "{}"'.format(machine_number)

    result = mysql.execute_sql(sql)
    return jsonify(tuple_list_to_list(result))


# Returns a count of parts made on given machines within the time period
# parameters:
#   - machine: comma separated list of machines to include
#   - part: comma separated list of parts to include
#   - start: integer timestamp relative to GMT (Unix timestamp)
#   - interval: include all parts made from start to start+interval
#   - count: number of intervals to return

@app.route('/counts', methods=['GET'])
def counts():
    tic = timeit.default_timer()

    machine_numbers = request.args.get('machine', default=None, type=str)
    part_numbers = request.args.get('part', default=None, type=str)

    if not machine_numbers and not part_numbers:
        abort(400, 'Either the "machine" or the "part" parameter is required')

    start = request.args.get('start', default=None, type=int)
    if not start:
        abort(400, 'The "start" parameter is required')

    interval = request.args.get('interval', default=3600, type=int)
    count = request.args.get('count', default=1, type=int)

    sql_prefix = 'SELECT COUNT(PerpetualCount) '
    sql_prefix += 'FROM GFxPRoduction '
    if machine_numbers:
        sql_prefix += 'WHERE Machine IN ({}) '.format(quote_string_list(machine_numbers))
    if part_numbers:
        sql_prefix += 'AND Part IN ({}) '.format(quote_string_list(part_numbers))

    data = {}
    for i in range(count):
        period_start = start + (interval * i)
        period_end = period_start + interval
        sql = sql_prefix + 'AND TimeStamp BETWEEN {} AND {} '.format(period_start, period_end)
        result = mysql.execute_sql(sql)
        data[str(i)] = {'period': i,
                   'start': period_start,
                   'end': period_end,
                   'count': result[0][0]
                   }

    toc = timeit.default_timer()
    data['elapsed_time'] = toc - tic  # elapsed time in seconds

    return jsonify(data)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
