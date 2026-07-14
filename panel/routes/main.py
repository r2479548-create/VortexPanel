from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('storefront.html')

@main_bp.route('/admin')
def admin():
    return render_template('admin.html')
