from flask import Blueprint, request, jsonify
from services.gmaps import get_place_predictions, get_coordinates_from_place_id

maps_locator_bp = Blueprint('/maps_locator', __name__)

@maps_locator_bp.route('/search-location', methods=['GET'])
def search_location():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    predictions = get_place_predictions(query)
    results = []

    for p in predictions:
        description = p.get('description')
        place_id = p.get('place_id')

        lat, lng = get_coordinates_from_place_id(place_id)

        if lat is not None and lng is not None:
            results.append({
                'description': description,
                'latitude': lat,
                'longitude': lng
            })

    return jsonify({'results': results})
