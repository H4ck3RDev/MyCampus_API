from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.document import Document
from models.utilisateur import Utilisateur


documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/documents"
)


@documents_bp.route("/", methods=["GET"])
@jwt_required()
def get_documents():
    try:
        documents = Document.query.all()

        return jsonify({
            "status": "success",
            "data": [document.to_dict() for document in documents]
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@documents_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_document(id):
    try:
        document = Document.query.get(id)

        if not document:
            return jsonify({
                "status": "error",
                "message": "Document introuvable."
            }), 404

        return jsonify({
            "status": "success",
            "data": document.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@documents_bp.route("/", methods=["POST"])
@jwt_required()
def create_document():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        nom = data.get("nom")
        chemin = data.get("chemin")
        id_utilisateur = data.get("id_utilisateur")

        if not nom or not chemin:
            return jsonify({
                "status": "error",
                "message": "Les champs nom et chemin sont requis."
            }), 400

        utilisateur = None
        if id_utilisateur is not None:
            utilisateur = Utilisateur.query.get(id_utilisateur)
            if not utilisateur:
                return jsonify({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }), 404

        document = Document(
            nom=nom,
            chemin=chemin,
            type_document=data.get("type_document"),
            id_utilisateur=id_utilisateur
        )

        db.session.add(document)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Document créé.",
            "data": document.to_dict()
        }), 201
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@documents_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_document(id):
    try:
        document = Document.query.get(id)

        if not document:
            return jsonify({
                "status": "error",
                "message": "Document introuvable."
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Aucune donnée reçue."
            }), 400

        if data.get("id_utilisateur") is not None:
            utilisateur = Utilisateur.query.get(data["id_utilisateur"])
            if not utilisateur:
                return jsonify({
                    "status": "error",
                    "message": "Utilisateur introuvable."
                }), 404
            document.id_utilisateur = data["id_utilisateur"]

        document.nom = data.get("nom", document.nom)
        document.chemin = data.get("chemin", document.chemin)
        document.type_document = data.get("type_document", document.type_document)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Document modifié.",
            "data": document.to_dict()
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500


@documents_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_document(id):
    try:
        document = Document.query.get(id)

        if not document:
            return jsonify({
                "status": "error",
                "message": "Document introuvable."
            }), 404

        db.session.delete(document)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Document supprimé avec succès."
        }), 200
    except Exception as e:
        import traceback
        return jsonify({"status": "error", "message": str(e), "traceback": traceback.format_exc()}), 500
