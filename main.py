#people have tried understanding the code but they cant and count if you are one of them
#only me and God undestand
#count = 20
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

# Function to fetch one record from Property table
def fetch_one_property(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Property LIMIT 1;")
        record = cur.fetchone()
        print("Fetched one record from Property table:", record)
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
    # Check if tables exist
    if not tables_exist(conn):
        # Create tables if they don't exist
        create_tables(conn)
        # Insert data into Property table
        insert_property_data(conn)
    else:
        print("Tables already exist")
    # Test fetching one record
    fetch_one_property(conn)
    # Test fetching all records
    fetch_all_property(conn)
    # Close connection
    conn.close()
