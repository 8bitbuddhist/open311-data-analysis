import atexit
import psycopg2.extras

# Close database connection
@atexit.register
def close_db():
    db.close()
    conn.close()


conn = psycopg2.connect("dbname='open311' user='' password='' host='localhost'")
db = conn.cursor('open311-data-analysis', cursor_factory=psycopg2.extras.DictCursor)