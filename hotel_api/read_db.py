from app import app, db, Room, User

def read_db():
    print("\nReading database contents:")
    
    print("\nRooms:")
    rooms = Room.query.all()
    for room in rooms:
        print(f"ID: {room.id}, Type: {room.room_type}, Available: {room.availability}, Price: ${room.price_per_night}")
    
    print("\nUsers:")
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")

if __name__ == "__main__":
    with app.app_context():
        read_db()

print("\nDatabase contents displayed.")