from flask import Flask, render_template, request, jsonify
import json
import os
from landsatxplore.api import API

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
    api = API("kalawy", "1072003Mm123.")
    
    # Get form data safely using .get() to avoid KeyError
    dataset = request.form.get('dataset')
    lat = request.form.get('latitude')
    lng = request.form.get('longitude')
    start_date = request.form.get('startDate')
    end_date = request.form.get('endDate')

    if not dataset or not lat or not lng or not start_date or not end_date:
        return jsonify({"error": "Missing required parameters"}), 400

    # Search for Landsat scenes
    scenes = api.search(
        dataset=dataset,
        latitude=float(lat),
        longitude=float(lng),
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=10
    )

    results = []
    # Process the results
    for scene in scenes:
        results.extend(scene.values())
        # Write scene footprints to disk
        fname = f"{scene['landsat_product_id']}.geojson"
        with open(fname, "w") as f:
            json.dump(scene['spatial_coverage'].__geo_interface__, f)
        
        os.remove(fname)
    
    api.logout()
    return jsonify({"message": f"{results}"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=1900,debug=True)
