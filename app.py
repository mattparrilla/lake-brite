import os
from flask import Flask, send_file, render_template, request
from gif_maker.lake_animations import generate_lake_brite_gif, METRICS
from gif_maker.colormap_palettes import PALETTES

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', palettes=PALETTES, metrics=METRICS)


@app.route('/image')
def image():
    return send_file('gif_maker/gif/lake-animation.gif', mimetype='image/gif')


@app.route('/save-image')
def save_image():
    return send_file('gif_maker/gif/lake-animation.gif', mimetype='image/gif', as_attachment=True)


@app.route('/lake-gif', methods=['POST'])
def lake_gif():
    if request.method == 'POST':
        metric = request.form['metric']
        palette = request.form['palette']
        duration = float(request.form['duration'])
        return generate_lake_brite_gif(metric, palette, duration)

if __name__ == '__main__':
    app.run(debug=True)
