from cv2 import data
import psycopg2
import pickle

def add_encode(name,encoding):

    
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="mirrag",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="face_recognition")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO encodings (name, encoding) VALUES (%s,%s)"""
        record_to_insert = (name,pickle.dumps(encoding))
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into encodings table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def read_encodings():
    """Reads the encodings from the database

    Returns:
        list of encodings and names 
    """

    try:
        connection = psycopg2.connect(user="postgres",
                                    password="mirrag",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="face_recognition")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from encodings"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from enocding table using cursor.fetchall")
        data = cursor.fetchall()
        encodings = []
        names = []
        print("Print each row and it's columns values")
        for row in data:
            name = row[0]
            #print("name = ", row[0], )
            names.append(name)
            enocde = pickle.loads(row[1])
            encodings.append(enocde)
            #print("encoding = ",enocde)


    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return names,encodings