import psycopg2

# establishing the connection
def db_connector():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="6543",
    )
    # #Creating a cursor object using the cursor() method
    # cursor = conn.cursor()

    # #Executing an MYSQL function using the execute() method
    # #sample query to check if data is fetching fine
    # cursor.execute("select * from indexooor")

    # # Fetch a single row using fetchone() method.
    # data = cursor.fetchall()
    # print("Connection established to: ",data)
    return conn
    # Closing the connection
