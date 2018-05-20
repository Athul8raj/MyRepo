from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename
#from werkzeug.routing import BaseConverter


app = Flask(__name__)


# class ListConverter(BaseConverter):
#     def to_python(self, value):
#         return value.split('+')

#     def to_url(self, values):
#         return '+'.join(BaseConverter.to_url(value) for value in values)


#app.url_map.converters['list'] = ListConverter
UPLOAD_FOLDER = 'your/upload/path'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'xls', 'xlsx', 'doc', 'docx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['APP_SECRET_KEY'] = 'my_secret_key'


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('convert_dtypes'))
    return render_template('memory_usage.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/convert_dtypes')
def convert_dtypes():
    g1 = pd.read_csv('csv/filename', low_memory=False)
    for dtype in ['float64', 'int64', 'object']:
        selected_dtype = g1.select_dtypes(include=[dtype])
        if dtype == 'int64':
            converted_int = selected_dtype.apply(pd.to_numeric, downcast='unsigned')
        if dtype == 'float64':
            converted_float = selected_dtype.apply(pd.to_numeric, downcast='float')
        if dtype == 'object':
            converted_obj = pd.DataFrame()
            for col in selected_dtype.columns:
                num_unique_values = len(selected_dtype[col].unique())
                num_total_values = len(selected_dtype[col])
                if num_unique_values / num_total_values < 0.5:
                    converted_obj.loc[:, col] = selected_dtype[col].astype('category')
                else:
                    converted_obj.loc[:, col] = selected_dtype[col]
            converted_dtype = [converted_int, converted_float, converted_obj]
            for conv_dtype in converted_dtype:
                if isinstance(conv_dtype, pd.DataFrame):
                    usage_b = conv_dtype.memory_usage(deep=True).sum()
                else:
                    usage_b = conv_dtype.memory_usage(deep=True)
                usage_mb = usage_b / 1024 ** 2  # convert bytes to megabytes
            return render_template('mem_report.html', usage_mb=usage_mb)


if __name__ == '__main__':
    app.run(debug=True)
