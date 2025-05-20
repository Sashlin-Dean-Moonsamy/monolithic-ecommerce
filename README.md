# Ecommerce Project

This is a Django-based ecommerce project that allows users to browse products, search for items, and manage their shopping experience.

## Overview

The project includes features such as:
- Product browsing and searching
- User authentication
- Shopping cart functionality
- Order management

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ecommerce
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add necessary environment variables:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

- Access the application at `http://localhost:8000`.
- Use the search functionality to find products.
- Register or log in to manage your shopping cart and orders.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 