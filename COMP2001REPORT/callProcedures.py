
from flask import Flask, request, jsonify
from __init__ import db
from __init__ import app
from sqlalchemy import text
from verifyUser import token_required

# USERS CRUD Operations

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        query = text("EXEC [CW2].[ReadUsers] @UserID = :UserID")
        result = db.session.execute(query, {'UserID': user_id})
        users = [dict(row._mapping) for row in result.fetchall()]

        if not users:
            return ({"message": "User not found"}), 404

        return (users), 200
    except Exception as e:
        return ({"message": "Unable to fetch user", "error": str(e)}), 500


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        query = text("SELECT * FROM CW2.USERS")
        result = db.session.execute(query)
        users = [dict(row._mapping) for row in result.fetchall()]

        if not users:
            return jsonify({"message": "No users found"}), 404

        return (users), 200
    except Exception as e:
        return ({"message": "Unable to fetch users", "error": str(e)}), 500


@app.route('/users/create', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        required_fields = ['UserName', 'UserEmail', 'Password', 'Role']
        missing = [field for field in required_fields if field not in data]

        if missing:
            return ({"message": f"Missing fields: {', '.join(missing)}"}), 400

        query = text("""
            EXEC [CW2].[CreateUser] 
            @UserName = :UserName, @UserEmail = :UserEmail, @Password = :Password, @Role = :Role
        """)
        db.session.execute(query, data)
        db.session.commit()

        return ({"message": "User successfully created!"}), 201
    except Exception as e:
        return ({"message": "Unable to create user", "error": str(e)}), 500


@app.route('/users/update/<int:user_id>', methods=['PUT'])
@token_required
def edit_user(user_id):
    try:
        data = request.get_json()
        query = text("""
            EXEC [CW2].[UpdateUser] 
            @UserID = :UserID, @UserName = :UserName, @UserEmail = :UserEmail, @Password = :Password, @Role = :Role
        """)
        db.session.execute(query, {'UserID': user_id, **data})
        db.session.commit()

        return ({"message": "User updated successfully!"}), 200
    except Exception as e:
        return ({"message": "Unable to update user", "error": str(e)}), 500


@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@token_required
def remove_user(user_id):
    try:
        query = text("EXEC [CW2].[DeleteUser] @UserID = :UserID")
        db.session.execute(query, {'UserID': user_id})
        db.session.commit()

        return ({"message": "User deleted successfully!"}), 200
    except Exception as e:
        return ({"message": "Unable to delete user", "error": str(e)}), 500


# TRAILS CRUD Operations

@app.route('/trails/<int:trail_id>', methods=['GET'])
def get_trail_by_id(trail_id):
    try:
        query = text("EXEC [CW2].[ReadTrails] @TrailID = :TrailID")
        result = db.session.execute(query, {'TrailID': trail_id})
        trails = [dict(row._mapping) for row in result.fetchall()]

        if not trails:
            return ({"message": "Trail not found"}), 404

        return (trails), 200
    except Exception as e:
        return ({"message": "Unable to fetch trail", "error": str(e)}), 500


@app.route('/trails', methods=['GET'])
def get_all_trails():
    try:
        query = text("SELECT * FROM CW2.TRAIL")
        result = db.session.execute(query)
        trails = [dict(row._mapping) for row in result.fetchall()]

        if not trails:
            return ({"message": "No trails found"}), 404

        return (trails), 200
    except Exception as e:
        return ({"message": "Unable to fetch trails", "error": str(e)}), 500


@app.route('/trails/create', methods=['POST'])
@token_required
def add_trail():
    try:
        data = request.get_json()
        
        # Include all necessary fields, including the points
        required_fields = [
            'TrailName', 'TrailSummary', 'TrailDescription', 'Difficulty',
            'Location', 'Length', 'ElevationGain', 'RouteType', 'OwnerID',
            'Pt1_Lat', 'Pt1_Long', 'Pt1_Desc',  # Point 1 fields
            'Pt2_Lat', 'Pt2_Long', 'Pt2_Desc',  # Point 2 fields
            'Pt3_Lat', 'Pt3_Long', 'Pt3_Desc',  # Point 3 fields
            'Pt4_Lat', 'Pt4_Long', 'Pt4_Desc',  # Point 4 fields
            'Pt5_Lat', 'Pt5_Long', 'Pt5_Desc',  # Point 5 fields
        ]
        
        # Check if any required fields are missing in the request
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            return ({"message": f"Missing fields: {', '.join(missing)}"}), 400

        # Prepare the SQL query with all required parameters
        query = text("""
            EXEC [CW2].[CreateTrail] 
            @TrailName = :TrailName, 
            @TrailSummary = :TrailSummary, 
            @TrailDescription = :TrailDescription, 
            @Difficulty = :Difficulty, 
            @Location = :Location, 
            @Length = :Length, 
            @ElevationGain = :ElevationGain, 
            @RouteType = :RouteType, 
            @OwnerID = :OwnerID,
            @Pt1_Lat = :Pt1_Lat, @Pt1_Long = :Pt1_Long, @Pt1_Desc = :Pt1_Desc,
            @Pt2_Lat = :Pt2_Lat, @Pt2_Long = :Pt2_Long, @Pt2_Desc = :Pt2_Desc,
            @Pt3_Lat = :Pt3_Lat, @Pt3_Long = :Pt3_Long, @Pt3_Desc = :Pt3_Desc,
            @Pt4_Lat = :Pt4_Lat, @Pt4_Long = :Pt4_Long, @Pt4_Desc = :Pt4_Desc,
            @Pt5_Lat = :Pt5_Lat, @Pt5_Long = :Pt5_Long, @Pt5_Desc = :Pt5_Desc
        """)

        # Execute the query with all the data
        db.session.execute(query, data)
        db.session.commit()

        return {"message": "Trail created successfully!"}, 201
    except Exception as e:
        return {"message": f"Unable to create trail", "error": str(e)}, 500

        return ({"message": "Trail created successfully!"}), 201
    except Exception as e:
        return ({"message": "Unable to create trail", "error": str(e)}), 500


@app.route('/trails/update/<int:trail_id>', methods=['PUT'])
@token_required
def edit_trail(trail_id):
    try:
        data = request.get_json()

        # Required fields for the update
        required_fields = [
            'TrailName', 'TrailSummary', 'TrailDescription', 'Difficulty',
            'Location', 'Length', 'ElevationGain', 'RouteType', 'OwnerID',
            'Pt1_Lat', 'Pt1_Long', 'Pt1_Desc', 
            'Pt2_Lat', 'Pt2_Long', 'Pt2_Desc',
            'Pt3_Lat', 'Pt3_Long', 'Pt3_Desc',
            'Pt4_Lat', 'Pt4_Long', 'Pt4_Desc',
            'Pt5_Lat', 'Pt5_Long', 'Pt5_Desc'
        ]
        
       
        missing = [field for field in required_fields if field not in data]
        if missing:
            return {"message": f"Missing fields: {', '.join(missing)}"}, 400
        
        # Execute the stored procedure with the data
        query = text("""
            EXEC [CW2].[UpdateTrail] 
            @TrailID = :TrailID, @TrailName = :TrailName, 
            @TrailSummary = :TrailSummary, 
            @TrailDescription = :TrailDescription, @Difficulty = :Difficulty, 
            @Location = :Location, @Length = :Length, 
            @ElevationGain = :ElevationGain, @RouteType = :RouteType, 
            @OwnerID = :OwnerID,
            @Pt1_Lat = :Pt1_Lat, @Pt1_Long = :Pt1_Long, @Pt1_Desc = :Pt1_Desc,
            @Pt2_Lat = :Pt2_Lat, @Pt2_Long = :Pt2_Long, @Pt2_Desc = :Pt2_Desc,
            @Pt3_Lat = :Pt3_Lat, @Pt3_Long = :Pt3_Long, @Pt3_Desc = :Pt3_Desc,
            @Pt4_Lat = :Pt4_Lat, @Pt4_Long = :Pt4_Long, @Pt4_Desc = :Pt4_Desc,
            @Pt5_Lat = :Pt5_Lat, @Pt5_Long = :Pt5_Long, @Pt5_Desc = :Pt5_Desc
        """)
        db.session.execute(query, {'TrailID': trail_id, **data})
        db.session.commit()

        return {"message": "Trail updated successfully!"}, 200
    except Exception as e:
        db.session.rollback()  # Rollback transaction on error
        return {"message": "Unable to update trail", "error": str(e)}, 500



@app.route('/trails/delete/<int:trail_id>', methods=['DELETE'])
@token_required
def remove_trail(trail_id):
    try:
        query = text("EXEC [CW2].[DeleteTrail] @TrailID = :TrailID")
        db.session.execute(query, {'TrailID': trail_id})
        db.session.commit()

        return ({"message": "Trail deleted successfully!"}), 200
    except Exception as e:
        return ({"message": "Unable to delete trail", "error": str(e)}), 500

    # Start of Feature CRUD operations

@app.route('/features/<feature_id>', methods=['GET'])
def fetch_feature_by_id(feature_id):
    try:
        query = text("EXEC [CW2].[ReadFeature] @FeatureID = :FeatureID")
        result = db.session.execute(query, {'FeatureID': feature_id})
        features = [dict(row._mapping) for row in result.fetchall()]
        
        if not features:
            return ({"message": "Feature not found"}), 404
        
        return (features), 200
    except Exception as e:
        return ({"message": "Can't fetch feature", "error": str(e)}), 500


@app.route('/features', methods=['GET'])
def fetch_all_features():
    try:
        query = text("SELECT * FROM CW2.FEATURE")
        result = db.session.execute(query)
        features = [dict(row._mapping) for row in result.fetchall()]
        
        if not features:
            return ({"message": "No features found"}), 404
        
        return (features), 200
    except Exception as e:
        return ({"message": "Can't fetch features", "error": str(e)}), 500


@app.route('/features/create', methods=['POST'])
@token_required
def create_feature():
    try:
        data = request.get_json()
        
        if 'TrailFeature' not in data:
            return ({"message": "TrailFeature field is required"}), 400

        query = text("""
            EXEC [CW2].[CreateFeature] 
            @TrailFeature = :TrailFeature
        """)
        db.session.execute(query, {'TrailFeature': data['TrailFeature']})
        db.session.commit()
        
        return ({"message": "Feature created successfully!"}), 201
    except Exception as e:
        return ({"message": "Can't create feature", "error": str(e)}), 500


@app.route('/features/update/<feature_id>', methods=['PUT'])
@token_required
def update_feature(feature_id):
    try:
        data = request.get_json()

        if 'TrailFeature' not in data:
            return ({"message": "TrailFeature field is required"}), 400

        query = text("""
            EXEC [CW2].[UpdateFeature] 
            @FeatureID = :FeatureID, 
            @TrailFeature = :TrailFeature
        """)
        db.session.execute(query, {'FeatureID': feature_id, 'TrailFeature': data['TrailFeature']})
        db.session.commit()
        
        return ({"message": "Feature updated successfully!"}), 200
    except Exception as e:
        return ({"message": "Can't update feature", "error": str(e)}), 500


@app.route('/features/delete/<feature_id>', methods=['DELETE'])
@token_required
def delete_feature(feature_id):
    try:
        query = text("EXEC [CW2].[DeleteFeature] @FeatureID = :FeatureID")
        db.session.execute(query, {'FeatureID': feature_id})
        db.session.commit()
        
        return ({"message": "Feature deleted successfully!"}), 200
    except Exception as e:
        return ({"message": "Can't delete feature", "error": str(e)}), 500

    # Start of Trail Features CRUD operations

@app.route('/trail_features', methods=['GET'])
def fetch_all_trail_features():
    try:
        query = text("SELECT * FROM CW2.TrailFeature")
        result = db.session.execute(query)
        trail_features = [dict(row._mapping) for row in result.fetchall()]
        
        if not trail_features:
            return ({"message": "No trail features found"}), 404
        
        return (trail_features), 200
    except Exception as e:
        return ({"message": "Can't fetch trail features", "error": str(e)}), 500


@app.route('/trail_features/<trail_feature_id>', methods=['GET'])
def fetch_trail_feature_by_id(trail_feature_id):
    try:
        query = text("EXEC [CW2].[ReadTrailFeature] @FeatureID = :FeatureID")
        result = db.session.execute(query, {'FeatureID': trail_feature_id})
        trail_features = [dict(row._mapping) for row in result.fetchall()]
        
        if not trail_features:
            return ({"message": "Trail feature not found"}), 404
        
        return (trail_features), 200
    except Exception as e:
        return ({"message": "Can't fetch trail feature", "error": str(e)}), 500


@app.route('/trail_features/create', methods=['POST'])
@token_required
def create_trail_feature():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['TrailID', 'FeatureID']):
            return ({"message": "TrailID and FeatureID are required"}), 400

        query = text("""
            EXEC [CW2].[CreateTrailFeature] 
            @TrailID = :TrailID, 
            @FeatureID = :FeatureID
        """)
        db.session.execute(query, {'TrailID': data['TrailID'], 'FeatureID': data['FeatureID']})
        db.session.commit()
        
        return ({"message": "Trail feature created successfully!"}), 201
    except Exception as e:
        return ({"message": "Can't create trail feature", "error": str(e)}), 500



print("Routes registered in callProcedures.py:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)
    