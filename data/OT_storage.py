import sqlite3
from data import OT_constants

class SQLiteStorage():
   
    def __init__(self, db_path: str = "olya.db"):
        self.db_path = db_path
        self._conn = None
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fsm_data (
                key TEXT PRIMARY KEY,
                state TEXT,
                data TEXT
            )
        """)
        
        #  universities
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS universities (
            university_id INTEGER PRIMARY KEY,
            university_name TEXT NOT NULL,
            university_fullname TEXT,
            university_location TEXT
        )
        """)

        #  courses
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            course_description TEXT,
            university_id INTEGER,
            FOREIGN KEY (university_id) REFERENCES universities(university_id)
        )
        """)
        
        #  courses_mess
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses_mess (
            mess_id INTEGER PRIMARY KEY,
            mess_desc TEXT NOT NULL,
            mess_lang TEXT,
            course_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback_mess (
            feed_id 	INTEGER PRIMARY KEY,
            feed_desc	TEXT NOT NULL,
            feed_lang	TEXT,
            feed_step	INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback_res (
	        feed_id	                INTEGER PRIMARY KEY,
	        feed_user_id	        INTEGER,
	        feed_user_name	        TEXT,
	        feed_clarity	        TEXT,
	        feed_clarity_comment	TEXT,
	        feed_usefulness	        TEXT,
	        feed_usefulness_comment	TEXT,
	        feed_support	        TEXT,
	        feed_support_comment	TEXT
	    )
        """)
        
        # insert datas only first time:
        # universities:
        if cursor.execute("""select university_id from universities""").fetchone() == None:
            # Prepare the data as a list of tuples
            data_to_insert = [( university_name, full_name) for university_name, full_name in OT_constants.UNIVERSITIES_DICT.items()]
            # Define the INSERT query
            insert_query = "INSERT INTO universities (university_name, university_fullname) VALUES (?, ?)"
            # Use executemany to insert the data
            cursor.executemany(insert_query, data_to_insert)
            
         # courses:
        if cursor.execute("""select course_id from courses""").fetchone() == None:
            # Insert data into the 'courses' table
            uid = 0
            for university_code, courses in OT_constants.COURSES_DICT.items():
                uid += 1
                for course_name in courses:
                    insert_query = "INSERT INTO courses (course_name, course_description, university_id) VALUES (?, ?, ?)"
                    course_ds_dict = OT_constants.COURSES_FULL_DICT.get(course_name)
                    cursor.execute(insert_query, (course_name, course_ds_dict, uid))        
                
        conn.commit()
        conn.close()

    def _get_connection(self) :
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
        return self._conn

    async def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    async def wait_closed(self) -> None:
        pass

    def _cleanup(self, chat, user):
#        chat, user = self.resolve_address(chat=chat, user=user)
#        if self.get_state(chat=chat, user=user) == None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fsm_data WHERE key = ?", (str(chat) + ":" + str(user),))
        conn.commit()