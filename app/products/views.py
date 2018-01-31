# app/main/views.py

from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required, current_user

from .. import db
from ..models import Product
from . import product
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from ..models import Catalog

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
    print product
    return render_template("product/product_details.html",
                           display_product=product,catalogs=catalogs,catalog_id=id)


@product.route("/cart")
@login_required
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing products added

    return render_template("product/cart.html", 
                            cart=session['cart'])


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
            order = [common_name, qty, price, total]
            session['cart'].append(order)
        
    else:
        #print "the else outside ran"
        order = [common_name, qty, price, total]
        session['cart'].append(order)



    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list

    flash("Product added to cart successfully!")
    return render_template("product/cart.html", 
                            cart=session['cart'])
    # return render_template("cart.html", product_name=test_product, product_qty=test_qty, product_price=test_price, product_total=total)


@product.route("/checkout")
@login_required
def checkout():
    """Checkout customer, process payment, and ship products."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/product/products")

