# Finder Home Electric Charger

## Overview
Finder Home Electric Charger is a Python-based application designed to connect electric car owners searching for a charging station with homeowners who have a space to accommodate cars for charging. This app aims to simplify the process of finding and offering electric car charging spots, fostering a community-driven solution to the growing demand for EV charging infrastructure.

## Features 

- **User Registration**: Separate registration for electric car owners and homeowners.
- **Search Functionality**: Electric car owners can search for nearby charging spots based on location.
- **Listing Management**: Homeowners can list their charging spots with details such as availability, pricing, and amenities.
- **Booking System**: Electric car owners can book charging spots directly through the app.
- **Payment Integration**: Secure payment options for seamless transactions.
- **Rating and Reviews**: Users can rate and review charging spots and experiences.
- **Notifications**: Real-time notifications for booking confirmations, cancellations, and updates.

## Technologies Used
- **Programming Language**: Python
- **Frameworks**: Flask/Django (for backend development)
- **Database**: SQLite/PostgreSQL (for storing user and listing data)
- **Frontend**: HTML, CSS, JavaScript (for user interface)
- **APIs**: Google Maps API (for location-based search)
- **Payment Gateway**: Stripe/PayPal (for handling payments)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/finder_home_electric_charger.git
   
    cd finder_home_electric_charger
    
   #Navigate to the project directory:
    cd finder_home_electric_charger
   ```
## Create a virtual environment:
```bash
python -m venv venv
```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
 
    
3. Set up the database:
   - Run the following command to create the database tables:
     ```bash
     python -c "from models import db; db.create_all()"
     ```
4. Configure the application:
5. Set up environment variables for sensitive information (e.g., database URI, API keys).
   - Create a `.env` file in the root directory and add your configurations:
     ```bash
     DATABASE_URI=your_database_uri
     GOOGLE_MAPS_API_KEY=your_google_maps_api_key
     STRIPE_API_KEY=your_stripe_api_key
     ```

### README: How to Modify or Add a Table and Generate & Apply Migrations

This guide explains how to modify an existing table or add a new table in your project and apply the changes using Alembic.

---

### **1. Modify or Add a Table**
1. **Locate the Models**:
   - Open the file where your SQLAlchemy models are defined (e.g., `src/core/services/models.py`).

2. **Modify an Existing Table**:
   - Update the model class to reflect the changes. For example, to add a new column:
     ```python
     from sqlalchemy import Column, String

     class User(Base):
         __tablename__ = 'users'
         # Existing columns...
         new_column = Column(String(100), nullable=True)  # Add a new column
     ```

3. **Add a New Table**:
   - Define a new model class for the table:
     ```python
     from sqlalchemy import Column, Integer, String

     class NewTable(Base):
         __tablename__ = 'new_table'
         id = Column(Integer, primary_key=True, autoincrement=True)
         name = Column(String(100), nullable=False)
     ```

---

### **2. Generate a Migration**
Run the following command to generate a migration script:
```bash
alembic revision --autogenerate -m "Describe your changes"
```
- Alembic will detect changes in your models and create a migration script in the `alembic/versions` directory.

---

### **3. Review the Migration Script**
- Open the generated migration file (e.g., `alembic/versions/<revision_id>_describe_your_changes.py`).
- Verify that the `upgrade()` and `downgrade()` functions correctly reflect your changes.

---

### **4. Apply the Migration**
Run the following command to apply the migration to your database:
```bash
alembic upgrade head
```
This will execute the `upgrade()` function in the migration script and apply the changes to the database.

---

### **5. Verify the Changes**
- Use a database client or query tool to confirm that the changes have been applied to the database.

---

### Notes:
- Always back up your database before applying migrations in production.
- If you encounter issues, check the Alembic logs or the generated migration script for errors.


### Contributing
Contributions are welcome! Please follow these steps:  
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
git checkout -b feature-name
3. Commit your changes:
git commit -m "Add feature-name"
4. Push to your branch:
git push origin feature-name
5. Open a pull request.
### License
This project is licensed under the MIT License. See the LICENSE file for details.