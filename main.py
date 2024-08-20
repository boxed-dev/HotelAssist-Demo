import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
import requests
import json
import datetime

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

BASE_URL = "http://localhost:5000"

# Tools to INTERACT with Backend
def get_all_rooms(_=None):
    response = requests.get(f"{BASE_URL}/rooms/all")
    return response.json()

def get_available_rooms(_=None):
    response = requests.get(f"{BASE_URL}/rooms")
    return response.json()

def get_room_details(room_id):
    url = f"{BASE_URL}/bookings/{room_id}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    return response.text

def book_room(_=None):
    url = f"{BASE_URL}/book"

    # inputs to be taken to book room
    user_id = input("Assistant: What is your user ID? ")
    room_id = input("Assistant: What is the room ID? ")
    check_in_date = input("Assistant: What is the check-in date? (YYYY-MM-DD) ")
    check_out_date = input("Assistant: What is the check-out date? (YYYY-MM-DD) ")

    # Validate the input
    try:
        datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
        datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format. Please use the format YYYY-MM-DD."

    payload = json.dumps({
        "user_id": user_id,
        "room_id": room_id,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def register_user(input_str):
    try:
        user_data = json.loads(input_str.replace("'", '"'))
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        return response.json()
    except json.JSONDecodeError:
        return "Invalid input format. Please provide user data as a dictionary string."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Tools for different tasks
tools = [
    Tool(
        name="GetAllRooms",
        func=get_all_rooms,
        description="Useful for getting information about all rooms in the hotel. Use this when asked about all rooms."
    ),
    Tool(
        name="GetAvailableRooms",
        func=get_available_rooms,
        description="Useful for getting information about available rooms in the hotel. Use this when asked about available rooms. No input is required."
    ),
    Tool(
        name="GetRoomDetails",
        func=get_room_details,
        description="Useful for getting detailed information about a specific room taking input as. NOTE: Input should be a room ID."
    ),
    Tool(
        name="BookRoom",
        func=book_room,
        description="Useful for booking a room. No input is required. The function will prompt the user for the necessary information."
    ),
    Tool(
        name="RegisterUser",
        func=register_user,
        description="Useful for registering a new user. Input should be a string representation of a dictionary with 'name' and 'email' keys."
    )
]


llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

# Memory to store chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)

# Agent User INteraction Loop
print("Welcome to the Hotel Assistant! How can I help you today?")
print("(Type 'exit' to quit)")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Thank you for using the Hotel Assistant. Goodbye!")
        break

    try:

        agent_output = agent.run(input=user_input)

        # Check if the agent wants to execure task to Book the room
        if "BookRoom" in agent_output:
            # Book the room
            response = book_room()
            print("Assistant:", response)
        else:
            print("Assistant:", agent_output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Assistant: I'm sorry, but I encountered an error while processing your request. Could you please provide me with the missing information?")

        # Asking the user for the missing info
        missing_info = input("Assistant: What information is missing? ")

        # Update the user input with the missing information
        user_input += f" {missing_info}"

        # Run the agent again with the updated user input
        agent_output = agent.run(input=user_input)
        print("Assistant:", agent_output)
