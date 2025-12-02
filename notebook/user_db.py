# user_db.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",
        database="fooddatabase"
    )


# Create a new user
def create_user(name, age, gender, ethnicity, marital_status, height_cm, weight_kg, bmi):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO user_profile
    (name, age, gender, ethnicity, marital_status, height_cm, weight_kg, bmi)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (name, age, gender, ethnicity, marital_status, height_cm, weight_kg, bmi))
    conn.commit()
    user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return user_id


# Add Conditions

def add_conditions(user_id, conditions_list):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO user_conditions (user_id, condition_name) VALUES (%s, %s)"

    for cond in conditions_list:
        cursor.execute(sql, (user_id, cond.strip()))

    conn.commit()
    cursor.close()
    conn.close()


# Add Medications

def add_medications(user_id, medication_list):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO user_medications (user_id, medication_name) VALUES (%s, %s)"

    for med in medication_list:
        cursor.execute(sql, (user_id, med.strip()))

    conn.commit()
    cursor.close()
    conn.close()


# Fetch user profile

def get_user_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_profile WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result


# Fetch user conditions

def get_user_conditions(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT condition_name FROM user_conditions WHERE user_id = %s", (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row["condition_name"] for row in rows]


# Fetch user medications
def get_user_medications(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT medication_name FROM user_medications WHERE user_id = %s", (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row["medication_name"] for row in rows]


# Fetch user NAME
def get_user_name(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM user_profile WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result["name"] if result else None


# Runtime: Ask user whether they are new/existing
def get_or_create_user():
    print("\nDo you already have a User ID?")
    ans = input("(y/n): ").lower().strip()

    if ans == "y":
        user_id = int(input("Enter your User ID: ").strip())
        profile = get_user_profile(user_id)

        if profile:
            print(f"\nLoaded profile for user_id {user_id}.")
            return user_id
        else:
            print("\nInvalid user_id. Creating a new profile instead.\n")

    # New User Flow

    print("\nCreating a new user profile...\n")

    name = input("Enter your name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    ethnicity = input("Ethnicity: ")
    marital_status = input("Marital status: ")
    height_cm = float(input("Height (cm): "))
    weight_kg = float(input("Weight (kg): "))

    bmi = weight_kg / ((height_cm / 100) ** 2)

    user_id = create_user(name, age, gender, ethnicity, marital_status, height_cm, weight_kg, bmi)

    # CONDITIONS INPUT
    print("\nEnter any medical conditions (comma separated). Example: high bp, diabetic")
    cond_input = input("Conditions: ").strip()

    if cond_input:
        add_conditions(user_id, cond_input.split(","))

    # MEDICATIONS INPUT
    print("\nEnter medications you take (comma separated). Example: metformin, amlodipine")
    med_input = input("Medications: ").strip()

    if med_input:
        add_medications(user_id, med_input.split(","))

    print(f"\nUser successfully created! Your User ID is: {user_id}\n")
    return user_id