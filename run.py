#from app.routes.patient_routes import patient_bp  # 导入patient_bp

from app import create_app

app = create_app()
#app.register_blueprint(patient_bp, url_prefix='/patients')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule} - {rule.endpoint}")
# pip install flask-sqlalchemy
