# app/main/views.py

from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
from datetime import datetime
from .. import db
#from forms import ProductForm
from app.products import product
from ..models import Product,Order,Order_detail, Catalog
from flask_login import login_user, logout_user, login_required, current_user
import paypalrestsdk, os
import stripe

stripe_keys = {
  'secret_key': 'sk_test_uxtuIOeAfAyn2AYpImH7Mjft',
  'publishable_key': 'pk_test_sRa1igLaBVBHhNtVkUPAyBAi'
}
stripe.api_key = stripe_keys['secret_key']
# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

#app.jinja_env.undefined = jinja2.StrictUndefined

@product.route('/stripecharge', methods=['POST'])
@login_required
def stripecharge():
    # Amount in cents
    amount = 0
    for order in session['cart']:
        amount = amount + order[1] * float(order[2])
    customer = stripe.Customer.create(
        email='teaasia5812@gmail.com',
        source=request.form['stripeToken']
    )
    #print customer.id
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=int(amount*100),
        currency='usd',
        description='TeaAsia Patment'
    )
    #print charge
    if charge['paid'] == True :
        current_order = Order(user_id = current_user.id, payment_id = charge['customer'] + '-' + charge['id'],email = charge['source']['name'] , status = True)
        db.session.add(current_order)
        #db.session.flush()
        db.session.commit()
        total = 0
        
        for order in session['cart']:
            order_detail = Order_detail(user_id = current_user.id, product_id = order[4], product_name = order[0], quantity = order[1], price = order[2], order_id = int(current_order.id) )
            db.session.add(order_detail)
            total = total + int(order[1]) * float(order[2])
            
        db.session.commit()
        order = Order.query.filter_by(id=current_order.id).first()
        order.total = total
        db.session.commit()
        flash('Order ID:%s Created! Shipout ASAP.' % (charge['customer'] + '-' + charge['id']))
        message = True
    orders = Order.query.filter_by(user_id=current_user.id, payment_id = charge['customer'] + '-' + charge['id'])
    catalogs = Catalog.get_all()
    return render_template("product/order.html",orders=orders,catalogs=catalogs,message=message)
@product.route("/products/<int:id>")
#@login_required
def list_products(id):
    """Return page showing all the products has to offer"""
    catalogs = Catalog.get_all()
    if id :
        products = Product.query.filter_by(catalog_id=id)
    else:
        products = Product.get_all()
    return render_template("product/all_products.html",
                           product_list=products,catalogs=catalogs,catalog_id=id)

@product.route("/product/<int:id>")
#@login_required
def show_product(id):
    """Return page showing the details of a given product.

    Show all info about a product. Also, provide a button to buy that product.
    """
    catalogs = Catalog.get_all()
    product = Product.get_by_id(id)
    return render_template("product/product_details.html",
                           display_product=product,catalogs=catalogs,catalog_id=id)

@product.route("/cart")
@login_required
def shopping_cart():
    """Display content of shopping cart."""
    if "cart" in session.keys():
        pass
    else:
        session["cart"] = []
    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing products added
    total = 0
    for order in session['cart']:
        total = total + order[1] * float(order[2])
    catalogs = Catalog.get_all()
    return render_template("product/cart.html", 
                            cart=session['cart'],catalogs=catalogs, total=total,publishkey = stripe_keys['publishable_key'])

@product.route("/remove_from_cart/<string:name>")
@login_required
def remove_from_cart(name):
    index = 0
    for order in session['cart']:
        if order[0] == name:
            target_index = index
        index = index + 1  
    
    session['cart'].pop(target_index)
    flash("Product removed from cart successfully!")
    catalogs = Catalog.get_all()
    total = 0
    for order in session['cart']:
        total = total + order[1] * float(order[2])
    return render_template("product/cart.html", 
                            cart=session['cart'],catalogs=catalogs,total=total,publishkey = stripe_keys['publishable_key'])

@product.route("/add_to_cart/<int:id>")
@login_required
def add_to_cart(id):
    """Add a product to cart and redirect to shopping cart page.

    When a product is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    if "cart" in session.keys():
        pass
    else:
        session["cart"] = []
    product = Product.get_by_id(id)
    qty = int(request.args.get('qty'))
    total = float(product.price) * qty
    common_name = product.common_name
    price = product.price_str()
    if len(session['cart']) > 0:
        new_item = True
        for old_order in session['cart']:
            #print "the for loop ran"
            if old_order[0] == common_name:
                #print "the if ran"
                old_order[1] += qty
                old_order[3] += total
                new_item = False
        if new_item:
            #print "the else in the for loop ran"
            order = [common_name, qty, price, total, id]
            session['cart'].append(order)
        
    else:
        #print "the else outside ran"
        order = [common_name, qty, price, total, id]
        session['cart'].append(order)

    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list
    total = 0
    for order in session['cart']:
        total = total + order[1] * float(order[2])
    flash("Product added to cart successfully!")
    catalogs = Catalog.get_all()
    return render_template("product/cart.html", 
                            cart=session['cart'],catalogs=catalogs,total=total,publishkey = stripe_keys['publishable_key'])
    # return render_template("cart.html", product_name=test_product, product_qty=test_qty, product_price=test_price, product_total=total)

@product.route("/clean")
@login_required
def clean():
    """Checkout customer, process payment, and ship products."""
    #from session

    flash("Success. cart already cleaned!!!!")
    catalogs = Catalog.get_all()
    session['cart'] =[]
    return redirect("/product/cart")

@product.route("/order")
@login_required
def shopping_order():
    """Display content of shopping order."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing products added
    orders = Order.query.filter_by(user_id=current_user.id)
    catalogs = Catalog.get_all()
    return render_template("product/order.html", 
                            orders=orders,catalogs=catalogs)

@product.route("/order_detail/<int:id>")
@login_required
def shopping_order_detail(id):
    catalogs = Catalog.get_all()
    order_details = Order_detail.query.filter_by(order_id=id)
    return render_template("product/order_detail.html", 
                            order_details=order_details,catalogs=catalogs)