from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import cluster

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate the input
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('auth.login'))

        # Attempt to authenticate user
        user = cluster.authenticate_user(username, password)
        
        if user:
            # Store the user in the session
            session['user'] = {'username': username, 'department': user['department']}
            
            # Redirect based on user department
            if user['department'] == 'Admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user['department'] == 'Receiving':
                return redirect(url_for('receiving.receiving'))
            elif user['department'] == 'Picking':
                return redirect(url_for('picking.picking'))
            elif user['department'] == 'Shipping':
                return redirect(url_for('shipping.shipping'))
            else:
                flash('Invalid department.', 'error')
                return redirect(url_for('auth.login'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
