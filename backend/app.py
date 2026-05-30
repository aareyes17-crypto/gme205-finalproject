from flask import Flask, jsonify, Response
from flask_cors import CORS
from database import get_connection
from flask import render_template
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
            "/api/validation",
            "/api/overlaps",
            "/api/search/<parcelid>",
            "/api/dashboard",
            "/api/report"
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


@app.route("/api/overlaps")
def get_overlaps():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                COUNT(*) AS overlap_pairs,
                MAX(
                    ST_Area(
                        ST_Intersection(a.geom, b.geom)
                    )
                ) AS largest_overlap
            FROM parcels a
            JOIN parcels b
            ON a.id < b.id
            AND ST_Intersects(a.geom, b.geom)
            AND ST_Area(
                ST_Intersection(a.geom, b.geom)
            ) > 0;
        """

        cursor.execute(query)

        row = cursor.fetchone()

        overlap_pairs = int(row[0]) if row[0] else 0
        largest_overlap = round(float(row[1]), 2) if row[1] else 0

        return jsonify({
            "overlap_pairs": overlap_pairs,
            "largest_overlap_m2": largest_overlap,
            "status": (
                "Spatial conflicts detected"
                if overlap_pairs > 0
                else "No overlaps detected"
            )
        })

    except Exception as error:

        return jsonify({
            "error": "Failed to analyze overlaps.",
            "details": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/api/search/<int:parcelid>")
def search_parcel(parcelid):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT
                parcelid,
                claimant,
                barangayna,
                municipali,
                provincena,
                area
            FROM parcels
            WHERE parcelid = %s;
        """

        cursor.execute(query, (parcelid,))

        row = cursor.fetchone()

        if row is None:

            return jsonify({
                "message": "Parcel not found"
            }), 404

        return jsonify({
            "parcelid": row[0],
            "claimant": row[1],
            "barangay": row[2],
            "municipality": row[3],
            "province": row[4],
            "area_m2": round(float(row[5]), 2)
        })

    except Exception as error:

        return jsonify({
            "error": "Failed to search parcel.",
            "details": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route('/api/dashboard')
def dashboard():

    conn = get_connection()
    cur = conn.cursor()

    # Total parcels
    cur.execute("""
        SELECT COUNT(*)
        FROM parcels;
    """)
    total_parcels = cur.fetchone()[0]

    # Geometry validation
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS valid_parcels,
            COUNT(*) AS total
        FROM parcels;
    """)
    valid_parcels, total = cur.fetchone()

    # Overlap pairs
    cur.execute("""
        SELECT COUNT(*)
        FROM parcels a
        JOIN parcels b
        ON a.id < b.id
        AND ST_Intersects(a.geom, b.geom)
        AND ST_Area(ST_Intersection(a.geom, b.geom)) > 0;
    """)
    overlap_pairs = cur.fetchone()[0]

    # Largest overlap
    cur.execute("""
        SELECT MAX(
            ST_Area(
                ST_Intersection(a.geom, b.geom)
            )
        )
        FROM parcels a
        JOIN parcels b
        ON a.id < b.id
        AND ST_Intersects(a.geom, b.geom)
        AND ST_Area(ST_Intersection(a.geom, b.geom)) > 0;
    """)
    largest_overlap = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "total_parcels": total_parcels,
        "valid_geometries": valid_parcels,
        "validity_rate_percent":
            round((valid_parcels / total) * 100, 2),
        "overlap_pairs": overlap_pairs,
        "largest_overlap_m2":
            round(float(largest_overlap), 2)
            if largest_overlap else 0
    })


@app.route('/api/report')
def report():

    conn = get_connection()
    cur = conn.cursor()

    # Total parcels
    cur.execute("""
        SELECT COUNT(*)
        FROM parcels;
    """)
    total_parcels = cur.fetchone()[0]

    # Validation
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE ST_IsValid(geom)) AS valid_parcels,
            COUNT(*) AS total
        FROM parcels;
    """)
    valid_parcels, total = cur.fetchone()

    # Overlaps
    cur.execute("""
        SELECT COUNT(*)
        FROM parcels a
        JOIN parcels b
        ON a.id < b.id
        AND ST_Intersects(a.geom, b.geom)
        AND ST_Area(ST_Intersection(a.geom, b.geom)) > 0;
    """)
    overlap_pairs = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({
        "report_title": "Milaor Parcel Boundary Integrity Report",
        "total_parcels": total_parcels,
        "valid_geometries": valid_parcels,
        "invalid_geometries": total_parcels - valid_parcels,
        "overlap_pairs": overlap_pairs,
        "assessment": (
            "Parcel geometries are valid but spatial overlaps exist."
            if overlap_pairs > 0
            else "No spatial conflicts detected."
        )
    })


@app.route('/map')
def map_view():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(debug=True)