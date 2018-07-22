from flask import Flask, session, request, url_for, redirect, render_template, abort
from service import *
import config

# todo 添加密码验证
# todo 添加文件下载功能

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
        abort(400)
    data_sign = request.form.get('sign', None)
    data_password = request.form.get('password', None)
    data_file = request.files.get('upload_file', None)
    if data_sign == '':
        data_sign = None
    if data_password == '':
        data_password = None
    if data_file.content_type == '' or data_file.content_type == 'application/octet-stream':
        data_file = None
    ip = request.remote_addr
    ret = RecordService.add(data_content, data_content_type, ip, data_sign, data_password, data_file)
    if ret is not None:
        return "ok"
    else:
        abort(400)


@app.route('/Clipboard/search/', methods=['POST'])
def search():
    return redirect(url_for('result', result_id=request.form['id']))


@app.route('/Clipboard/<int:result_id>/')
def result(result_id):
    item = RecordService.get(result_id)
    if item is None:
        abort(404)
    return render_template('result.html', item=item, item_id=int(item['id']))


if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = config.file_uploads['max_size']
    app.run(host=config.host, port=config.port, debug=config.debug)
