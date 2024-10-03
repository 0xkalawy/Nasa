from flask import Flask, render_template, request, jsonify
from landsatxplore.api import API
from datetime import datetime


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/landsat")
def landsat():
    return render_template("landsat.html")

@app.route("/fetch", methods=['POST'])
def fetch():
    # API Initialization
    
    # Get form data safely using .get() to avoid KeyError
    dataset = request.form.get('dataset')
    lat = request.form.get('latitude')
    lng = request.form.get('longitude')
    start_date = request.form.get('startDate')
    end_date = request.form.get('endDate')

    if not dataset or not lat or not lng or not start_date or not end_date:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        datetime_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        datetime_end_date = datetime.strptime(end_date, '%Y-%m-%d')
        min_date = datetime(1972, 1, 1)
        # Check if the dates are before January 1, 1972
        if  datetime_start_date < min_date or  datetime_end_date < min_date:
            return "Nice try, but Landsat launched in 1972 ;)"
        if datetime_end_date < datetime_start_date:
            return "How end date come before first date? XD"
    except ValueError:
        return "Invalid date format. Please use 'YYYY-MM-DD'."
    api = API("kalawy", "1072003Mm123.")
    # Search for Landsat scenes
    scenes = api.search(
        dataset=dataset,
        latitude=float(lat),
        longitude=float(lng),
        start_date=start_date,
        end_date=end_date
    )
    polygon_coords = [(coord[0], coord[1]) for coord in scenes[0]['spatial_coverage'].exterior.coords]
    api.logout()
    return jsonify({"html":render_template("data.html",**scenes[0]),
                    "coords":polygon_coords})

if __name__ == "__main__":
    app.run("0.0.0.0", port=1900,debug=True)
