#!/usr/bin/env python3

from flask import Blueprint, request, render_template, flash, session, redirect, url_for

from utils import decorators, pwhash
from database import AdminUser

admin = Blueprint('admin', __name__)

@admin.route('/', methods=['GET'])
@decorators.admin_required
def home():
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = AdminUser.get(AdminUser.username == username)
            if pwhash.verify(password, user.password):
                session['admin'] = username
                return redirect(url_for('.home'))
        except AdminUser.DoesNotExist:
            pass

        flash('Username/password are incorrect.')
        return render_template('admin/login.html')

    else:
        if 'admin' in session and session['admin']:
            flash('Warning: you are already logged in as {}'.format(session['admin']))
        return render_template('admin/login.html')


@admin.route('/logout', methods=['GET'])
@decorators.admin_required
def logout():
    session.pop('admin', None)
    return redirect(url_for('.login'))
