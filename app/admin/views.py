# app/main/views.py
from shutil import copyfile
from flask import render_template, session, redirect, url_for, current_app, jsonify, request, flash, app
import hashlib
from .. import db
from forms import ProductForm, ChangeCatalogForm, ChangeUserForm
from app.admin import admin
from ..models import Product, Order, Order_detail, Catalog, User, Role
from flask_login import login_user, logout_user, login_required, current_user
import paypalrestsdk, os, datetime
from ..email import send_email
from werkzeug import secure_filename
#from flask_uploads import UploadSet, IMAGES
from sqlalchemy.orm import query
#images = UploadSet('images', IMAGES)
from app import images

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

# app.jinja_env.undefined = jinja2.StrictUndefined


@admin.route("/users", methods=['GET', 'POST'])
@login_required
def users():
    """Return page showing all the products has to offer"""
    check_admin()
    users = User.get_all()
    orders = Order.get_all()
    catalogs = Catalog.get_all()
    # pre setting value
    return render_template('admin/users.html', users=users, orders=orders, catalogs=catalogs)


@admin.route("/user/<int:id>", methods=['GET', 'POST'])
@login_required
def user(id):
    """Return page showing all the products has to offer"""
    check_admin()
    from_order = True
    users = User.query.filter_by(id=id)
    orders = Order.get_all()
    catalogs = Catalog.get_all()
    # pre setting value
    return render_template('admin/users.html', from_order=from_order, users=users, orders=orders, catalogs=catalogs)


@admin.route("/edit_user/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Return page showing all the catalog"""
    check_admin()
    add_user = False
    user = User.query.get_or_404(id)
    form = ChangeUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.name.data
        role_name = form.role.data
        user.role_id = Role.query.filter_by(name=str(form.role.data)).first().id
        user.add = form.add.data
        user.confirmed = form.confirmed.data
        db.session.commit()
        # redirect to the departments page
        return redirect(url_for('admin.users'))
    # pre setting value
    form.name.data = user.username
    catalogs = Catalog.get_all()
    return render_template('admin/user.html', action="Edit", form=form,
                            add_user=add_user, catalogs=catalogs, title="Edit User")  


@admin.route("/shipout_order/<int:id>", methods=['GET', 'POST'])
@login_required
def shipout_order(id):
    """Update shipout -> True"""
    check_admin()
    order = Order.query.filter_by(id=id).first()
    if order.shipout == False :
        order.shipout = True
        order.ship_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
        db.session.add(order)
        db.session.commit()
        user = User.query.filter_by(id=order.user_id).first()
        send_email(user.email, 'Confirm Your Shipping', 'admin/email/ship', user=user, order=order)
        flash('Order was ship out and send email to user.')
    orders = Order.get_all()
    catalogs = Catalog.get_all()

    return render_template("admin/orders.html", catatlogs=catalogs, orders=orders)


@admin.route("/orders")
@login_required
def orders():
    """Return page showing all the products has to offer"""
    check_admin()
    orders = Order.get_all()
    catalogs = Catalog.get_all()
    return render_template("admin/orders.html", catalogs=catalogs, orders=orders)

# @admin.route("/edit_order/<int:id>",methods=['GET', 'POST'])
# @login_required
# def edit_order(id):
#     """Return page showing all the products has to offer"""
#     check_admin()
#    
#     #pre setting value
#     return render_template('admin/order.html', action="Edit",
#                            add_order0=add_order, form=form,
#                            order=order, title="Edit Order")


@admin.route("/catalogs")
@login_required
def catalogs():
    """Return page showing all the products has to offer"""
    check_admin()
    catalogs = Catalog.get_all()
    return render_template("admin/catalogs.html", catalogs=catalogs)    


@admin.route("/add_catalogs", methods=['GET', 'POST'])
@login_required
def add_catalog():
    """Return page showing all the products has to offer"""
    check_admin()
    add_catalog = True
    form = ChangeCatalogForm()
    if form.validate_on_submit():
        catalog = Catalog(catalog_name=form.name.data)
        db.session.add(catalog)
        db.session.commit()
        # redirect to the departments page
        return redirect(url_for('admin.catalogs'))
    # pre setting value
    catalogs = Catalog.get_all()
    return render_template('admin/catalog.html', action="Add", form=form,
                            add_catalog=add_catalog, catalogs=catalogs, title="Add Catalog")  


@admin.route("/edit_catalog/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_catalog(id):
    """Return page showing all the catalog"""
    check_admin()
    add_catalog = False
    catalog = Catalog.query.get_or_404(id)
    form = ChangeCatalogForm(obj=catalog)
    if form.validate_on_submit():

        catalog.catalog_name = form.name.data
        db.session.commit()
        # redirect to the departments page
        return redirect(url_for('admin.catalogs'))
    # pre setting value
    form.name.data = catalog.catalog_name
    catalogs = Catalog.get_all()
    return render_template('admin/catalog.html', action="Edit", form=form,
                            add_catalog=add_catalog, catalogs=catalogs, title="Edit Catalog")  


@admin.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    """Return page showing all the products has to offer"""
    check_admin()
    add_product = True
    form = ProductForm()
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        src = os.getcwd() + '\\static\\_uploads\\images\\' + filename
        form.upload.data.save(src)
        filemd5 = hashlib.md5()

        with open(os.getcwd() + '\\static\\_uploads\\images\\' + filename,'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                filemd5.update(chunk)
        if form.available.data :
            in_stock = True
        else:    
            in_stock = False
        dst = os.getcwd() + '\\static\\product\\images\\' + filemd5.hexdigest()+'.'+filename.split('.')[1]        
        if  Product.query.filter_by(imgurl = filemd5.hexdigest()+'.'+filename.split('.')[1]).first() == None :

            copyfile(src, dst)
            os.remove(src)
            product = Product(common_name=form.common_name.data,
            price=form.price.data,
            imgurl=filemd5.hexdigest()+'.'+filename.split('.')[1],
            color=form.color.data,
            size=form.size.data,
            available=in_stock,
            catalog_id=Catalog.query.filter_by(catalog_name=str(form.catalog_id.data)).first().id
            )
            db.session.add(product)
            db.session.commit()
            flash('Add product successfull.')
        else:
            os.remove(src)
            flash('Upload image file was in used.')
        # redirect to the departments page
        return redirect(url_for('admin.products'))

    # form.common_name.data = product.common_name
    # form.price.data = product.price
    catalogs = Catalog.get_all()
    products = Product.get_all()
    return render_template('admin/product.html', action="Add",
                           add_product=add_product, form=form,
                           products=products, title="Edit Product", catalogs=catalogs)


@admin.route("/delete_product/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """Return page showing all the products has to offer"""
    check_admin()
    product = Product.query.get_or_404(id)
    os.remove(os.getcwd() + '\\static\\product\\images\\' + product.imgurl)
    db.session.delete(product)
    db.session.commit()
    flash('Product was deleted successfull.')
    catalogs = Catalog.get_all()    
    products = Product.get_all()
    return render_template("admin/products.html",
                           products=products, catalogs=catalogs)

    
@admin.route("/edit_product/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """Return page showing all the products has to offer"""
    check_admin()
    add_product = False
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        filename = secure_filename(form.upload.data.filename)
        src = os.getcwd() + '\\static\\_uploads\\images\\' + filename
        form.upload.data.save(src)
        filemd5 = hashlib.md5()

        with open(os.getcwd() + '\\static\\_uploads\\images\\' + filename,'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                filemd5.update(chunk)
        if form.available.data :
            in_stock = True
        else:    
            in_stock = False
        dst = os.getcwd() + '\\static\\product\\images\\' + filemd5.hexdigest()+'.'+filename.split('.')[1]        
        product = Product.query.filter_by(id = id).first()
        product.common_name = form.common_name.data
        product.price=form.price.data
        orgfilename = os.getcwd() + '\\static\\product\\images\\'+product.imgurl
        product.imgurl=filemd5.hexdigest()+'.'+filename.split('.')[1]
        product.color=form.color.data
        product.size=form.size.data
        product.available=in_stock
        product.catalog_id=Catalog.query.filter_by(catalog_name=str(form.catalog_id.data)).first().id
        db.session.commit()
        flash('Update product successfull.')
        copyfile(src, dst)
        os.remove(orgfilename)
        os.remove(src)
        #os.remove(os.getcwd() + '\\static\\product\\images\\'+orgfilename)
        # redirect to the departments page
        return redirect(url_for('admin.products'))
    # pre setting value
    form.catalog_id.data = product.product_type
    catalogs = Catalog.get_all()    
    return render_template('admin/product.html', action="Edit",
                           add_product=add_product, form=form,
                           product=product, catalogs=catalogs, title="Edit Product")


@admin.route("/products")
@login_required
def products():
    """Return page showing all the products has to offer"""
    check_admin()
    catalogs = Catalog.get_all()
    products = Product.get_all()
    return render_template("admin/products.html",
                           products=products, catalogs=catalogs)
