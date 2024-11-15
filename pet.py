import mysql.connector
from datetime import datetime

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your username
    password="",  # Replace with your password
    database="pet_adoption"
)

cursor = db.cursor()

# Function to add a new pet
def add_pet(name, species, breed, age, description):
    sql = "INSERT INTO pets (name, species, breed, age, description) VALUES (%s, %s, %s, %s, %s)"
    values = (name, species, breed, age, description)
    cursor.execute(sql, values)
    db.commit()
    print(f"Pet '{name}' added successfully.")

# Function to register a user
def register_user(name, email, phone):
    sql = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
    values = (name, email, phone)
    cursor.execute(sql, values)
    db.commit()
    print(f"User '{name}' registered successfully.")

# Function to record adoption
def adopt_pet(user_id, pet_id):
    # Check if the pet is already adopted
    cursor.execute("SELECT is_adopted FROM pets WHERE id = %s", (pet_id,))
    pet = cursor.fetchone()
    if pet and pet[0]:
        print("This pet is already adopted.")
        return

    # Record the adoption
    sql = "INSERT INTO adoption_history (user_id, pet_id, adoption_date) VALUES (%s, %s, %s)"
    values = (user_id, pet_id, datetime.now().date())
    cursor.execute(sql, values)

    # Update pet's adoption status
    cursor.execute("UPDATE pets SET is_adopted = 1 WHERE id = %s", (pet_id,))
    db.commit()
    print("Adoption recorded successfully.")

# Function to view available pets
def view_available_pets():
    cursor.execute("SELECT * FROM pets WHERE is_adopted = 0")
    pets = cursor.fetchall()
    for pet in pets:
        print(f"ID: {pet[0]}, Name: {pet[1]}, Species: {pet[2]}, Breed: {pet[3]}, Age: {pet[4]}")

# Function to view adoption history
def view_adoption_history():
    cursor.execute("""
        SELECT u.name AS user_name, p.name AS pet_name, a.adoption_date 
        FROM adoption_history a
        JOIN users u ON a.user_id = u.id
        JOIN pets p ON a.pet_id = p.id
    """)
    history = cursor.fetchall()
    for record in history:
        print(f"User: {record[0]}, Pet: {record[1]}, Date: {record[2]}")

# Sample execution
# Add pets
add_pet("Bella", "Dog", "Labrador", 3, "Friendly and playful.")
add_pet("Mittens", "Cat", "Persian", 2, "Quiet and affectionate.")

# Register users
register_user("Alice", "alice@example.com", "1234567890")
register_user("Bob", "bob@example.com", "9876543210")

# Adopt a pet
adopt_pet(user_id=1, pet_id=1)

# View available pets
print("\nAvailable Pets:")
view_available_pets()

# View adoption history
print("\nAdoption History:")
view_adoption_history()

import streamlit as st

# Simplified Streamlit interface
st.title("Pet Adoption Platform")

choice = st.sidebar.selectbox("Menu", ["Add Pet", "View Pets", "Adopt Pet", "View Adoption History"])

if choice == "Add Pet":
    name = st.text_input("Name")
    species = st.text_input("Species")
    breed = st.text_input("Breed")
    age = st.number_input("Age", min_value=0, max_value=30, step=1)
    description = st.text_area("Description")
    if st.button("Add Pet"):
        add_pet(name, species, breed, age, description)
        st.success("Pet added successfully!")

elif choice == "View Pets":
    st.write("Available Pets:")
    pets = view_available_pets()
    st.write(pets)

elif choice == "Adopt Pet":
    user_id = st.number_input("User ID", min_value=1, step=1)
    pet_id = st.number_input("Pet ID", min_value=1, step=1)
    if st.button("Adopt"):
        adopt_pet(user_id, pet_id)
        st.success("Adoption recorded!")

elif choice == "View Adoption History":
    st.write("Adoption History:")
    history = view_adoption_history()
    st.write(history)
