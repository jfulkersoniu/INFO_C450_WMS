from flask import Blueprint, render_template, request, flash, redirect, url_for
import cluster

shipping_bp = Blueprint('shipping', __name__)

@shipping_bp.route('/', methods=['GET', 'POST'])
def shipping():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'begin_packing':
            # Fetch the oldest order in "Picked" status
            order_details = cluster.find_picked_order()

            if "error" in order_details:
                flash(order_details["error"], "error")
                return redirect(url_for('shipping.shipping'))

            return render_template('confirm_pack.html', order_details=order_details)

        elif action == 'logout':
            return redirect(url_for('auth.logout'))

    return render_template('shipping.html')

@shipping_bp.route('/confirm', methods=['POST'])
def confirm_packing():
    order_id = request.form.get('order_id')
    carton_id = request.form.get('carton_id')

    # Pack order
    result = cluster.pack_order(order_id, carton_id)

    if "error" in result:
        flash(result["error"], "error")
    else:
        flash(result["message"], "success")

    return redirect(url_for('shipping.shipping'))
