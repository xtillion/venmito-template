from sqlalchemy import text

class Person:
    def __init__(self, id, first_name, last_name, telephone, email, android, desktop, iphone, city, country):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.telephone = telephone
        self.email = email
        self.android = bool(android)
        self.desktop = bool(desktop)
        self.iphone = bool(iphone)
        self.city = city
        self.country = country

    def __repr__(self):
        return (f"Person(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, "
                f"telephone={self.telephone}, email={self.email}, android={self.android}, "
                f"desktop={self.desktop}, iphone={self.iphone}, city={self.city}, country={self.country})")

    @staticmethod
    def insert_person(engine, person):
        try:
            with engine.connect() as connection:
                query = text("""
                    INSERT INTO person (id, first_name, last_name, telephone, email, android, desktop, iphone, city, country)
                    VALUES (:id, :first_name, :last_name, :telephone, :email, :android, :desktop, :iphone, :city, :country)
                    ON CONFLICT (id) DO NOTHING
                """)
                result = connection.execute(query, {
                    'id': person.id,
                    'first_name': person.first_name,
                    'last_name': person.last_name,
                    'telephone': person.telephone,
                    'email': person.email,
                    'android': person.android,
                    'desktop': person.desktop,
                    'iphone': person.iphone,
                    'city': person.city,
                    'country': person.country
                })
                
                if result.rowcount > 0:
                    connection.commit()
                    print(f"Successfully inserted person {person.id}")
                else:
                    connection.rollback()
                    print(f"Person {person.id} already exists, skipping insertion.")
        except Exception as e:
            print(f"Error inserting person {person.id}: {e}") 