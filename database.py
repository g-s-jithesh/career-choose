import sqlite3
import os

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    HAS_MYSQL_MODULE = True
except ImportError:
    HAS_MYSQL_MODULE = False

DB_NAME = "career_chooser"
DB_USER = "root"
DB_PASS = "123456" # Default MySQL root password
DB_HOST = "localhost"
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "career_chooser.db")

# Flag tracking active backend: 'mysql' or 'sqlite'
ACTIVE_BACKEND = "sqlite"

SAMPLE_CAREERS = [
    # Science Careers
    (
        "Software Engineer",
        "Design, develop, and maintain software applications, web systems, and mobile platforms.",
        "Science,All",
        "Coding & Technology,Building, Mechanics & Robotics",
        "Computer Science & IT,Engineering & Architecture",
        "Introvert,Both", "Logic", "Medium-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Data Scientist & AI Specialist",
        "Analyze complex datasets, build machine learning models, and derive actionable business intelligence.",
        "Science,Commerce",
        "Coding & Technology,Mathematics & Problem Solving",
        "Computer Science & IT,Business, Finance & Banking",
        "Introvert", "Logic", "Medium-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Doctor / Physician / Surgeon",
        "Diagnose illnesses, treat patients, perform surgeries, and advance healthcare.",
        "Science",
        "Science & Experiments,Helping People & Social Service",
        "Healthcare & Medicine",
        "Extrovert,Both", "Science", "Long-term", "Hands-on", "High Risk/High Reward", "Demanding"
    ),
    (
        "Mechanical / Mechatronics Engineer",
        "Design, build, and test mechanical systems, robotics, and industrial machinery.",
        "Science",
        "Building, Mechanics & Robotics,Mathematics & Problem Solving",
        "Engineering & Architecture",
        "Both", "Math", "Medium-term", "Hands-on", "Stable", "Standard"
    ),
    (
        "Biotechnologist / Geneticist",
        "Research biological systems, develop gene therapies, and innovate in pharmaceuticals and agriculture.",
        "Science",
        "Science & Experiments,Nature, Animals & Outdoors",
        "Healthcare & Medicine,Ecology & Wildlife Sciences",
        "Introvert,Both", "Science", "Long-term", "Hands-on", "Stable", "Standard"
    ),
    (
        "Aerospace Engineer",
        "Design and analyze aircraft, spacecraft, satellites, and propulsion technology.",
        "Science",
        "Science & Experiments,Mathematics & Problem Solving,Building, Mechanics & Robotics",
        "Engineering & Architecture,Computer Science & IT",
        "Both", "Math", "Medium-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Architect",
        "Plan and design aesthetic, functional buildings and modern urban spaces.",
        "Science,Arts",
        "Art, Drawing & Design,Building, Mechanics & Robotics,Mathematics & Problem Solving",
        "Engineering & Architecture,Design, Animation & Arts",
        "Both", "Art", "Medium-term", "Desk Job", "Medium Risk", "Standard"
    ),

    # Commerce Careers
    (
        "Chartered Accountant (CA)",
        "Audit financial statements, manage taxation, and provide strategic financial advisory.",
        "Commerce",
        "Mathematics & Problem Solving,Business, Stocks & Finance",
        "Business, Finance & Banking",
        "Introvert,Both", "Math", "Long-term", "Desk Job", "Stable", "Demanding"
    ),
    (
        "Investment Banker / Equity Analyst",
        "Advise companies on mergers, acquisitions, stock offerings, and high-stakes capital investments.",
        "Commerce",
        "Business, Stocks & Finance,Mathematics & Problem Solving",
        "Business, Finance & Banking",
        "Extrovert", "Math", "Medium-term", "Desk Job", "High Risk/High Reward", "Demanding"
    ),
    (
        "Corporate Financial Manager",
        "Oversee corporate budgets, capital allocations, and long-term financial health.",
        "Commerce",
        "Business, Stocks & Finance,Leadership & Event Organizing",
        "Business, Finance & Banking,Marketing & Entrepreneurship",
        "Both", "Math", "Medium-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Digital Marketing Strategist",
        "Plan digital advertising campaigns, optimize brand reach, and drive consumer growth.",
        "Commerce,Arts,All",
        "Writing, Reading & Media,Leadership & Event Organizing",
        "Marketing & Entrepreneurship,Design, Animation & Arts",
        "Extrovert", "Communication", "Short-term", "Desk Job", "Medium Risk", "Standard"
    ),

    # Arts & Humanities Careers
    (
        "Graphic & UI/UX Designer",
        "Create captivating visual identities, user interfaces, branding, and digital media.",
        "Arts,All",
        "Art, Drawing & Design,Coding & Technology",
        "Design, Animation & Arts,Computer Science & IT",
        "Both", "Art", "Short-term", "Desk Job", "Medium Risk", "Standard"
    ),
    (
        "Journalist & Media Producer",
        "Investigate news, produce investigative stories, write articles, and broadcast media content.",
        "Arts,All",
        "Writing, Reading & Media,Helping People & Social Service",
        "Law, Journalism & Public Policy,Design, Animation & Arts",
        "Extrovert", "Communication", "Medium-term", "Hands-on", "Medium Risk", "Demanding"
    ),
    (
        "Corporate Lawyer & Legal Counsel",
        "Advise clients on legal rights, handle litigation, draft contracts, and interpret laws.",
        "Arts,Commerce,All",
        "Writing, Reading & Media,Leadership & Event Organizing",
        "Law, Journalism & Public Policy",
        "Extrovert,Both", "Communication", "Long-term", "Desk Job", "Stable", "Demanding"
    ),
    (
        "Clinical Psychologist & Counselor",
        "Assess mental health, provide therapeutic counseling, and support psychological well-being.",
        "Arts,Science,All",
        "Helping People & Social Service,Science & Experiments",
        "Psychology & Social Sciences,Healthcare & Medicine",
        "Extrovert,Both", "Empathy", "Long-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Wildlife & Environmental Conservationist",
        "Protect natural habitats, conduct ecological field studies, and preserve wildlife species.",
        "Arts,Science,All",
        "Nature, Animals & Outdoors,Science & Experiments",
        "Ecology & Wildlife Sciences",
        "Both", "Nature", "Medium-term", "Hands-on", "Stable", "Demanding"
    ),
    (
        "Animator & 3D Game Artist",
        "Design 3D models, character animations, and visual effects for games and movies.",
        "Arts,Science,All",
        "Art, Drawing & Design,Coding & Technology",
        "Design, Animation & Arts,Computer Science & IT",
        "Introvert,Both", "Art", "Short-term", "Desk Job", "Medium Risk", "Standard"
    ),

    # Universal / All Stream Careers
    (
        "Startup Founder / Entrepreneur",
        "Build innovative businesses from scratch, manage teams, and scale disruptive products.",
        "All",
        "Leadership & Event Organizing,Business, Stocks & Finance",
        "Marketing & Entrepreneurship,Business, Finance & Banking",
        "Extrovert,Both", "Leadership", "Any", "Both", "High Risk/High Reward", "Demanding"
    ),
    (
        "Event Director & Operations Lead",
        "Plan, produce, and manage large-scale concerts, corporate summits, and cultural festivals.",
        "All",
        "Leadership & Event Organizing,Art, Drawing & Design",
        "Marketing & Entrepreneurship,Design, Animation & Arts",
        "Extrovert", "Organization", "Short-term", "Hands-on", "Medium Risk", "Demanding"
    ),
    (
        "Cybersecurity Analyst",
        "Defend critical infrastructure, protect against cyber attacks, and maintain data security.",
        "Science,All",
        "Coding & Technology,Mathematics & Problem Solving",
        "Computer Science & IT",
        "Introvert", "Logic", "Medium-term", "Desk Job", "Stable", "Standard"
    ),
    (
        "Civil Services / Public Administrator",
        "Implement public policies, manage administrative districts, and drive nation-building.",
        "All",
        "Leadership & Event Organizing,Helping People & Social Service",
        "Law, Journalism & Public Policy",
        "Extrovert,Both", "Leadership", "Long-term", "Both", "Stable", "Demanding"
    )
]

def get_mysql_connection(database=None):
    if not HAS_MYSQL_MODULE:
        return None
    try:
        if database:
            return mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=database,
                connect_timeout=2
            )
        else:
            return mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                connect_timeout=2
            )
    except Exception:
        return None

def get_sqlite_connection():
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error opening SQLite DB: {e}")
        return None

def init_db():
    global ACTIVE_BACKEND
    # First attempt MySQL
    conn_mysql = get_mysql_connection()
    if conn_mysql:
        try:
            cursor = conn_mysql.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            conn_mysql.close()

            conn_db = get_mysql_connection(database=DB_NAME)
            if conn_db:
                cursor = conn_db.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS careers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        allowed_streams VARCHAR(255),
                        hobby_interest VARCHAR(255),
                        career_interest VARCHAR(255),
                        work_environment VARCHAR(50),
                        primary_strength VARCHAR(50),
                        education_length VARCHAR(50),
                        hands_on VARCHAR(50),
                        risk_tolerance VARCHAR(50),
                        work_life_balance VARCHAR(50)
                    )
                """)
                # Check if hobby_interest column exists
                for col in ["hobby_interest", "career_interest"]:
                    try:
                        cursor.execute(f"ALTER TABLE careers ADD COLUMN {col} VARCHAR(255)")
                        conn_db.commit()
                    except Exception:
                        pass

                cursor.execute("SELECT COUNT(*) FROM careers")
                if cursor.fetchone()[0] == 0:
                    insert_sql = """
                        INSERT INTO careers (
                            title, description, allowed_streams, hobby_interest, career_interest,
                            work_environment, primary_strength, education_length, hands_on,
                            risk_tolerance, work_life_balance
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.executemany(insert_sql, SAMPLE_CAREERS)
                    conn_db.commit()
                conn_db.close()
                ACTIVE_BACKEND = "mysql"
                print("Connected and initialized MySQL database successfully.")
                return True
        except Exception as e:
            print(f"MySQL initialization notice: {e}. Falling back to local database.")

    # Graceful fallback to SQLite
    ACTIVE_BACKEND = "sqlite"
    conn_sq = get_sqlite_connection()
    if not conn_sq:
        print("Failed to initialize SQLite database.")
        return False
    
    cursor = conn_sq.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            allowed_streams TEXT,
            hobby_interest TEXT,
            career_interest TEXT,
            work_environment TEXT,
            primary_strength TEXT,
            education_length TEXT,
            hands_on TEXT,
            risk_tolerance TEXT,
            work_life_balance TEXT
        )
    """)
    # Check if empty or missing new columns
    cursor.execute("SELECT COUNT(*) FROM careers")
    row = cursor.fetchone()
    if row[0] == 0:
        insert_sql = """
            INSERT INTO careers (
                title, description, allowed_streams, hobby_interest, career_interest,
                work_environment, primary_strength, education_length, hands_on,
                risk_tolerance, work_life_balance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(insert_sql, SAMPLE_CAREERS)
        conn_sq.commit()
    conn_sq.close()
    print("Local database initialized successfully.")
    return True

def get_careers(stream_filter=None, filters=None):
    """
    Retrieve matching careers based on stream and user answers for:
    - hobby_interest
    - career_interest
    """
    if filters is None:
        filters = {}

    hobby_choice = filters.get("hobby_interest", "Select")
    career_choice = filters.get("career_interest", "Select")

    # If active backend is mysql, query mysql; otherwise sqlite
    if ACTIVE_BACKEND == "mysql":
        conn = get_mysql_connection(database=DB_NAME)
        if conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM careers WHERE 1=1"
            params = []

            if stream_filter:
                query += " AND (allowed_streams LIKE %s OR allowed_streams LIKE '%%All%%')"
                params.append(f"%{stream_filter}%")

            if hobby_choice and hobby_choice != "Select":
                query += " AND (hobby_interest LIKE %s OR title LIKE %s OR description LIKE %s)"
                term = f"%{hobby_choice.split(',')[0].strip()}%"
                params.extend([term, term, term])

            if career_choice and career_choice != "Select":
                query += " AND (career_interest LIKE %s OR title LIKE %s OR description LIKE %s)"
                term = f"%{career_choice.split(',')[0].strip()}%"
                params.extend([term, term, term])

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            conn.close()

            # If no exact match found with both strict filters, try relaxed matching
            if not results and (hobby_choice != "Select" or career_choice != "Select"):
                results = get_careers_relaxed_mysql(stream_filter, hobby_choice, career_choice)

            return results

    # SQLite query
    conn = get_sqlite_connection()
    if not conn:
        return []

    cursor = conn.cursor()
    query = "SELECT * FROM careers WHERE 1=1"
    params = []

    if stream_filter:
        query += " AND (allowed_streams LIKE ? OR allowed_streams LIKE '%All%')"
        params.append(f"%{stream_filter}%")

    if hobby_choice and hobby_choice != "Select":
        first_hobby = hobby_choice.split("&")[0].split(",")[0].strip()
        query += " AND (hobby_interest LIKE ? OR title LIKE ? OR description LIKE ?)"
        term = f"%{first_hobby}%"
        params.extend([term, term, term])

    if career_choice and career_choice != "Select":
        first_career = career_choice.split("&")[0].split(",")[0].strip()
        query += " AND (career_interest LIKE ? OR title LIKE ? OR description LIKE ?)"
        term = f"%{first_career}%"
        params.extend([term, term, term])

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()

    # Relaxed fallback if strictly filtered query returned 0 rows
    if not results and (hobby_choice != "Select" or career_choice != "Select"):
        results = get_careers_relaxed_sqlite(stream_filter, hobby_choice, career_choice)

    return results

def get_careers_relaxed_sqlite(stream_filter, hobby_choice, career_choice):
    """Fallback to match either hobby OR career interest for stream"""
    conn = get_sqlite_connection()
    if not conn:
        return []
    cursor = conn.cursor()

    query = "SELECT * FROM careers WHERE 1=1"
    params = []
    if stream_filter:
        query += " AND (allowed_streams LIKE ? OR allowed_streams LIKE '%All%')"
        params.append(f"%{stream_filter}%")

    clauses = []
    if hobby_choice and hobby_choice != "Select":
        first_h = hobby_choice.split("&")[0].split(",")[0].strip()
        clauses.append("(hobby_interest LIKE ? OR title LIKE ?)")
        params.extend([f"%{first_h}%", f"%{first_h}%"])

    if career_choice and career_choice != "Select":
        first_c = career_choice.split("&")[0].split(",")[0].strip()
        clauses.append("(career_interest LIKE ? OR title LIKE ?)")
        params.extend([f"%{first_c}%", f"%{first_c}%"])

    if clauses:
        query += " AND (" + " OR ".join(clauses) + ")"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()

    # If still empty, return general top stream careers
    if not results:
        conn = get_sqlite_connection()
        c = conn.cursor()
        if stream_filter:
            c.execute("SELECT * FROM careers WHERE allowed_streams LIKE ? OR allowed_streams LIKE '%All%'", (f"%{stream_filter}%",))
        else:
            c.execute("SELECT * FROM careers LIMIT 8")
        results = [dict(r) for r in c.fetchall()]
        conn.close()

    return results

def get_careers_relaxed_mysql(stream_filter, hobby_choice, career_choice):
    conn = get_mysql_connection(database=DB_NAME)
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM careers WHERE 1=1"
    params = []
    if stream_filter:
        query += " AND (allowed_streams LIKE %s OR allowed_streams LIKE '%%All%%')"
        params.append(f"%{stream_filter}%")

    clauses = []
    if hobby_choice and hobby_choice != "Select":
        first_h = hobby_choice.split("&")[0].split(",")[0].strip()
        clauses.append("(hobby_interest LIKE %s OR title LIKE %s)")
        params.extend([f"%{first_h}%", f"%{first_h}%"])

    if career_choice and career_choice != "Select":
        first_c = career_choice.split("&")[0].split(",")[0].strip()
        clauses.append("(career_interest LIKE %s OR title LIKE %s)")
        params.extend([f"%{first_c}%", f"%{first_c}%"])

    if clauses:
        query += " AND (" + " OR ".join(clauses) + ")"

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    if init_db():
        careers = get_careers()
        print(f"Total careers retrieved: {len(careers)}")
