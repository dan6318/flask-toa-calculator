# Flask app
from flask import Flask, request, jsonify, render_template
from formula import RaidInputs, UniqueCalculations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calc")
def api_calc():
    inp = RaidInputs(request.args)
    result = UniqueCalculations().probability_calculator(inp)
    if not inp.party_points:
        inp.party_points = inp.personal_points
    return jsonify({
        "inputs": {
            "raid_level": inp.raid_level,
            "team_size": inp.team_size,
            "personal_points": inp.personal_points,
            "party_points": inp.party_points,
        },
        "results": result
    })

if __name__ == "__main__":
    app.run(debug=True)