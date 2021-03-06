import os
from flask import request, redirect
from flask_login import login_required
from werkzeug.utils import secure_filename
import time
from src.login import *

from src.database import engine
from src.extensions import allowed_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../input/')

full_api = Blueprint('full_api', __name__)


@full_api.route('/full', methods=['POST'])
@login_required
def upload():
        f = request.files['full_video']
        user = current_user
        #parser = reqparse.RequestParser()
        #parser.add_argument('user_id', type=str)
        #args = parser.parse_args()

        user_id = user.get_id()
        result = engine.execute("select * from full where user_id=%s", user_id)
        i: int = 1
        for x in result:
            i = i+1

        fname = "full0"+str(user_id)+"0"+str(i)+".mp4"

        path = UPLOAD_FOLDER + fname

        full_video = fname
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        storage_path = '/input/'+fname

        if allowed_file(f.filename):
            f.save(path)
            size = os.stat(path).st_size
            engine.execute("insert into full (full_video,date,size,storage_path, user_id) "
                           "values (%s, %s, %s, %s, %s)", full_video, date, size, storage_path, user_id)

            return "ok"
        else:
            return "error"


@full_api.route('/full', methods=['GET'])
@login_required
def full_list():
    user_id = current_user
    result = engine.execute("select * from full where user_id=%s",user_id.get_id())
    return render_template('full.html', datas=result, mimetype='application/json')


@full_api.route('/full/<id>', methods=['GET'])
def show(id):
    result = engine.execute("select * from full where id=%s",id)

    return render_template('full_update.html', datas=result)


@full_api.route('/full/<id>', methods=['POST'])
def update(id):
    parser = reqparse.RequestParser()
    parser.add_argument('full_video', type=str)
    parser.add_argument('date', type=str)
    parser.add_argument('size', type=str)
    parser.add_argument('storage_path', type=str)
    parser.add_argument('user_id', type=str)
    args = parser.parse_args()

    full_video = args['full_video']
    date = args['date']
    size = args['size']
    storage_path = args['storage_path']
    user_id = args['user_id']

    engine.execute("update full set date=%s,size=%s,user_id=%s where id=%s", date, size, user_id, id)
    return redirect("/api/full")


@full_api.route('/full/delete/<id>', methods=['GET'])
def delete(id):
    engine.execute("delete from full where id=%s", id)
    return redirect("/api/full")

