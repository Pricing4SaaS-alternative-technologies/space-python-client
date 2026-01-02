from app.models.feature import Feature

def parse_feature_from_dict(data):
    return Feature(data["name"], data["value"])
