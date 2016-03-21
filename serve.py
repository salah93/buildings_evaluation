from flask import (jsonify, Flask,
                   render_template, request)
from invisibleroads_macros import security
from nearby import geomap


app = Flask(__name__)


# Making an API endpoint (GET)
@app.route('/_get_points')
def get_points():
    address = request.args.get('address', "")
    search_query = request.args.get('search_query', "")
    results = geomap(address, search_query)
    print(results)
    return jsonify(address=results['address'],
                   points=results['points'])


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # flask
    app.secret_key = security.make_random_string(10)
    app.run(port=27973, debug=True)
