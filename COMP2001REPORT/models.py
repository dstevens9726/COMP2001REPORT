from __init__ import db
from __init__ import app


class Trails(db.Model):
    __tablename__ = 'TRAIL'
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True)
    TrailName = db.Column(db.String(255), nullable=False)
    TrailSummary = db.Column(db.String(500))
    TrailDescription = db.Column(db.String(100))
    Difficulty = db.Column(db.String(50))
    Location = db.Column(db.String(255))
    Length = db.Column(db.Float)
    ElevationGain = db.Column(db.Float)
    RouteType = db.Column(db.String(100))
    
    OwnerID = db.Column(db.Integer, db.ForeignKey('USERS.UserID'))
    
    Rating = db.Column(db.Float)
    Pt1_Lat = db.Column(db.Float)
    Pt1_Long = db.Column(db.Float)
    Pt1_Desc = db.Column(db.String(300))
    Pt2_Lat = db.Column(db.Float)
    Pt2_Long = db.Column(db.Float)
    Pt2_Desc = db.Column(db.String(300))
    Pt3_Lat = db.Column(db.Float)
    Pt3_Long = db.Column(db.Float)
    Pt3_Desc = db.Column(db.String(300))
    Pt4_Lat = db.Column(db.Float)
    Pt4_Long = db.Column(db.Float)
    Pt4_Desc = db.Column(db.String(300))
    Pt5_Lat = db.Column(db.Float)
    Pt5_Long = db.Column(db.Float)
    Pt5_Desc = db.Column(db.String(300))

class Feature(db.Model):
    __tablename__ = 'FEATURE'
    __table_args__ = {'schema': 'CW2'}
    TrailFeatureID = db.Column(db.Integer, primary_key=True)
    TrailFeature = db.Column(db.String(50), nullable=False)
class Users(db.Model):
    __tablename__ = 'USERS'
    __table_args__ = {'schema': 'CW2'}
    UserID = db.Column(db.Integer, primary_key=True)
    UserEmail = db.Column(db.String(100), nullable=False)
    UserName = db.Column(db.String(30), nullable=False)
    Password = db.Column(db.String(30), nullable=False)
    Role = db.Column(db.String(50), nullable=False)

class Trail_Feature(db.Model):
    __tablename__ = 'TRAIL_FEATURE'
    __table_args__ = {'schema': 'CW2'}
    
    TrailID = db.Column(db.Integer , db.ForeignKey('TRAIL.TrailID'), primary_key=True)
    
    TrailFeatureID = db.Column(db.Integer, db.ForeignKey('FEATURE.TrailFeatureID'), primary_key=True)



with app.app_context():
    print("tables recorded:")
    print(db.metadata.tables.keys())
