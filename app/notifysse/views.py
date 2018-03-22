# app/main/views.py
from flask_sse import sse
from app.notifysse import notifysse
#import paypalrestsdk

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

# app.jinja_env.undefined = jinja2.StrictUndefined


@notifysse.route("/hello")
# @login_required
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"


@notifysse.route("/")
# @login_required
def publish_hello():

    return render_template('index.html')