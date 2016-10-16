from flask import session, redirect, url_for, flash
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin' in session and session['admin']:
            return f(*args, **kwargs)
        flash('You must be an admin to access that page.')
        return redirect(url_for('admin.login'))
    return decorated
