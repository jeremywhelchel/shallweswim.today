#!/usr/bin/env python3

from flask import Flask, jsonify, Response, redirect, render_template, url_for
import google.cloud.logging
import logging
import os

import data as data_lib

data = data_lib.Data()

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


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


@app.route("/freshness")
def freshness():
    return jsonify(data.Freshness())


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"))


# XXX This is used for gunicorn.
def start_app():
    # If running in Google Cloud Run, use cloud logging
    if 'K_SERVICE' in os.environ:
        # Setup Google Cloud logging
        # By default this captures all logs at INFO level and higher
        log_client = google.cloud.logging.Client()
        log_client.get_default_handler()
        log_client.setup_logging()
        logging.info('Using google cloud logging')
    else:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('Using standard logging')

    logging.info('Starting app')
    data.Start()
    return app


if __name__ == "__main__":  # Run Flask dev-server directly
    logging.info("Running app.run()")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
