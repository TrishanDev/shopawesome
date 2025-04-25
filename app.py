from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Mock user database
users = {
    'example_user': {'password': 'password123', 'name': 'John Doe'}
}

# Sample product data
products = [
    {'id': 1, 'name': 'Premium Headphones', 'price': 149.99, 'description': 'High-quality wireless headphones with noise cancellation.'},
    {'id': 2, 'name': 'Smart Watch', 'price': 199.99, 'description': 'Feature-rich smart watch with health tracking and notifications.'},
    {'id': 3, 'name': 'Portable Speaker', 'price': 79.99, 'description': 'Waterproof portable speaker with amazing sound quality.'},
    {'id': 4, 'name': 'Laptop Backpack', 'price': 59.99, 'description': 'Durable laptop backpack with anti-theft features and USB charging port.'}
]

# Home route
@app.route('/')
def home():
    return render_template('home.html', products=products)

# Product detail route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return redirect(url_for('home'))

# Add to cart route
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', [])
        product_in_cart = False
        for item in cart:
            if item.get('id') == product_id:
                item['quantity'] = item.get('quantity', 1) + 1
                product_in_cart = True
                break
        if not product_in_cart:
            cart_item = product.copy()
            cart_item['quantity'] = 1
            cart.append(cart_item)
        session['cart'] = cart
    return redirect(url_for('cart'))

# Remove from cart route
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    new_cart = [item for item in cart if item.get('id') != product_id]
    session['cart'] = new_cart
    return jsonify({'success': True})

# Update cart quantity
@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    quantity = request.json.get('quantity', 1)
    if quantity <= 0:
        return jsonify({'success': False, 'message': 'Quantity must be positive'})
    cart = session.get('cart', [])
    for item in cart:
        if item.get('id') == product_id:
            item['quantity'] = quantity
            break
    session['cart'] = cart
    return jsonify({'success': True})

# Cart route
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# Checkout route
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip')
        payment_method = request.form.get('payment')
        session.pop('cart', None)
        return render_template('order_confirmation.html', name=name)
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('home'))
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

# Order confirmation route
@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if username in users:
            flash('Username already exists.', 'error')
        elif not username or not password or not name:
            flash('All fields are required.', 'error')
        else:
            users[username] = {'password': password, 'name': name}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username]['password'] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('login.html')

# Profile route
@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please log in.', 'error')
        return redirect(url_for('login'))
    user = users.get(session['user'])
    return render_template('profile.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
