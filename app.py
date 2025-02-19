# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import insert_data_from_csv, Session, add_placement_data, update_placement_data, delete_placement_data, authenticate_admin
from models import PlacementData
from plots import create_dashboard_plots

""" __name__ is a special py var that represents the name
 of the current module. When u run a py script directly 
 __name__ is set to "__main__" whereas when imported as 
 a module it is set to the name of module. """
app = Flask(__name__) #Flask is a class provided by the Flask framework. It represents flask application

app.secret_key = 'your_secret_key'  # Needed for session management

# Insert data from CSV
insert_data_from_csv("D:/Onkar/Onkar Doc/NEW Scanned Docs/SM VITA/python/project/sunbeam_batch_placement_data.csv")

# Create plots
create_dashboard_plots()

@app.route("/", methods=['GET'])
def getHome():
    print("Welcome to placement records")
    return render_template('home.html')

@app.route("/placement", methods=['GET'])
def getPlacements():
    # Change this part to use SQLAlchemy session
    session = Session()
    result = session.query(PlacementData).all()
    session.close()
    return render_template('placement_data.html', data=result)

@app.route("/dashboard", methods=['GET'])
def getDashboard():
    return render_template('plot.html')


# Admin Login Route
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_admin(username, password):
            session['admin'] = username  # Store admin username in session
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('admin_login.html')


@app.route("/admin/dashboard", methods=['GET'])
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    db_session = Session()
    result = db_session.query(PlacementData).all()
    db_session.close()
    return render_template('admin_dashboard.html',data=result)


@app.route("/admin/add", methods=['POST'])
def admin_add():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    try:
        batch = request.form['Batch']
        karad_dac = request.form['KaradDac']
        dac = request.form['DAC']
        dmc = request.form['DMC']
        desd = request.form['DESD']
        dbda = request.form['DBDA']
        add_placement_data(batch, karad_dac, dac, dmc, desd, dbda)
        flash("Record added successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/update/<int:id>", methods=['POST'])
def admin_update(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    try:
        batch = request.form['Batch']
        karad_dac = request.form['KaradDac']
        dac = request.form['DAC']
        dmc = request.form['DMC']
        desd = request.form['DESD']
        dbda = request.form['DBDA']
        update_placement_data(id, batch, karad_dac, dac, dmc, desd, dbda)
        flash("Record updated successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/delete/<int:id>", methods=['POST'])
def admin_delete(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    try:
        delete_placement_data(id)
        flash("Record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('admin_dashboard'))


@app.route("/admin/update_form/<int:id>", methods=['GET', 'POST'])
def update_form(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db_session = Session()
    record = db_session.query(PlacementData).filter_by(id=id).first()
    db_session.close()

    if not record:
        flash("Record not found!", "danger")
        return redirect(url_for('admin_dashboard'))

    # Render a template to display the current record in a form for editing
    return render_template('update_form.html', record=record)

@app.route("/admin/logout")
def admin_logout():
    session.pop('admin', None)  # Remove admin from session
    return redirect(url_for('admin_login'))



if __name__ == '__main__':
    app.run(debug=True) # debug=True gives more detailed errors and automatic reloading of server