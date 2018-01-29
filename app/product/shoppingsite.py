"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import model
from sqlalchemy.sql.expression import false


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    if "cart" in session.keys():
        pass
    else:
        session["cart"] = []
    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    return render_template("all_melons.html",
                           melon_list=melons)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    return render_template("cart.html", 
                            cart=session['cart'])


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    

    melon = model.Melon.get_by_id(id)
    qty = int(request.args.get('qty'))
    total = melon.price * qty
    total = "$%.2f" % total
    common_name = melon.common_name
    price = melon.price_str()
    print "OMG MELON", melon
    if len(session['cart']) > 0:
        new_item = True
        for old_order in session['cart']:
            #print "the for loop ran"
            if old_order[0] == common_name:
                #print "the if ran"
                old_order[1] += qty
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

    flash("Melon added to cart successfully!")
    return render_template("cart.html", 
                            cart=session['cart'])
    # return render_template("cart.html", melon_name=test_melon, melon_qty=test_qty, melon_price=test_price, melon_total=total)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form.get("email")
    password = request.form.get("password")
    
    authenticated = model.Customer.authenticate(email, password)
    

    if authenticated:
        name = model.Customer.get_by_email(email)
        session["first_name"] = name
        session["login"] = (email, password)


        print "email is %s and password is %s" %(email, password)
        print "session email is %s and session password is %s" %(session["login"][0], session["login"][1])
        return redirect("/melons")

    else:
        flash("Sorry! Your information was not found in our system.")
        return redirect("/login")
        
    

@app.route("/logout")
def logout():
    """strips all session variables and returns the login page"""

    for key in session.keys():
        del session[key]

    return redirect("/login")

@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
