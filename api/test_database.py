from database import engine


try:
    with engine.connect() as connection:
        print("SUCCESS: PostgreSQL connection is working!")

except Exception as e:
    print("ERROR: PostgreSQL connection failed")
    print(e)