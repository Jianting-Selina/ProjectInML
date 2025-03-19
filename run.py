#from app.routes.patient_routes import patient_bp  # 导入patient_bp

from app import create_app

app = create_app()
#app.register_blueprint(patient_bp, url_prefix='/patients')

if __name__ == "__main__":
    app.run(debug=True)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")
# pip install flask-sqlalchemy
