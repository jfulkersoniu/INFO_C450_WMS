from flask import Flask, session, redirect, url_for, flash, render_template
from blueprints.admin import admin_bp
from blueprints.picking import picking_bp
from blueprints.receiving import receiving_bp
from blueprints.shipping import shipping_bp
from blueprints.auth import auth_bp

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(picking_bp, url_prefix='/picking')
app.register_blueprint(receiving_bp, url_prefix='/receiving')
app.register_blueprint(shipping_bp, url_prefix='/shipping')
app.register_blueprint(auth_bp, url_prefix='/auth')

def check_user_permission(required_department=None):
    if 'user' not in session:
        flash('You need to log in first.', 'error')
        return False
    department = session['user']['department']
    if department == 'Admin' or department == required_department:
        return True
    flash("You do not have permission to access that page and have been redirected to your department's function. If you believe you have received this message in error, contact your manager.", 'error')
    return False

@app.route('/')
@app.route('/')
def index():
    if 'user' in session:
        department = session['user']['department']
        if department == 'Admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif department == 'Receiving':
            return redirect(url_for('receiving.receiving'))
        elif department == 'Picking':
            return redirect(url_for('picking.picking'))
        elif department == 'Shipping':
            return redirect(url_for('shipping.shipping'))
        else:
            flash('You do not have access to any pages.', 'error')
            return redirect(url_for('auth.login'))
    return redirect(url_for('auth.login'))

@app.route('/admin')
def admin_dashboard():
    if check_user_permission('Admin'):
        return render_template('admin.html')
    return redirect(url_for('auth.login'))

@app.route('/receiving')
def receiving():
    if check_user_permission('Receiving') or check_user_permission('Admin'):
        return render_template('receiving.html')
    return redirect(url_for('auth.login'))

@app.route('/picking')
def picking():
    if check_user_permission('Picking') or check_user_permission('Admin'):
        return render_template('picking.html')
    return redirect(url_for('auth.login'))

@app.route('/shipping')
def shipping():
    if check_user_permission('Shipping') or check_user_permission('Admin'):
        return render_template('shipping.html')
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
