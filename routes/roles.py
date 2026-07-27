from flask import Blueprint, request, jsonify

from database import db
from models.role import Role


roles_bp = Blueprint(
    "roles",
    __name__,
    url_prefix="/roles"
)



# GET tous les rôles

@roles_bp.route("/", methods=["GET"])
def get_roles():

    roles = Role.query.all()


    return jsonify({

        "status": "success",

        "data":[
            role.to_dict()
            for role in roles
        ]

    }),200




# GET un rôle

@roles_bp.route(
    "/<int:id>",
    methods=["GET"]
)
def get_role(id):

    role = Role.query.get(id)


    if not role:

        return jsonify({

            "message":
            "Rôle introuvable"

        }),404



    return jsonify(
        role.to_dict()
    ),200




# POST créer rôle

@roles_bp.route(
    "/",
    methods=["POST"]
)
def create_role():

    data=request.json


    role = Role(

        nom_role=data["nom_role"],

        description=data.get(
            "description"
        )

    )


    db.session.add(role)

    db.session.commit()



    return jsonify({

        "message":
        "Rôle créé",

        "data":
        role.to_dict()

    }),201




# PUT modifier rôle

@roles_bp.route(
    "/<int:id>",
    methods=["PUT"]
)
def update_role(id):

    role=Role.query.get(id)


    if not role:

        return jsonify({

            "message":
            "Rôle introuvable"

        }),404



    data=request.json


    role.nom_role=data.get(
        "nom_role",
        role.nom_role
    )


    role.description=data.get(
        "description",
        role.description
    )


    db.session.commit()



    return jsonify({

        "message":
        "Rôle modifié",

        "data":
        role.to_dict()

    }),200





# DELETE rôle

@roles_bp.route(
    "/<int:id>",
    methods=["DELETE"]
)
def delete_role(id):

    role=Role.query.get(id)


    if not role:

        return jsonify({

            "message":
            "Rôle introuvable"

        }),404



    db.session.delete(role)

    db.session.commit()



    return jsonify({

        "message":
        "Rôle supprimé"

    }),200