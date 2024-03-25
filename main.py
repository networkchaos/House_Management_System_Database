#people have tried understanding the code but they cant and count if you are one of them
#only me and God undestand
#count = 20
import psycopg2
from psycopg2 import sql

# Function to connect to PostgreSQL
#cofigure the following connection according to your satisfaction

def connect():
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="localhost"
    )
    return conn

# Function to check if tables exist
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

# Function to create tables
def create_tables(conn):
    commands = (
        """
        CREATE TABLE IF NOT EXISTS Property (
            Property_ID SERIAL PRIMARY KEY,
            Property_Name VARCHAR(255),
            Address VARCHAR(255),
            City VARCHAR(100),
            State VARCHAR(100),
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
            First_Name VARCHAR(100),
            Last_Name VARCHAR(100),
            Email VARCHAR(255),
            Phone VARCHAR(20),
            Address VARCHAR(255),
            City VARCHAR(100),
            State VARCHAR(100),
            Zip_Code VARCHAR(20)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Tenants (
            Tenant_ID SERIAL PRIMARY KEY,
            First_Name VARCHAR(100),
            Last_Name VARCHAR(100),
            Email VARCHAR(255),
            Phone VARCHAR(20),
            Address VARCHAR(255),
            City VARCHAR(100),
            State VARCHAR(100),
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
            Tenant_ID INTEGER REFERENCES Tenants(Tenant_ID),
            Booking_ID INTEGER REFERENCES Booking(Booking_ID)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Amenities (
            Amenity_ID SERIAL PRIMARY KEY,
            Amenity_Name VARCHAR(100),
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

# Main function
if __name__ == '__main__':
    # Connect to PostgreSQL
    conn = connect()
    # Check if tables exist
    if not tables_exist(conn):
        # Create tables if they don't exist
        create_tables(conn)
    else:
        print("Tables already exist")
    # Close connection
    conn.close()
