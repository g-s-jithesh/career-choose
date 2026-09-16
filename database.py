import mysql.connector
from mysql.connector import Error

DB_NAME = "career_chooser"
DB_USER = "root"
DB_PASS = "123456" # Change this if your MySQL root user has a password
DB_HOST = "localhost"

def create_connection(database=None):
    try:
        if database:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=database
            )
        else:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS
            )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to MySQL server. Please ensure XAMPP/WAMP or your MySQL service is running.")
        return False
    
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

    conn = create_connection(database=DB_NAME)
    cursor = conn.cursor()
    
    # Create careers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            allowed_streams VARCHAR(255),
            work_environment VARCHAR(50),
            primary_strength VARCHAR(50),
            education_length VARCHAR(50),
            hands_on VARCHAR(50),
            risk_tolerance VARCHAR(50),
            work_life_balance VARCHAR(50)
        )
    """)
    
    # Insert some sample data if table is empty
    cursor.execute("SELECT COUNT(*) FROM careers")
    if cursor.fetchone()[0] == 0:
        sample_careers = [
            ("Software Engineer", "Design and build software applications.", "All,Science", "Introvert,Both", "Logic", "Medium-term", "Desk Job", "Stable", "Standard"),
            ("Graphic Designer", "Create visual concepts using software or by hand.", "All,Arts", "Both", "Art", "Short-term", "Desk Job", "Medium Risk", "Standard"),
            ("Mechanical Engineer", "Design, develop, build, and test mechanical devices.", "Science", "Both", "Math", "Medium-term", "Hands-on", "Stable", "Standard"),
            ("Surgeon", "Medical practitioner qualified to practice surgery.", "Science", "Extrovert,Both", "Science", "Long-term", "Hands-on", "High Risk/High Reward", "Demanding"),
            ("Wildlife Conservationist", "Protect ecosystems and wildlife.", "Science,Arts,All", "Both", "Nature", "Medium-term", "Hands-on", "Stable", "Demanding"),
            ("Chartered Accountant", "Manage financial accounts and provide financial advice.", "Commerce", "Introvert,Both", "Math", "Long-term", "Desk Job", "Stable", "Demanding"),
            ("Marketing Manager", "Develop and execute marketing strategies.", "Commerce,Arts,All", "Extrovert", "Communication", "Medium-term", "Desk Job", "Medium Risk", "Standard"),
            ("Data Scientist", "Analyze and interpret complex data to help make decisions.", "Science,Commerce", "Introvert", "Logic", "Medium-term", "Desk Job", "Stable", "Standard"),
            ("Entrepreneur", "Start and run a business venture.", "All", "Extrovert,Both", "Leadership", "Any", "Both", "High Risk/High Reward", "Demanding"),
            ("Psychologist", "Study the human mind and behavior.", "Arts,Science,All", "Extrovert,Both", "Empathy", "Long-term", "Desk Job", "Stable", "Standard"),
            ("Investment Banker", "Help companies and governments raise capital.", "Commerce", "Extrovert", "Math", "Medium-term", "Desk Job", "High Risk/High Reward", "Demanding"),
            ("Event Planner", "Coordinate and manage events like weddings and conferences.", "All", "Extrovert", "Organization", "Short-term", "Hands-on", "Medium Risk", "Demanding")
        ]
        
        insert_query = """
            INSERT INTO careers (title, description, allowed_streams, work_environment, primary_strength, education_length, hands_on, risk_tolerance, work_life_balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, sample_careers)
        conn.commit()
    
    conn.close()
    return True

def get_careers(stream_filter=None, filters=None):
    conn = create_connection(database=DB_NAME)
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM careers WHERE 1=1"
    params = []
    
    if stream_filter:
        query += " AND (allowed_streams LIKE %s OR allowed_streams LIKE '%%All%%')"
        params.append(f"%{stream_filter}%")
        
    if filters:
        if 'work_environment' in filters and filters['work_environment'] != "Don't Care":
            query += " AND (work_environment LIKE %s OR work_environment LIKE '%%Both%%')"
            params.append(f"%{filters['work_environment']}%")
        if 'primary_strength' in filters and filters['primary_strength'] != "Don't Care":
            query += " AND primary_strength = %s"
            params.append(filters['primary_strength'])
        if 'education_length' in filters and filters['education_length'] != "Don't Care":
            query += " AND education_length = %s"
            params.append(filters['education_length'])
        if 'hands_on' in filters and filters['hands_on'] != "Don't Care":
            query += " AND hands_on = %s"
            params.append(filters['hands_on'])

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    
    return results

if __name__ == "__main__":
    if init_db():
        print("Database initialized successfully.")
        careers = get_careers()
        print(f"Total careers in DB: {len(careers)}")
