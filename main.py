from flask import Flask, session, request, url_for, redirect, render_template, abort, send_file
from service import *
import config


app = Flask(__name__, static_url_path='/Clipboard/static')


@app.route('/Clipboard/')
def index():
    return render_template('index.html', type_list=CONTENT_TYPE)


@app.route('/Clipboard/', methods=['POST'])
def add():
    data_content = None
    data_content_type = None
    try:
        data_content = request.form['content']
        data_content_type = request.form['content_type']
    except KeyError:
        return render_template('error.html', code=400, message='Content is empty.'), 400
    data_sign = request.form.get('sign', None)
    data_password = request.form.get('password', None)
    data_file = request.files.get('upload_file', None)
    if data_sign == '':
        data_sign = None
    if data_password == '':
        data_password = None
    if data_file is not None and data_file.filename == '':
        data_file = None
    ip = request.remote_addr
    if data_content.strip() == '' and data_file is None:
        return redirect(url_for('index'))
    ret = RecordService.add(data_content, data_content_type, ip, data_sign, data_password, data_file)
    if ret is not None:
        return redirect(url_for('result', result_id=ret.id))
    else:
        return render_template('error.html', code=400, message='Some error occurred while creating record.'), 400


@app.route('/Clipboard/search/', methods=['POST'])
def search():
    return redirect(url_for('result', result_id=request.form['id']))


@app.route('/Clipboard/<int:result_id>/')
def result(result_id):
    item = RecordService.get(result_id)
    if item is None:
        return render_template('error.html', code=404, message='Record %s is not found.' % (result_id,)), 404
    if 'authenticate' not in session or session['authenticate'] is None:
        session['authenticate'] = []
    if item.password is not None and result_id not in session['authenticate']:
        return render_template('authenticate.html', item_id=int(item.id), error=False)
    else:
        return render_template('result.html', item=item.to_json(no_mongo_id=True, format_datetime=True), item_id=int(item.id))


@app.route('/Clipboard/<int:result_id>/', methods=['POST'])
def password_check(result_id):
    item = RecordService.get(result_id)
    if item is None:
        return render_template('error.html', code=404, message='Record %s is not found.' % (result_id,)), 404
    if 'authenticate' not in session or session['authenticate'] is None:
        session['authenticate'] = []
    if result_id in session['authenticate']:
        return render_template('result.html', item=item.to_json(no_mongo_id=True, format_datetime=True), item_id=int(item.id))
    else:
        pw = request.form.get('password', None)
        if pw is not None and pw == item.password:
            session['authenticate'].append(result_id)
            session['authenticate'] = session['authenticate']
            return render_template('result.html', item=item.to_json(no_mongo_id=True, format_datetime=True), item_id=int(item.id))
        else:
            return render_template('authenticate.html', item_id=int(item.id), error=True)


@app.route('/Clipboard/<int:result_id>/download/')
def download(result_id):
    item = RecordService.get(result_id)
    if item is None:
        return render_template('error.html', code=404, message='Record %s is not found.' % (result_id,)), 404
    if 'authenticate' not in session or session['authenticate'] is None:
        session['authenticate'] = []
    if item.password is None or result_id in session['authenticate']:
        if item.file_name is not None:
            return send_file(get_file_real_path(result_id), as_attachment=True, attachment_filename=item.file_name)
        else:
            return render_template('error.html', code=404, message='File of record %s is not found.' % (result_id,)), 404
    else:
        return render_template('error.html', code=401), 401


if __name__ == '__main__':
    app.secret_key = config.secret_key
    app.config['UPLOAD_FOLDER'] = get_file_real_path()
    app.config['MAX_CONTENT_LENGTH'] = config.file_uploads['max_size']
    if config.host is not None and config.port is not None:
        app.run(host=config.host, port=config.port, debug=config.debug)
    else:
        app.run(debug=config.debug)
