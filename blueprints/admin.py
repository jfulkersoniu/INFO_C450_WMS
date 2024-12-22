from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import cluster

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET', 'POST'])
def admin_dashboard():
    # Check if user is logged in
    if 'user' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))
    
    # Extract user information from session
    username = session['user']['username']
    department = session['user']['department']

    # Restrict access to Admin users only
    if department != 'Admin':
        flash("You do not have permission to access that page and have been redirected to your department's function. If you believe you have received this message in error, contact your manager.", 'error')
        return redirect(url_for('index'))  # Redirect to home or another authorized page

    if request.method == 'POST':
        # Trigger order generation
        cluster.generate_test_orders()
        flash('Test orders generated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin.html', username=username, department=department)

@admin_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # Check if user is logged in
    if 'user' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('auth.login'))
    
    # Extract user information from session
    username = session['user']['username']
    department = session['user']['department']
    
    # Restrict access to Admin users only
    if department != 'Admin':
        flash("You do not have permission to access that page and have been redirected to your department's function. If you believe you have received this message in error, contact your manager.", 'error')
        return redirect(url_for('index'))  # Redirect to home or another authorized page
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        department = request.form.get('department')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate inputs
        if not username or not department or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('admin.create_user'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('admin.create_user'))
        
        # Call the create_user function from cluster.py to store the user
        result = cluster.create_user(username, department, password)
        
        # Flash success or error message based on the result
        if result['status'] == 'success':
            flash(result['message'], 'success')
        else:
            flash(result['message'], 'error')
        
        return redirect(url_for('admin.create_user'))
    
    return render_template('create_user.html', username=username, department=department)
