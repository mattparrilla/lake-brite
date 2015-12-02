import os
from flask import Flask, send_file, render_template, request
from gif_maker.lake_animations import generate_lake_brite_gif
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', palettes=['jet', 'winter'], metrics=['Temperature', 'Dissolved Oxygen'])


@app.route('/image')
def image():
    return send_file('gif_maker/gif/lake-animation/temperature.gif', mimetype='image/gif')


@app.route('/lake-gif', methods=['POST'])
def lake_gif():
    if request.method == 'POST':
        metric = request.form['metric']
        palette = request.form['palette']
        duration = request.form['duration']
        print palette, metric
        return 'test'
       # json.loads({
       #     'metric': metric,
       #     'palette': palette,
       #     'duraiton': duration
       # })
    else:
        return 'hello'
    # generate_lake_brite_gif(metric, palette, duration)

if __name__ == '__main__':
    app.run(debug=True)