import os
from flask import Flask, send_file, render_template, request
from gif_maker.lake_animations import generate_lake_brite_gif, METRICS
from gif_maker.colormap_palettes import PALETTES

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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

if __name__ == '__main__':
    app.run(debug=True)
