from backend import database

def seed_data():
    db = database.SessionLocal()
    
    # Check if we already have data to avoid duplicates
    if db.query(database.Task).count() > 0:
        print("Database is already seeded!")
        return

    tasks = [
        # Weekday Tasks (DSA / Fast Backend)
        database.Task(day_type="weekday", category="DSA", description="Two Sum (Array Hash)", url="https://leetcode.com/problems/two-sum/"),
        database.Task(day_type="weekday", category="DSA", description="Valid Parentheses (Stack)", url="https://leetcode.com/problems/valid-parentheses/"),
        database.Task(day_type="weekday", category="FastAPI", description="Read: Pydantic Models", url="https://fastapi.tiangolo.com/tutorial/body/"),
        
        # Weekend Tasks (System Design / Big Picture)
        database.Task(day_type="weekend", category="System Design", description="Watch: How Discord Stores Billions of Messages", url="https://www.youtube.com/watch?v=112028"),
        database.Task(day_type="weekend", category="Project", description="Build the Docker Compose file for this bot", url="https://docs.docker.com/compose/")
    ]

    db.add_all(tasks)
    db.commit()
    db.close()
    print("✅ Successfully seeded 5 tasks into the database!")

if __name__ == "__main__":
    seed_data()