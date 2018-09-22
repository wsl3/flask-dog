# encoding: utf8


from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from app.main.forms import NameForm
from app import db
from app.model import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['person'] = 'new'
        else:
            session['person'] = 'old'
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', name=session.get('name'), form=form)

