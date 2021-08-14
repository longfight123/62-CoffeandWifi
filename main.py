"""Collection of cafes website

This webpage displays a table of different cafes with personal ratings,
location data, and other information. There is a secret /add route where the user
can add additional cafes to the table.

This script requires that 'Flask', 'Flask-Bootstrap',
 'Flask-WTF', 'python_dotenv' be installed within the Python
environment you are running this script in. The user needs to have their own
'SECRET_KEY' in an environment variable .env file.

"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os
#from dotenv import load_dotenv

#load_dotenv('.env')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)


class CafeForm(FlaskForm):
    """
    A class used to create a WTForm.

    ...

    Attributes
    ----------
    cafe: StringField
        name of the cafe
    location: StringField
        link to the location of the cafe
    open_time: StringField
        time the cafe opens
    close_time: StringField
        time the cafe closes
    coffee_rating: SelectField
        rating of the coffee
    wifi_rating: SelectField
        rating of the wifi
    power_rating: SelectField
        rating of the power
    submit: SubmitField
        submit the form
    """
    cafe = StringField(label='Cafe name', validators=[DataRequired(message='Enter a value.')])
    location = StringField(label='Cafe Location On Google Maps (URL)', validators=[DataRequired(message='Enter a value.'), URL(message='Enter a valid URL.')])
    open_time = StringField(label='Open time. eg 8AM', validators=[DataRequired(message='Enter a value.')])
    close_time = StringField(label='Close time. eg 3PM', validators=[DataRequired(message='Enter a value.')])
    coffee_rating = SelectField(choices=['C', 'CC', 'CCC', 'CCCC', 'CCCCC'], validators=[DataRequired(message='Enter a value.')])
    wifi_rating = SelectField(choices=['W', 'WW', 'WWW', 'WWWW', 'WWWWW'], validators=[DataRequired(message='Enter a value.')])
    power_rating = SelectField(choices=['P', 'PP', 'PPP', 'PPPP', 'PPPPP'], validators=[DataRequired(message='Enter a value.')])
    submit = SubmitField(label='Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    """the landing page

    GET: landing page
    """
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    """the secret add cafe page

    GET: displays the WTForm to add a cafe
    POST: add the cafe to the csv
    """
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data
        new_row = f'{cafe},{location},{open_time},{close_time},{coffee_rating},{wifi_rating},{power_rating}'
        with open('cafe-data.csv', 'a') as csv_file:
            csv_file.write(f'\n{new_row}')
        with open('cafe-data.csv', newline='') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            list_of_rows = []
            for row in csv_data:
                list_of_rows.append(row)
        return render_template('cafes.html', cafes=list_of_rows)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    """shows all the cafes

    GET: show all cafes in the csv
    """
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
