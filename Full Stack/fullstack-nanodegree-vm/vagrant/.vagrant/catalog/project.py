from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# A list of all of the restaurants

# ----------------------------Restaurant Items Below --------------------------


@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restautantsList.html', restaurants=restaurants)


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def restautantsEdit(restaurant_id):
    restaurantEdit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['restaurant_edit_name']:
            restaurantEdit.name = request.form['restaurant_edit_name']
            session.add(restaurantEdit)
            session.commit()
            flash('Restaurant has been edited')
            return redirect(url_for('restaurantList'))
    return render_template('restaurantEdit.html', restaurant=restaurant, restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/delete')
def restautantsDelete(restaurant_id):
    return "deleteing restautant {0}".format(restaurant_id)


@app.route('/restautants/new')
def restuarantsNew():
    return "making a new restaurants"

# -------------------------------Menu Items Below -----------------------------
# all of the menu items for a given restaurant


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item ceated!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    edit_menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['edit_menu_item_name']:
            edit_menu_item.name = request.form['edit_menu_item_name']
            session.add(edit_menu_item)
            session.commit()
            flash("item has been edited!")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edit_menu_item)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("delete item ceated!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)

# JSON Response for a restaurants entire menu


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# JSON Response for one restaurants menu


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    itemToReturn = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=itemToReturn.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
