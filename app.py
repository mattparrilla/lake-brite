import os
from flask import (
    Flask, send_file, render_template, request
)
from werkzeug import secure_filename
from gif_maker.lake_animations import generate_lake_brite_gif, METRICS
from gif_maker.colormap_palettes import PALETTES
from gif_maker.matrix_to_gif import normal_gif_to_lake_brite

UPLOAD_FOLDER = 'gif_maker/gif/uploads'
ALLOWED_EXTENSIONS = set(['gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html', palettes=PALETTES, metrics=METRICS)


@app.route('/lake-animation')
def lake_animation():
    return send_file('gif_maker/gif/lake-animation.gif', mimetype='image/gif')


@app.route('/save-lake-animation')
def save_lake_animation():
    return send_file('gif_maker/gif/lake-animation.gif', mimetype='image/gif', as_attachment=True)


@app.route('/lake-gif', methods=['POST'])
def lake_gif():
    if request.method == 'POST':
        metric = request.form['metric']
        palette = request.form['palette']
        duration = float(request.form['duration'])
        return generate_lake_brite_gif(metric, palette, duration)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/regular-gif')
def regular_gif():
    return send_file('gif_maker/gif/regular.gif', mimetype='image/gif')


@app.route('/save-regular-gif')
def save_regular_gif():
    return send_file('gif_maker/gif/regular.gif', mimetype='image/gif', as_attachment=True)


@app.route('/upload-gif', methods=['POST'])
def upload_gif():
    basedir = os.path.abspath(os.path.dirname(__file__))

    if request.method == 'POST':
        files = request.files['file']
        duration = float(request.form['gif-duration'])
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            updir = os.path.join(basedir, 'gif_maker/gif/uploads/')
            file_path = os.path.join(updir, filename)
            files.save(file_path)
            return normal_gif_to_lake_brite(file_path, duration)

if __name__ == '__main__':
    app.run(debug=True)
