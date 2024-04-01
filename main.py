
#people have tried understanding the code but they cant add count if you are one of them
#only me and God undestand 🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿
#count = 20


#class collab 
import psycopg2
from psycopg2 import sql
from datetime import date

# Function to connect to PostgreSQL
def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="home",
        port="5000",
        user="postgres",
        password="admin"
    )
    return conn


def tables_exist(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM   information_schema.tables 
            WHERE  table_name = 'property'
        );
    """)
    exists = cur.fetchone()[0]
    cur.close()
    return exists


def create_tables(conn):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS Property (
            Property_ID SERIAL PRIMARY KEY,
            Property_Name VARCHAR(20),
            Address VARCHAR(20),
            City VARCHAR(10),
            State VARCHAR(10),
            Zip_Code VARCHAR(20),
            Type VARCHAR(50),
            Size INTEGER,
            Rental_Rate NUMERIC(10, 2),
            Status VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Landlord (
            Landlord_ID SERIAL PRIMARY KEY,
            First_Name VARCHAR(10),
            Last_Name VARCHAR(10),
            Email VARCHAR(20),
            Phone VARCHAR(20),
            Address VARCHAR(20),
            City VARCHAR(100),
            State VARCHAR(10),
            Zip_Code VARCHAR(20)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Tenants (
            Tenant_ID SERIAL PRIMARY KEY,
            First_Name VARCHAR(10),
            Last_Name VARCHAR(10),
            Email VARCHAR(20),
            Phone VARCHAR(20),
            Address VARCHAR(20),
            City VARCHAR(10),
            State VARCHAR(10),
            Zip_Code VARCHAR(20),
            Start_Date DATE,
            End_Date DATE,
            Property_ID INTEGER REFERENCES Property(Property_ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Maintenance (
            Maintenance_ID SERIAL PRIMARY KEY,
            Property_ID INTEGER REFERENCES Property(Property_ID),
            Description TEXT,
            Date_Requested DATE,
            Date_Completed DATE,
            Cost NUMERIC(10, 2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Payments (
            Payment_ID SERIAL PRIMARY KEY,
            Amount NUMERIC(10, 2),
            Date DATE,
            Payment_Method VARCHAR(50),
            Tenant_ID INTEGER REFERENCES Tenants(Tenant_ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Amenities (
            Amenity_ID SERIAL PRIMARY KEY,
            Amenity_Name VARCHAR(10),
            Description TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Property_Amenities (
            Property_Amenity_ID SERIAL PRIMARY KEY,
            Property_ID INTEGER REFERENCES Property(Property_ID),
            Amenity_ID INTEGER REFERENCES Amenities(Amenity_ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Landlord_Contract (
            Contract_ID SERIAL PRIMARY KEY,
            Landlord_ID INTEGER REFERENCES Landlord(Landlord_ID),
            Start_Date DATE,
            End_Date DATE,
            Terms TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Tenant_Contract (
            Contract_ID SERIAL PRIMARY KEY,
            Tenant_ID INTEGER REFERENCES Tenants(Tenant_ID),
            Start_Date DATE,
            End_Date DATE,
            Terms TEXT
        )
        """
    )
    try:
        cur = conn.cursor()
        # create tables if they don't exist
        for command in commands:
            cur.execute(command)
        # commit changes
        conn.commit()
        print("Tables created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to insert data into Property table
def insert_property_data(conn):
    try:
        cur = conn.cursor()
        # Insert data with parameterized query
        property_data = [
            ("Property1", "123 Main St", "Nairobi", "Nairobi", "0010", "Apartment", 1000, 1500.00, "Available"),
            ("Property2", "456 Central Ave", "Mombasa", "Mombasa", "00200", "House", 1500, 2000.00, "Occupied"),
            ("Property3", "789 Park Rd", "Kisumu", "Kisumu", "00300", "Condo", 1200, 1800.00, "Available"),
            ("Property4", "101 River St", "Nakuru", "Nakuru", "00400", "Duplex", 1300, 2200.00, "Available"),
            ("Property5", "111 Garden Blvd", "Eldoret", "Uasin Gishu", "00500", "Townhouse", 1100, 1600.00, "Occupied"),
            ("Property6", "222 Lakeview Dr", "Thika", "Kiambu", "00600", "Villa", 1700, 2500.00, "Available"),
            ("Property7", "333 Mountain Rd", "Kakamega", "Kakamega", "00700", "Penthouse", 1400, 2300.00, "Available"),
            ("Property8", "444 Beach Ave", "Malindi", "Kilifi", "00800", "Cottage", 1600, 2000.00, "Occupied")
        ]
        for data in property_data:
            cur.execute("""
                INSERT INTO Property (Property_Name, Address, City, State, Zip_Code, Type, Size, Rental_Rate, Status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, data)
        conn.commit()
        print("Property data inserted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to bulk delete records from Property table
def bulk_delete_property(conn, property_ids):
    try:
        cur = conn.cursor()
        # Bulk Delete
        bulk_delete_query = """
        DELETE FROM Property 
        WHERE Property_ID IN %s;
        """
        cur.execute(bulk_delete_query, (tuple(property_ids),))
        conn.commit()
        print("Bulk delete operation completed successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to perform INNER JOIN example
def inner_join_example(conn):
    try:
        cur = conn.cursor()
        inner_join_query = """
        SELECT Property.Property_Name, Property.Address, Landlord.First_Name, Landlord.Last_Name
        FROM Property
        INNER JOIN Landlord ON Property.Property_ID = Landlord.Property_ID;
        """
        cur.execute(inner_join_query)
        inner_join_result = cur.fetchall()
        print("\nINNER JOIN Result:")
        for row in inner_join_result:
            print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to perform CROSS JOIN example
def cross_join_example(conn):
    try:
        cur = conn.cursor()
        cross_join_query = """
        SELECT Property.Property_Name, Landlord.First_Name
        FROM Property
        CROSS JOIN Landlord;
        """
        cur.execute(cross_join_query)
        cross_join_result = cur.fetchall()
        print("\nCROSS JOIN Result:")
        for row in cross_join_result:
            print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to perform UPDATE operation
def update_property_status(conn, property_id, new_status):
    try:
        cur = conn.cursor()
        update_query = """
        UPDATE Property
        SET Status = %s
        WHERE Property_ID = %s;
        """
        cur.execute(update_query, (new_status, property_id))
        conn.commit()
        print("Property status updated successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Function to fetch all records from Property table
def fetch_all_property(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Property;")
        records = cur.fetchall()
        print("Fetched all records from Property table:", records)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Main function
if __name__ == '__main__':
    # Connect to PostgreSQL
    conn = connect()
    try:
        # Create tables if they don't exist
        create_tables(conn)
        # Insert data into Property table
        insert_property_data(conn)
        # Test fetching all records
        fetch_all_property(conn)
        # Test bulk delete
        bulk_delete_property(conn, [1, 3, 5])
        # Test fetching all records after bulk delete
        fetch_all_property(conn)
        # Test INNER JOIN
        inner_join_example(conn)
        # Test CROSS JOIN
        cross_join_example(conn)
        # Test UPDATE
        update_property_status(conn, 2, "Unavailable")
        # Fetch all records after update
        fetch_all_property(conn)
        # Print PostgreSQL database version
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print('PostgreSQL database version:', db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection terminated.')
            
'''
Database connection
The connection function is used to connect the application backend together with the database. Which is postgres. Details In a connection function.


Table creations
Create_tables is a function used to create many tables in a database together to avoid delays and create other tables if they do not exist.
Do not duplicate creation of tables we used a do note create if exitst function.
Data insertion
Used to insert data to created table quickly: 

Error handling:
Error handling is implemented using try-except blocks to catch any exceptions that may occur during database operations. Exceptions are printed for debugging purposes.
Parametrised quieres:
Parameterized queries are utilized throughout the code to prevent SQL injection attacks and improve query performance. They are employed in INSERT, DELETE, UPDATE, and SELECT statements
Bulk update, Bulk delete, Fechone, fetchall and fechmany() API python calls:
The `fetch_all_property()` function fetches all records from the `Property` table using the `fetchall()` method. It retrieves all rows from the result set and prints them.
The `inner_join_example()` function performs an INNER JOIN between the `Property` and `Landlord` tables, demonstrating the usage of the `fetchall()` method to retrieve and print the result set.
The `cross_join_example()` function executes a CROSS JOIN between the `Property` and `Landlord` tables and utilizes the `fetchall()` method to fetch and display the result set.


'''