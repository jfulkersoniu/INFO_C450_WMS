from flask import Blueprint, request, render_template, flash, redirect, url_for
import cluster

receiving_bp = Blueprint('receiving', __name__)

@receiving_bp.route('/', methods=['GET', 'POST'])
def receiving():
    if request.method == 'GET':
        return render_template('receiving.html')
    elif request.method == 'POST':
        data = request.form
        upc = data['upc']
        quantity = int(data['quantity'])
        location = data['location']
        
        # Add inventory item
        result = cluster.add_inventory_item(upc, quantity, location, reserved=False)
        
        # Flash a success or error message
        if result:
            flash(f"Item successfully added! ID: {str(result)}", "success")
        else:
            flash("Failed to add item to inventory.", "error")

        return redirect(url_for('receiving.receiving'))
