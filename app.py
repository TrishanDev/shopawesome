from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample product data with more details
products = [
    {
        'id': 1, 
        'name': 'Premium Headphones', 
        'price': 149.99,
        'description': 'High-quality wireless headphones with noise cancellation.'
    },
    {
        'id': 2, 
        'name': 'Smart Watch', 
        'price': 199.99,
        'description': 'Feature-rich smart watch with health tracking and notifications.'
    },
    {
        'id': 3, 
        'name': 'Portable Speaker', 
        'price': 79.99,
        'description': 'Waterproof portable speaker with amazing sound quality.'
    },
    {
        'id': 4, 
        'name': 'Laptop Backpack', 
        'price': 59.99,
        'description': 'Durable laptop backpack with anti-theft features and USB charging port.'
    }
]

# Home route - displaying products
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
    # Find the product by its ID
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        # Get cart from session or create an empty one
        cart = session.get('cart', [])
        
        # Check if product already exists in cart
        product_in_cart = False
        for item in cart:
            if item.get('id') == product_id:
                item['quantity'] = item.get('quantity', 1) + 1
                product_in_cart = True
                break
        
        # If not in cart, add with quantity 1
        if not product_in_cart:
            cart_item = product.copy()
            cart_item['quantity'] = 1
            cart.append(cart_item)
        
        # Save cart back to session
        session['cart'] = cart
    
    return redirect(url_for('cart'))

# Remove from cart route
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    
    # Create a new cart without the removed item
    new_cart = [item for item in cart if item.get('id') != product_id]
    
    # Update the session
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

# Cart route - displaying cart items
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# Checkout route - form for checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process the checkout form
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip')
        payment_method = request.form.get('payment')
        
        # In a real app, you would:
        # 1. Validate the form data
        # 2. Process the payment
        # 3. Create an order in the database
        # 4. Send confirmation email
        
        # Clear the cart
        session.pop('cart', None)
        
        # Redirect to order confirmation
        return render_template('order_confirmation.html', name=name)
    
    # GET request - show the checkout form
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('home'))
        
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

# Order confirmation route
@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)