import psycopg2
import getpass

# user = input("username: ")
# password = getpass.getpass('Password:')

conn = psycopg2.connect(dbname="axl3210", user="axl3210", password="just@send@it!", host="reddwarf.cs.rit.edu", port="5432")
cursor = conn.cursor()

# execute a command and print result
def execute( string, toPrint = True ):
    cursor.execute(string)

    if toPrint:
        print(cursor.fetchone())


def reloadSchema():
    print("Wiping schema...")
    cursor.execute("DROP schema DataFest2018 cascade;")

    print("Creating schema...")
    cursor.execute("CREATE schema DataFest2018;")

    setPath()


# set search path to package schema
def setPath():
    cursor.execute("SET search_path TO DataFest2018;")

def create():
    commands = [
        """CREATE TYPE package_type AS ENUM('Flat Envelope','Small Box','Medium Box','Big Box');""",
        """
        CREATE TYPE Address AS(
            street varchar(64),
            city varchar(64),
            province varchar(64),
            country varchar(64),
            zip varchar(5),
            number integer,
            type address_type
            );
        """,
        """
        CREATE TABLE Recipient(
            name VARCHAR(256),
            address Address,
            PRIMARY KEY(address, name)
            );
        """,
        """
        CREATE FUNCTION update_order_cost() RETURNS trigger AS $update_order_cost$
            BEGIN                  
                UPDATE orders
                SET cost = cost + NEW.cost
                WHERE order_id = NEW.order_id;
                RETURN NULL;
            END;
        $update_order_cost$ LANGUAGE plpgsql;
        """,
        """
        CREATE TRIGGER update_cost
        AFTER INSERT OR UPDATE ON package
        FOR EACH ROW EXECUTE PROCEDURE update_order_cost();
        """,
        """
        CREATE INDEX address_index on customer(address);
        """,
        """
        INSERT INTO admin VALUES ('admin', 'admin', 'admin');
        """,
        """
        INSERT INTO deliverydepartment VALUES ('delivery', 'delivery', 'delivery');
        """
    ]
    for command in commands:
        cursor.execute(command)


if __name__ == '__main__':
    try:
        reloadSchema()
        create()
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
