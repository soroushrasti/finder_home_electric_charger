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

### Project Structure

finder_home_electric_charger/
├── app.py                # Main application file
├── templates/            # HTML templates for the frontend
├── static/               # Static files (CSS, JavaScript, images)
├── models.py             # Database models
├── routes.py             # Application routes
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


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