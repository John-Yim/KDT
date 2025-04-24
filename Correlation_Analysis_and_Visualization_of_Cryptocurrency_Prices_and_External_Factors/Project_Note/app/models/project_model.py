from app.db import get_db

def get_all_projects():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects ORDER BY project_id")
    return cursor.fetchall()

def get_project_by_id(project_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
    return cursor.fetchone()