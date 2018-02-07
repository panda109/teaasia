# app/main/views.py

from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash
from flask_login import login_required, current_user
from datetime import datetime
from .. import db
from app.products import product
from ..models import Product,Order,Order_detail, Catalog
from flask_login import login_user, logout_user, login_required, current_user
import paypalrestsdk

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AVZNCwkrjarX-zC0D_5eSpdl57UkbErxRk6GkAQb0_jOQ3G53jkHzluhVQIZlRJVdKRwi-MGoGuewGni",
  "client_secret": "EBYefvJFPvDEt914WwlLlwpORxgXvZxEyqD87x2xuSbjfowwKMf9VOgDdQ28fY9J5P2eLKAudIAmy-Sc" })
# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

#app.jinja_env.undefined = jinja2.StrictUndefined

@product.route("/products")
def list_all_products():
    """Return page showing all the products has to offer"""
    catalogs = Catalog.get_all()
    products = Product.get_all()
    return render_template("product/all_products.html",
                           product_list=products,catalogs=catalogs)
@product.route("/products/<int:id>")
def list_products(id):
    """Return page showing all the products has to offer"""
    catalogs = Catalog.get_all()
    products = Product.query.filter_by(catalog_id=id)
    return render_template("product/all_products.html",
                           product_list=products,catalogs=catalogs,catalog_id=id)


@product.route("/product/<int:id>")
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
    catalogs = Catalog.get_all()
    return render_template("product/cart.html", 
                            cart=session['cart'],catalogs=catalogs)


@product.route("/add_to_cart/<int:id>")
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
    print "OMG PRODUCT", product
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

    flash("Product added to cart successfully!")
    catalogs = Catalog.get_all()
    return render_template("product/cart.html", 
                            cart=session['cart'],catalogs=catalogs)
    # return render_template("cart.html", product_name=test_product, product_qty=test_qty, product_price=test_price, product_total=total)

#        "redirect_urls": {
#            "return_url": "http://127.0.0.1:5000/product/checkout",
#            "cancel_url": "http://127.0.0.1:5000/product"},
@product.route("/payment", methods=['POST'])
@login_required
def payment():

    payment_dict,payment_method,items,item_list,amount,url = {},{},{},{},{},{}
    payment_dict['intent'] = "sale"
    payment_method['payment_method'] =  "paypal"
    payment_dict['payer'] = payment_method
    url['return_url'] = "https://localhost:5000/product/cart"
    url['cancel_url'] = "https://localhost:5000/"
    payment_dict['redirect_urls'] = url
    #for each item in session
    total = 0
    templist = []
    for order in session['cart']:
        item = {}
        item['name'] = order[0]
        item['sku'] = str(order[4])
        item['price'] = str(order[2])
        item['currency'] = "USD"
        item['quantity'] = str(order[1])
        templist.append(item)
        total = total + order[1] * float(order[2])
    #
    items['items'] = templist
    item_list['item_list'] = items
    amount['total'] = str(total)
    amount['currency'] = "USD"
    item_list['item_list'] = items
    item_list['amount'] = amount
    item_list['description'] = 'This is payment description.'
    payment_dict['transactions'] = [item_list]
    #print payment_dict
    payment = paypalrestsdk.Payment(payment_dict)
    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        #=======================================================================
        # for link in payment.links:
        #     if link.method == "REDIRECT":
        #         redirect_url = str(link.href)
        #         print("Redirect for approval: %s" % (redirect_url))
        #     if link.rel == "approval_url":
        #         approval_url = str(link.href)
        #         print("Redirect for approval: %s" % (approval_url))
        #=======================================================================
    else:
        print(payment.error)
    return jsonify({'paymentID' : payment.id})

@product.route("/execute", methods=['POST'])
@login_required
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print session['cart']
        if len(session['cart']) > 0:
            current_order = Order(user_id = current_user.id, paypal_id = payment.id + '_' + request.form['payerID'], status = True)
            db.session.add(current_order)
            #db.session.flush()
            db.session.commit()
            total = 0
            for order in session['cart']:
                order_detail = Order_detail(user_id = current_user.id, product_id = order[4], quantity = order[1], price = order[2], order_id = int(current_order.id) )
                db.session.add(order_detail)
                total = total + int(order[1]) * float(order[2])
            db.session.commit()
            order = Order.query.filter_by(id=current_order.id).first()
            order.total = total
            db.session.commit()
        print('PayerID %s, PaymentID %s Execute success!' % (request.form['payerID'], payment.id))
        success = True
    else:
        print(payment.error)
    return jsonify({'success' : success})

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