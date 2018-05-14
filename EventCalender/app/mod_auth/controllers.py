# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, json, abort, send_from_directory

# Import password / encryption helper tools
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
# Import the database object from the main app module

from app import db
import os

# Import module forms
from app.mod_auth.forms import LoginForm,  NewEventForm, Registration, SearchForm

# Import module models (i.e. User)
from app.mod_auth.models import User, Event, Location
import urllib.parse
import requests
from sqlalchemy import or_, and_, update


# Define the blueprint: 'auth', set its url prefix: app.url/auth
# mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
mod = Blueprint('templates', __name__)
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if request.method == 'POST' and form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first() # first_or_404()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['email'] = user.email
            session['owner'] = user.name
            session['role'] = user.role
            flash('Welcome %s' % user.name)
            return redirect(url_for('templates.index'))
        flash('Wrong email or password', 'error-message')
    return render_template("auth/signin.html", form=form)


@mod.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        result = search_results(form)
    else:
        result = None
    return render_template('index.html', form=form, events=result, carousel_events=get_events())


@mod.route('/results')
def search_results(form):
    search_string = form.search.data
    results = db.session.query(Event, Location).join(Location, Event.location_id == Location.id).filter(or_(
        Event.name.contains(search_string),
        Location.name.contains(search_string),
        Event.description.contains(search_string),
        Location.street.contains(search_string),
        Event.category.contains(search_string))).all()
    return results


@mod.route('/user/<int:user_id>')
def user(user_id):
    return render_template('user.html')


@mod.route('/map')
def map():
    return render_template('map.html', locations=get_event_location_data)


@mod.route('/calendar')
def calendar():
    return render_template('calendar.html', events=get_event_data)


@mod.route('/events')
def events():
    return render_template('events.html', events=get_event_location())


@mod.route('/event/<int:e_id>')
def event(e_id):
    return render_template('event.html', event=get_event(e_id))


@mod_auth.route('/statistics')
def statistics():
    return render_template('auth/statistics.html', events=get_events_admin(), users=get_users(), locations=get_location())


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if "user_id" in session:
        return redirect(url_for("index"))
    form = Registration(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(
            form.name.data,
            form.phone.data,
            form.email.data,
            form.password.data,
            form.company.data,
            form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Gratulerer, du har nå registrert bruker!")
        return redirect(url_for('auth.signin'))
    return render_template("auth/signup.html", form=form)


@mod_auth.route('/add_events', methods=['GET', 'POST'])
def add_events():
    form = NewEventForm(CombinedMultiDict((request.files, request.form)))
    if request.method == "POST":
        f = form.image.data
        filename = "aviator_art_home_page_4-Cessna.jpg"
        print("f", f)
        if not (f is None):
            filename = secure_filename(f.filename)
            print("\n\n!!! TYPE !!! :", type(filename))
            f.save(os.path.join('app/static/images', filename)) #f.save(os.path.join('/home/ahmedabdi/mysite/Eventcalendar/app/static/images', filename))

        if "owner" in session:
            owner = session.get('owner')
        else:
            owner = "Unknown"
        lat = 0
        lng = 0

        try:
            encodeAddress = urllib.parse.quote(form.street.data)
            url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(encodeAddress)
            response = requests.get(url)
            print(response.status_code)
            resp_json_payload = response.json()

            if response.status_code in (200, 404):
                lat = resp_json_payload['results'][0]['geometry']['location']['lat']
                lng = resp_json_payload['results'][0]['geometry']['location']['lng']
            print(lat, "\n", lng)
        except requests.exceptions.RequestException as e:
            print(e)

        # TODO : Not create NEW location if already exists
        new_location = Location(
            form.location_name.data,
            lat,
            lng,
            form.country.data,
            form.city.data,
            form.street.data,
            form.zip.data
        )
        db.session.add(new_location)
        db.session.flush()
        new_event = Event(
            new_location.id,
            owner,
            form.name.data,
            form.event_type.data,
            form.category.data,
            form.description.data,
            form.startDate.data,
            form.startTime.data,
            form.endDate.data,
            form.endTime.data,
            filename,
            deleted=False,
        )
        db.session.add(new_event)
        db.session.commit()
        flash("Arrangement har blitt lagt til","success")
        return redirect(url_for("templates.events"))
    return render_template('auth/add_events.html', form=form)


@mod_auth.route("/logout")
def logout():
    session.pop('user_id')
    session.pop('email')
    session.pop('owner')
    session.pop("role")
    return redirect(url_for("templates.index"))


@mod_auth.route("/get_event_data")
def get_event_data():
    events_from_db = get_events()
    events = request.args.get('events', events_from_db, type=str)
    return json.dumps(events)


@mod_auth.route("/get_event_location_data")
def get_event_location_data():
    events_locations_from_db = get_event_location()
    event_location = request.args.get('event_location', events_locations_from_db, type=str)
    return json.dumps(event_location)


def get_event_location():
    return db.session.query(Event, Location).join(Location, Event.location_id == Location.id).filter(Event.deleted==False).all()


@mod_auth.route('/delete/<int:e_id>', methods=['POST'])
def remove_event(e_id):
    event = Event.query.get_or_404(e_id)
    if event.deleted:
        abort(404)
    event.deleted = True
    db.session.commit()
    return redirect(url_for('templates.index'))


def get_events():
    return db.session.query(Event).filter(and_(Event.startTime.isnot(None), Event.startDate.isnot(None), Event.endTime.isnot(None),Event.endDate.isnot(None), Event.deleted == False)).all()


def get_events_admin():
    return db.session.query(Event).filter(and_(Event.startTime.isnot(None), Event.startDate.isnot(None), Event.endTime.isnot(None),Event.endDate.isnot(None))).all()


def get_users():
    return db.session.query(User).all()


def get_location():
    return db.session.query(Location).all()


def get_event(e_id):
    return db.session.query(Event).get(e_id)
