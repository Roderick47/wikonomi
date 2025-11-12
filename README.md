# WIKONOMI

A Django-based web application for managing products, businesses, and user interactions.

## Features

- **Product Management**: Add, edit, and manage products with images and descriptions.
- **Business Profiles**: Create and manage business profiles.
- **User Interactions**: Comments, ratings, and follow functionality.
- **Search & Filter**: Advanced search and filtering options.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Roderick47/wikonomi.git
   cd wikonomi
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Contributing

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

3. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a pull request on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
