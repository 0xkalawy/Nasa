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
    
    # Search for Landsat scenes
    scenes = api.search(
        dataset='landsat_tm_c2_l1',
        latitude=50.85,
        longitude=-4.35,
        start_date='1995-01-01',
        end_date='1995-10-01',
        max_cloud_cover=10
    )
    
    print(f"{len(scenes)} scenes found.")
    
    # Process the results
    for scene in scenes:
        print(scene['acquisition_date'].strftime('%Y-%m-%d'))
        # Write scene footprints to disk
        fname = f"{scene['landsat_product_id']}.geojson"
        with open(fname, "w") as f:
            json.dump(scene['spatial_coverage'].__geo_interface__, f)
        
        # Remove file using os.remove() for cross-platform compatibility
        os.remove(fname)
    
    api.logout()
    return jsonify({"message": f"{len(scenes)} scenes processed."})

if __name__ == "__main__":
    app.run("0.0.0.0", port=1900)
