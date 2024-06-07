from app import create_app

db_var = 'sqlite:///newdatabase.db'

flask_app = create_app(db_var)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=True)
