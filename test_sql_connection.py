import pyodbc
import getpass

server = "172.26.0.1,1433"
database = "AdventureWorks2022"
username = "ansible_reader"

password = getpass.getpass("Enter SQL password: ")

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string)

    print("\nConnection successful!")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT TOP 10
            BusinessEntityID,
            FirstName,
            LastName
        FROM Person.Person
    """)

    rows = cursor.fetchall()

    print("\nQuery Result:")
    print("-" * 50)

    for row in rows:
        print(row)

    cursor.close()
    connection.close()

    print("\nConnection closed.")

except pyodbc.Error as error:
    print("\nDatabase connection/query failed:")
    print(error)
