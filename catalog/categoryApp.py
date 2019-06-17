from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random, string, json, httplib2, requests
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database
engine = create_engine('sqlite:///stock_catalog.db')
Base.metadata.bind = engine

# Create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

@app.route('/')
@app.route('/categories')
def showCategories():
	# Get all categories
	categories = session.query(Category).all()

	# Get lastest 5 category items added
	categoryItems = session.query(CategoryItem).all()

	return render_template('categories.html', categories = categories, categoryItems = categoryItems)

@app.route('/categories/<int:category_id>')
@app.route('/categories/<int:category_id>/stock')
def showCategory(catalog_id):
	# Get all categories
	categories = session.query(Category).all()

	# Get category
	category = session.query(Category).filter_by(id = catalog_id).first()

	# Get name of category
	categoryName = category.name

	# Get all items of a specific category
	categoryItems = session.query(CategoryItem).filter_by(category_id = catalog_id).all()

	# Get count of category items
	categoryItemsCount = session.query(CategoryItem).filter_by(category_id = catalog_id).count()

	return render_template('category.html', categories = categories, categoryItems = categoryItems, categoryName = categoryName, categoryItemsCount = categoryItemsCount)

@app.route('/categories/<int:category_id>/stocks/<int:stock_id>')
def showCategoryItem(category_id, stock_id):
	# Get category item
	categoryItem = session.query(CategoryItem).filter_by(id = stock_id).first()

	# Get creator of item
	creator = getUserInfo(categoryItem.user_id)

	return render_template('categoryItem.html', categoryItem = categoryItem, creator = creator)

@app.route('/category/add', methods=['GET', 'POST'])
def addCategoryItem():
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	if request.method == 'POST':
		# TODO: Retain data when there is an error

		if not request.form['name']:
			flash('Please add instrument name')
			return redirect(url_for('addCategoryItem'))

		if not request.form['description']:
			flash('Please add a description')
			return redirect(url_for('addCategoryItem'))

		# Add category item
		newCategoryItem = CategoryItem(name = request.form['name'], description = request.form['description'], category_id = request.form['category'], user_id = login_session['user_id'])
		session.add(newCategoryItem)
		session.commit()

		return redirect(url_for('showCategories'))
	else:
		# Get all categories
		categories = session.query(Category).all()

		return render_template('addCategoryStock.html', categories = categories)

@app.route('/category/<int:category_id>/stocks/<int:stock_id>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_id, stock_id):
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	# Get category item
	categoryItem = session.query(CategoryStock).filter_by(id = item_id).first()

	# Get creator of item
	creator = getUserInfo(categoryStock.user_id)

	# Check if logged in user is creator of category item
	if creator.id != login_session['user_id']:
		return redirect('/login')

	# Get all categories
	categories = session.query(Category).all()

	if request.method == 'POST':
		if request.form['name']:
			categoryStock.name = request.form['name']
		if request.form['description']:
			categoryStock.description = request.form['description']
		if request.form['category']:
			categoryStock.category_id = request.form['category']
		return redirect(url_for('showCategoryStock', category_id = categoryStock.category_id ,stock_id = categoryStock.id))
	else:
		return render_template('editCategoryStock.html', categories = categories, categoryStock = categoryStock)

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_id, stock_id):
	# Check if user is logged in
	if 'username' not in login_session:
	    return redirect('/login')

	# Get category item
	categoryStock = session.query(CategoryStock).filter_by(id = stock_id).first()

	# Get creator of item
	creator = getUserInfo(categoryStock.user_id)

	# Check if logged in user is creator of category item
	if creator.id != login_session['user_id']:
		return redirect('/login')

	if request.method == 'POST':
		session.delete(categoryStock)
		session.commit()
		return redirect(url_for('showCategory', catalog_id = categoryStock.category_id))
	else:
		return render_template('deleteCategoryStock.html', categoryStock = categoryStock)

@app.route('/login')
def login():
	# Create anti-forgery state token
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	return render_template('login.html', STATE=state)

@app.route('/logout')
def logout():
	if login_session['provider'] == 'facebook':
		fbdisconnect()
		del login_session['facebook_id']

	if login_session['provider'] == 'google':
		gdisconnect()
		del login_session['gplus_id']
		del login_session['access_token']

	del login_session['username']
	del login_session['email']
	del login_session['picture']
	del login_session['user_id']
	del login_session['provider']

	return redirect(url_for('showCategories'))


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
	# Validate anti-forgery state token
	if request.args.get('state') != login_session['state']:
	    response = make_response(json.dumps('Invalid state parameter.'), 401)
	    response.headers['Content-Type'] = 'application/json'
	    return response

	# Gets acces token
	access_token = request.data
	print "access token received %s " % access_token

	# Gets info from fb clients secrets
	app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
	app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']

	url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]

	# Use token to get user info from API
	userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token
	token = result.split("&")[0]

	url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
	h = httplib2.Http()
	result = h.request(url, 'GET')[1]

	data = json.loads(result)
	login_session['provider'] = 'facebook'
	login_session['username'] = data["name"]
	login_session['email'] = data["email"]
	login_session['facebook_id'] = data["id"]

	# Store token in login_session in order to logout
	stored_token = token.split("=")[1]
	login_session['access_token'] = stored_token


	login_session['picture'] = data["data"]["url"]

	# See if user exists
	user_id = getUserID(login_session['email'])
	if not user_id:
	    user_id = createUser(login_session)
	login_session['user_id'] = user_id

	return "Login Successful!"

@app.route('/fbdisconnect')
def fbdisconnect():
	facebook_id = login_session['facebook_id']
	access_token = login_session['access_token']

	url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
	h = httplib2.Http()
	result = h.request(url, 'DELETE')[1]

	return "you have been logged out"





@app.route('/categories/JSON')
def showCategoriesJSON():
	categories = session.query(Category).all()
	return jsonify(categories = [category.serialize for category in categories])

@app.route('/categories/<int:category_id>/JSON')
@app.route('/categories/<int:category_id>/stocks/JSON')
def showCategoryJSON(catalog_id):
	categoryStocks = session.query(CategoryStock).filter_by(category_id = catalog_id).all()
	return jsonify(categoryStocks = [categoryStock.serialize for categoryStock in categoryStocks])

@app.route('/category/<int:category_id>/stocks/<int:stock_id>/JSON')
def showCategoryItemJSON(category_id, stock_id):
	categoryStock = session.query(CategoryStock).filter_by(id = stock_id).first()
	return jsonify(categoryStock = [categoryStock.serialize])

if __name__ == '__main__':
	app.debug = True
	app.secret_key = 'super_secret_key'
	app.run(host = '0.0.0.0', port = 8070)