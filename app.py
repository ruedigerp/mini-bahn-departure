import requests
import json
from urllib.parse import quote
from flask import Flask, render_template
from config import locations, remote_api, remote_api_params


app = Flask(__name__)

urls = []
for location in locations:
    location_encoded = quote(location) + '.json'
    urls.append((location, f'{remote_api}{location_encoded}?{remote_api_params}'))


@app.route("/")
def main():
    global urls
    next_lines = []
    context = []
    for location, url in urls:
        next_lines = json.loads(requests.get(url).text).get('raw')
        lines = []
        for line in next_lines[:5]:
            current = {}
            current['name'] = line.get('line')
            current['route'] = line.get('destination')
            current['time'] = line.get('countdown')
            current['type'] = line.get('type')
            delay = line.get('delay')
            if delay and int(delay) > 0:
                current['delay'] = delay
            lines.append(current)
        context.append({'loc': location, 'lines': lines})

    return render_template('main.html', context=context)
