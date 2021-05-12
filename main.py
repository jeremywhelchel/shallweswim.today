from flask import Flask, Response, redirect, render_template, url_for
import logging
import os

import data

# XXX
logging.getLogger().setLevel(logging.INFO)

data = data.Data()
data.Start()

app = Flask(__name__)


@app.route("/")
def index():
    current_time, current_temp = data.CurrentReading()
    past_tides, next_tides = data.PrevNextTide()
    return render_template(
        "index.html",
        current_time=current_time,
        current_temp=current_temp,
        past_tides=past_tides,
        next_tides=next_tides,
    )


@app.template_filter()
def fmt_datetime(timestamp):
    return timestamp.strftime("%A, %B %-d at %-I:%M %p")


@app.route("/plot")
def plot():
    plot = data.LiveTempPlot()
    return Response(plot, mimetype="image/svg+xml")


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"))


if __name__ == "__main__":
    logging.info("Running app.run()")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
