from flask import Flask, jsonify, request
from models import db, Room, User, Booking
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Endpoint to get room availability
@app.route('/rooms', methods=['GET'])
def get_rooms():
    available_rooms = Room.query.filter_by(availability=True).all()
    return jsonify({"available_rooms": [room.as_dict() for room in available_rooms]})

# Endpoint to get room details by ID
@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room_details(room_id):
    room = Room.query.get(room_id)
    if room:
        return jsonify(room.as_dict())
    else:
        return jsonify({"error": "Room not found"}), 404

# Endpoint to get all room details
@app.route('/rooms/all', methods=['GET'])
def get_all_rooms():
    all_rooms = Room.query.all()
    return jsonify({"rooms": [room.as_dict() for room in all_rooms]})

# Endpoint to register a new user
@app.route('/register', methods=['POST'])
def register_user():
    new_user = User(
        name=request.json.get('name'),
        email=request.json.get('email')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict()), 201

# Endpoint to create a booking
@app.route('/book', methods=['POST'])
def book_room():
    user_id = request.json.get('user_id')
    room_id = request.json.get('room_id')
    check_in_date = datetime.strptime(request.json.get('check_in_date'), '%Y-%m-%d').date()
    check_out_date = datetime.strptime(request.json.get('check_out_date'), '%Y-%m-%d').date()

    # Way to Check if the room is available
    room = Room.query.get(room_id)
    if room and room.availability:
        # Create a new booking
        new_booking = Booking(
            user_id=user_id,
            room_id=room_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )
        db.session.add(new_booking)

        # Update room availability to prevent double booking
        room.availability = False
        db.session.commit()
        
        return jsonify(new_booking.as_dict()), 201
    else:
        return jsonify({"error": "Room is not available"}), 400

# Endpoint to get bookings for a user
@app.route('/bookings/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify({"bookings": [booking.as_dict() for booking in bookings]})

# Fxn to convert model instances to dictionaries
def model_to_dict(model_instance):
    return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}

Room.as_dict = model_to_dict
User.as_dict = model_to_dict
Booking.as_dict = model_to_dict

if __name__ == '__main__':
    app.run(debug=True)