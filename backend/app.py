from flask import Flask, jsonify, Response
from flask_cors import CORS
from database import get_connection
import json

app = Flask(__name__)
CORS(app)


def geojson_response(geojson_data):
    """
    Return GeoJSON response for QGIS.
    """
    return Response(
        json.dumps(geojson_data),
        mimetype="application/geo+json"
    )


@app.route("/")
def home():

    return jsonify({
        "message": "Milaor Parcel Spatial Analysis API is running.",
        "available_endpoints": [
            "/api/parcels",
            "/api/parcels.geojson",
            "/api/statistics",
            "/api/validation"
        ]
    })


@app.route("/api/parcels")
@app.route("/api/parcels.geojson")
def get_parcels():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                id,
                parcelid,
                barangayna,
                claimant,
                surveyplan,
                lotnumber,
                area,
                municipali,
                provincena,
                ST_AsGeoJSON(
                    ST_Transform(
                        ST_Force2D(geom),
                        4326
                    )
                ) AS geometry
            FROM parcels;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        features = []

        for row in rows:

            feature = {
                "type": "Feature",
                "properties": {
                    "id": row[0],
                    "parcelid": row[1],
                    "barangay": row[2],
                    "claimant": row[3],
                    "surveyplan": row[4],
                    "lotnumber": row[5],
                    "area": row[6],
                    "municipality": row[7],
                    "province": row[8]
                },
                "geometry": json.loads(row[9])
            }

            features.append(feature)

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return geojson_response(geojson)

    except Exception as error:

        return jsonify({
            "error": "Failed to load parcel data.",
            "details": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/api/statistics")
def get_statistics():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_parcels,
                SUM(area) AS total_area,
                AVG(area) AS average_area,
                COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS valid_parcels,
                COUNT(*) FILTER (WHERE NOT ST_IsValid(geom)) AS invalid_parcels
            FROM parcels;
        """

        cursor.execute(query)

        row = cursor.fetchone()

        return jsonify({
            "total_parcels": int(row[0]),
            "total_area_m2": round(float(row[1]), 2),
            "average_area_m2": round(float(row[2]), 2),
            "valid_parcels": int(row[3]),
            "invalid_parcels": int(row[4])
        })

    except Exception as error:

        return jsonify({
            "error": "Failed to generate statistics.",
            "details": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/api/validation")
def get_validation():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS total_parcels,
                COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS valid_parcels,
                COUNT(*) FILTER (WHERE NOT ST_IsValid(geom)) AS invalid_parcels
            FROM parcels;
        """

        cursor.execute(query)

        row = cursor.fetchone()

        total_parcels = int(row[0])
        valid_parcels = int(row[1])
        invalid_parcels = int(row[2])

        valid_percentage = round(
            (valid_parcels / total_parcels) * 100,
            2
        )

        invalid_percentage = round(
            (invalid_parcels / total_parcels) * 100,
            2
        )

        return jsonify({
            "total_parcels": total_parcels,
            "valid_parcels": valid_parcels,
            "invalid_parcels": invalid_parcels,
            "valid_percentage": valid_percentage,
            "invalid_percentage": invalid_percentage
        })

    except Exception as error:

        return jsonify({
            "error": "Failed to validate parcels.",
            "details": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)