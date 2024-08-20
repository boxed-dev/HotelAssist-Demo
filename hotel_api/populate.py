from app import app as flask_app, db, Room, User
from sqlalchemy.exc import IntegrityError
#Function to add fake values to the database
def populate_db():

    rooms = [
        Room(room_type='Single', availability=True, price_per_night=100.0),
        Room(room_type='Double', availability=True, price_per_night=150.0),
        Room(room_type='Suite', availability=True, price_per_night=250.0),
        Room(room_type='Single', availability=True, price_per_night=110.0),
        Room(room_type='Double', availability=True, price_per_night=160.0),
        Room(room_type='Suite', availability=True, price_per_night=270.0),
        Room(room_type='Single', availability=True, price_per_night=105.0),
        Room(room_type='Double', availability=True, price_per_night=155.0),
        Room(room_type='Suite', availability=True, price_per_night=260.0),
        Room(room_type='Single', availability=True, price_per_night=115.0),
        Room(room_type='Double', availability=True, price_per_night=165.0),
        Room(room_type='Suite', availability=True, price_per_night=280.0),
        Room(room_type='Single', availability=True, price_per_night=120.0),
        Room(room_type='Double', availability=True, price_per_night=170.0),
        Room(room_type='Suite', availability=True, price_per_night=290.0),
        Room(room_type='Single', availability=True, price_per_night=125.0),
        Room(room_type='Double', availability=True, price_per_night=175.0),
        Room(room_type='Suite', availability=True, price_per_night=300.0)
    ]
    
    # Add some sample users
    users = [
        User(name='John Doe', email='john@example.com'),
        User(name='Jane Smith', email='jane@example.com')
    ]
    
    # Add rooms to the session and commit
    db.session.add_all(rooms)
    db.session.commit()

    for user in users:
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(f"User with email {user.email} already exists. Skipping.")

    print("Database populated with initial data.")

if __name__ == "__main__":
    # Create the Flask app and push an application context
    with flask_app.app_context():
        db.create_all()
        populate_db()