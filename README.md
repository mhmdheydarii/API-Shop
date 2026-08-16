<h1 align="center">Shop REST API</h1>

<p align="center">
A RESTful e-commerce API built with Django and Django REST Framework.
</p>

<hr>

<h2>Features</h2>

<ul>
  <li>User Authentication & Authorization</li>
  <li>JWT Authentication</li>
  <li>Role-Based Permissions</li>
  <li>Product Filtering</li>
  <li>Pagination</li>
  <li>Iranian Phone Number Validation</li>
  <li>Order Management</li>
  <li>Payment Integration</li>
  <li>Admin & Customer Dashboards</li>
</ul>

<h2>Technologies</h2>

<ul>
  <li>Django</li>
  <li>Django REST Framework</li>
  <li>PostgreSQL</li>
  <li>Docker</li>
  <li>Swagger</li>
  <li>Rate Limiting</li>
</ul>

<h2>Project Structure</h2>

<pre>
project/
├── accounts/
├── products/
├── orders/
├── payments/
├── coupons/
├── cart/
├── core/
├── Dockerfile
├── docker-compose.yml
└── README.md
</pre>

<h2>Installation</h2>

<h3>Clone the Repository</h3>

<pre>
git clone https://github.com/your-username/your-repository.git
cd your-repository
</pre>

<h3>Create Virtual Environment</h3>

<pre>
python -m venv .venv
</pre>

<p>Activate the virtual environment:</p>

<pre>
.venv\Scripts\activate
</pre>

<h3>Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>Environment Variables</h3>

<p>
Create a <code>.env</code> file and configure the required environment variables.
</p>

<pre>
SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES_DB=your-database
POSTGRES_USER=your-user
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
</pre>

<h3>Run Migrations</h3>

<pre>
python manage.py migrate
</pre>

<h3>Create Superuser</h3>

<pre>
python manage.py createsuperuser
</pre>

<h3>Run the Development Server</h3>

<pre>
python manage.py runserver
</pre>

<h2>Authentication</h2>

<p>
This API uses JWT-based authentication for securing protected endpoints.
</p>

<ul>
  <li>Access Token</li>
  <li>Refresh Token</li>
</ul>

<h2>API Documentation</h2>

<p>
API documentation will be added here.
</p>

<h2>Swagger</h2>

<p>
Swagger UI is available for exploring and testing the API endpoints.
</p>

<pre>
/swagger/
</pre>

<h2>Docker</h2>

<p>
The project is containerized using Docker and Docker Compose.
</p>

<pre>
docker compose up --build
</pre>

<h2>Testing</h2>

<pre>
python manage.py test
</pre>

<h2>Author</h2>

<p>
Mohammad Hossein Heydari
</p>

<p>
Backend Developer | Python | Django | Django REST Framework
</p>
