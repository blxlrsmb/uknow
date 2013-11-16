from flask import Blueprint, render_template, redirect

base = Blueprint('base', __name__)


@base.route('/')
def index():
    return render_template('index.jade')


@base.route('/err')
def error():
    raise Exception()
