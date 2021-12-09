from webapp import db, create_app

db.create_all(app=create_app())     #db создаст все модели для этого application-а