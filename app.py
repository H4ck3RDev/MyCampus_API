from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from database import db
from flask_jwt_extended import JWTManager

from routes.roles import roles_bp
from routes.utilisateurs import utilisateurs_bp
from routes.auth import auth_bp
from routes.annees_academiques import annees_academiques_bp
from routes.facultes import facultes_bp
from routes.departements import departements_bp
from routes.promotions import promotions_bp
from routes.etudiants import etudiants_bp
from routes.professeurs import professeurs_bp
from routes.cours import cours_bp
from routes.affectations_professeurs import affectations_professeurs_bp
from routes.inscriptions import inscriptions_bp
from routes.notes import notes_bp
from routes.messages import messages_bp
from routes.notifications import notifications_bp
from routes.presences import presences_bp
from routes.documents import documents_bp

from models import Role, Utilisateur

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

db.init_app(app)

app.register_blueprint(roles_bp)
app.register_blueprint(utilisateurs_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(annees_academiques_bp)
app.register_blueprint(facultes_bp)
app.register_blueprint(departements_bp)
app.register_blueprint(promotions_bp)
app.register_blueprint(etudiants_bp)
app.register_blueprint(professeurs_bp)
app.register_blueprint(cours_bp)
app.register_blueprint(affectations_professeurs_bp)
app.register_blueprint(inscriptions_bp)
app.register_blueprint(notes_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(presences_bp)
app.register_blueprint(documents_bp)

jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Bienvenue sur l'API MyCampus",
        "version": "1.0.0",
        "status": "OK"
    })


@app.route("/test-db", methods=["GET"])
def test_db():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return jsonify({
            "status": "success",
            "message": "Connexion à MySQL réussie."
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)