from flask import Blueprint, render_template, request, flash, redirect, url_for
import cluster

picking_bp = Blueprint('picking', __name__)

@picking_bp.route('/', methods=['GET', 'POST'])
def picking():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'begin_picking':
            # Fetch the oldest order and begin the picking process
            order_details = cluster.pick_order()

            if "error" in order_details:
                flash(order_details["error"], "error")
                return redirect(url_for('picking.picking'))

            print("picking.py details:", order_details)

            return render_template('confirm_pick.html', order_details=order_details)

        elif action == 'logout':
            return redirect(url_for('auth.logout'))

    return render_template('picking.html')

@picking_bp.route('/confirm', methods=['POST'])
def confirm_picking():
    order_id = request.form.get('order_id')
    confirmations = []

    # Process the confirmations from the form
    for key in request.form.keys():
        if key.startswith("upc_"):
            upc = key.split("_")[1]
            quantity = int(request.form.get(key))
            confirmations.append({"upc": upc, "quantity_confirmed": quantity})

    result = cluster.confirm_pick(order_id, confirmations)

    if "error" in result:
        flash(result["error"], "error")
    else:
        flash(result["message"], "success")

    return redirect(url_for('picking.picking'))
