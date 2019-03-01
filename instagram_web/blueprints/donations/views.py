from app import app
from flask import Flask, render_template, redirect, request, flash, url_for, Blueprint
from models.base_model import db
from models.user import User
from models.image import Image
from models.donation import Donation
from flask_login import current_user, login_required
from instagram_web.util.braintree_helpers import gateway, generate_client_token

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')

@donations_blueprint.route('<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    client_token = generate_client_token()
    return render_template('donations/new.html', image_id=image_id, client_token=client_token)

@donations_blueprint.route('<image_id>/checkout', methods=['POST'])
def create(image_id):
    amount = request.form['amount']
    nonce_from_the_client = request.form['payment_method_nonce']
    result = gateway.transaction.sale({
        'amount': amount,
        'payment_method_nonce': nonce_from_the_client,
        'options': {
            "submit_for_settlement": True
        }
    })

    image_owner_id = Image.get_by_id(image_id)
    
    if result.is_success:
        new_donation = Donation.create(
            sender_id=current_user.id, receiver_id=image_owner_id, image=image_id, amount=amount)
        # need to link to user not image
        new_donation.save()
        flash('Donation received successfully', 'success')
        return redirect(url_for('users.show', username=current_user.name))
    else:
        flash(result.transaction.status)
        # flash(f'{result.transaction.processor_response_code}': {result.transaction.processor_response_code})
        return redirect(url_for('users.show', username=current_user.name))

