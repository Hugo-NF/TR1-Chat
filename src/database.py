import io
import sqlite3


class Message:
    def __init__(self, id_message, id_user, id_room, message_text, created_at):
        self.id_message =  id_message
        self.id_user = id_user
        self.id_room = id_room
        self.messsage_text = message_text
        self.created_at = created_at

class Room:
    def __init__(self, id_room, room_name, no_connected=0):
        self.id_room = id_room
        self.room_name = room_name
        self.no_connected = no_connected


class User:
    def __init__(self, id_user, display_name, id_room=None):
        self.id_user = id_user
        self.display_name = display_name
        self.id_room = id_room


class Database:
    """Class to manage a connection with application's sqlite3 database"""

    def __init__(self, database_name):
        """Opens a database connection. If database doesn't exists, a new one is created"""
        self.database_name = database_name
        try:
            self.conn = sqlite3.connect("file:{dbname}?mode=rw"
                                    .format(dbname=database_name), uri=True)
        except sqlite3.OperationalError:
            self.create_schema(database_name)

    def create_schema(self, database_name):
        """Create the database schema"""
        self.conn = sqlite3.connect(database_name)
        cursor = self.conn.cursor()

        # Messages table
        cursor.execute("""
            CREATE TABLE `messages` (
            	`id_message`	INTEGER NOT NULL,
            	`id_user`	INTEGER NOT NULL,
            	`id_room`	INTEGER NOT NULL,
            	`message_text`	TEXT NOT NULL,
            	`created_at`	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            	FOREIGN KEY(`id_room`) REFERENCES `rooms`(`id_room`),
            	FOREIGN KEY(`id_user`) REFERENCES `users`(`id_user`),
            	PRIMARY KEY(`id_message`)
            );           
         """)

        # Rooms table
        cursor.execute("""
            CREATE TABLE `rooms` (
                `id_room`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `room_name`	VARCHAR ( 255 ) NOT NULL,
                `no_connected`	INTEGER DEFAULT 0
            );
        """)

        # Users table
        cursor.execute("""
            CREATE TABLE `users` (
            `id_user`	INTEGER NOT NULL,
            `display_name`	VARCHAR ( 25 ) NOT NULL UNIQUE,
            `id_room`	INTEGER DEFAULT NULL,
            PRIMARY KEY(`id_user`)
             );    
        """)

        self.conn.commit()

    def get_user_by(self, attr, value):
        """Returns a list of users matching the pair 'attr' = 'value'"""
        users = []
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM users WHERE {attr} = '{value}'
        """.format(attr=attr, value=value))

        for row in cursor.fetchall():
            users.append(User(*row))

        return users

    def add_user(self, user, echo=True):
        """Adds an user to database and echoes it's object or not"""

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (display_name, id_room)
            VALUES ('{display_name}', {id_room})
        """.format(display_name=user.display_name, id_room='NULL' if user.id_room is None else user.id_room))
        self.conn.commit()

        # Returns just added user
        if echo:
            cursor.execute("""SELECT * FROM users WHERE display_name = {}""".format(user.display_name))
            answer = []
            for row in cursor.fetchall():
                answer.append(User(*row))
            return answer

    def delete_user(self, user):
        """Deletes an user using it's ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM users WHERE id_user = {id_user}
        """.format(id_user=user.id_user))
        self.conn.commit()

    def update_user_room(self, user):
        """Update user's id_room foreign key"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE users SET id_room = {id_room}
            WHERE id_user = {id_user}
        """.format(id_user=user.id_user, id_room='NULL' if user.id_room is None else user.id_room))
        self.conn.commit()

    def get_room_by(self, attr, value):
        """Returns a list of rooms matching the pair 'attr' = 'value'"""
        rooms = []
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM rooms WHERE {attr} = '{value}'
        """.format(attr=attr, value=value))

        for row in cursor.fetchall():
            rooms.append(Room(*row))

        return rooms

    def add_room(self, room, echo=True):
        """Adds a new room and echoes it's object or not"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO rooms (room_name)
            VALUES ('{room_name}')
        """.format(room_name=room.room_name))
        self.conn.commit()

        if echo:
            cursor.execute("""SELECT * FROM rooms WHERE room_name = {}""".format(room.room_name))
            answer = []
            for row in cursor.fetchall():
                answer.append(Room(*row))
            return answer

    def delete_room(self, room):
        """Deletes a room using it's ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM rooms WHERE id_room = {id_room}
        """.format(id_room=room.id_room))
        self.conn.commit()

    def get_message_by(self, attr, value):
        """Returns a list of messages matching the pair 'attr' = 'value'"""
        messages = []
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM messages WHERE {attr} = '{value}'
        """.format(attr=attr, value=value))

        for row in cursor.fetchall():
            messages.append(Message(*row))

        return messages

    def add_message(self, message, echo=True):
        """Adds a message to database and echoes it's object or not"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (id_user, id_room, message_text)
            VALUES ({id_user}, {id_room}, '{message_text}')
        """.format(id_user=message.id_user, id_room=message.id_room, message_text=message.messsage_text))
        self.conn.commit()

        if echo:
            cursor.execute("""SELECT * FROM messages WHERE id_message = {}""".format(cursor.lastrowid))
            answer = []
            for row in cursor.fetchall():
                answer.append(Message(*row))
            return answer

    def delete_message(self, message):
        """Deletes an message from database using it's ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            DELETE FROM messages WHERE id_message = {id_message}
        """.format(id_message=message.id_message))
        self.conn.commit()

    def run_sql(self, sql):
        """Runs and commits a SQL query"""
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor

    def dump_db_to_sql(self):
        """Export all database to file as .sql file"""
        with io.open(self.database_name+".sql", 'w') as file:
            for line in self.conn.iterdump():
                file.write("%s\n" % line)
        file.close()

    def close_connection(self, commit=True):
        """Closes database connections"""
        if commit:
            self.conn.commit()
        self.conn.close()