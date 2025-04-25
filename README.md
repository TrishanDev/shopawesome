# ShopAwesome – Flask E-commerce App

**ShopAwesome** is a minimal and elegant e-commerce web application built with Python (Flask). It’s designed for fast deployment, small product showcases, and educational or commercial use. The codebase is clean, modular, and easy to extend.

---

## Features

- Modern and responsive user interface  
- Product listing with images  
- Add to Cart functionality  
- Real-time cart with total calculation  
- Static checkout page (demo version)  
- Organized folder structure for clarity and scalability

---

## Project Structure

```
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── product1.jpg
│       ├── product2.jpg
│       └── product3.jpg
└── templates/
    ├── base.html
    ├── home.html
    ├── cart.html
    └── checkout.html
```

---

## Local Setup

1.Got to the file directory on your device and open with any code editor(eg. VS Code)
   ```

2. Install dependencies  
   ```
   pip install -r requirements.txt
   ```

3. Run the app  
   ```
   python app.py
   ```

4. Open your browser at  
   ```
   http://localhost:5000

   http://127.0.0.1:5000/
   ```

---

## Deployment

To deploy on platforms like Acquirebase, Render, or Railway:

- Ensure the `requirements.txt` file is included
- Use this command in production:
  ```
  gunicorn app:app
  ```

For platforms requiring a `Procfile`, you can include:
```
web: gunicorn app:app
```

---

## License

This project is open-source and free to use. You may modify, distribute, and build upon it. Attribution is appreciated.
