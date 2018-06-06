from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)
	    

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method=='POST':
        newRes=Restaurant(name=request.form['name'])
        session.add(newRes)
        session.commit()
        flash("new Restaurant created!")
        return redirect(url_for('restaurants'))
    
    else:
        return render_template('newRes.html')

		
		
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    editedRes=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        editedRes.name = request.form['name']
        session.add(editedRes)
        session.commit()
        flash("Restaurant edited!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('editRes.html', restaurant_id=restaurant_id, editeditem=editedRes)			
		


@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    deleteRes=session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        session.delete(deleteRes)
        session.commit()
        flash("Restaurant deleted!")
        return redirect(url_for('restaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRes.html', restaurant_id=restaurant_id, deleteitem=deleteRes)	
    


		


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem=MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, menuitem=editedItem)	
    

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteMenuItem=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        session.delete(deleteMenuItem)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, menuitem=deleteMenuItem)	
    

if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
