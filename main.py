from flask import Flask, render_template, request, jsonify
from landsatxplore.api import API
from datetime import datetime
from skyfield.api import load, Topos
from skyfield.sgp4lib import EarthSatellite

app = Flask(__name__,)

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
    api.logout()
    try:
        polygon_coords = [(coord[0], coord[1]) for coord in scenes[0]['spatial_coverage'].exterior.coords]
        return jsonify({"html":render_template("data.html",**scenes[0]),
                    "coords":polygon_coords})
    except:
        return "<h1>No records Found :(</h1>"
@app.route("/when",methods=["POST"])
def when():
    lat = float(request.form.get('latitude'))
    lng = float(request.form.get('longitude'))
    
    # Landsat 7
    landsat7_tle_lines = [					
        '1 25682U 99020A   24277.93332473  .00003289  00000-0  67948-3 0  9998',
        '2 25682  97.8818 299.5785 0001593  80.2440  36.0495 14.60994277355017'
    ]
    satellite = EarthSatellite(landsat7_tle_lines[0], landsat7_tle_lines[1], 'Landsat 7', load.timescale())
    ts = load.timescale()
    observer = Topos(latitude_degrees=lat, longitude_degrees=lng)
    t0 = ts.now()
    t1 = ts.utc(t0.utc_datetime().year, t0.utc_datetime().month, t0.utc_datetime().day + 1)
    times, events = satellite.find_events(observer, t0, t1, altitude_degrees=30.0)

    
    #  Landsat 8
    landsat8_tle_lines = [
        '1 39084U 13008A   24278.18399940  .00002503  00000-0  56547-3 0  9992',
        '2 39084  98.2188 346.4235 0001322  95.0598 265.0752 14.57105069619284'
    ]
    satellite = EarthSatellite(landsat8_tle_lines[0], landsat8_tle_lines[1], 'Landsat 8', load.timescale())
    ts = load.timescale()
    observer = Topos(latitude_degrees=lat, longitude_degrees=lng)
    t0 = ts.now()
    t1 = ts.utc(t0.utc_datetime().year, t0.utc_datetime().month, t0.utc_datetime().day + 1)
    times, events = satellite.find_events(observer, t0, t1, altitude_degrees=30.0)

    # Landsat 9
    landsat9_tle_lines = [
        '1 49260U 21088A   24278.21838193  .00002638  00000-0  59532-3 0  9994',
        '2 49260  98.2216 346.4546 0001336  91.8042 268.3309 14.57114917160569'
    ]
    satellite = EarthSatellite(landsat9_tle_lines[0], landsat9_tle_lines[1], 'Landsat 9', load.timescale())
    ts = load.timescale()
    observer = Topos(latitude_degrees=lat, longitude_degrees=lng)
    t0 = ts.now()
    t1 = ts.utc(t0.utc_datetime().year, t0.utc_datetime().month, t0.utc_datetime().day + 1)
    times, events = satellite.find_events(observer, t0, t1, altitude_degrees=30.0)


    for ti, event in zip(times, events):
        name = ('rise above 30°', 'culminate', 'set below 30°')[event]
        return f'{ti.utc_iso()} {name}'

if __name__ == "__main__":
    app.run("0.0.0.0", port=1900,debug=True)
