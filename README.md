# GME 205 FINAL PROJECT: Development of a PostGIS-Based Cadastral Parcel Analysis and Web GIS System for Milaor, Camarines Sur
## Description
- This project extends the methodologies presented in Laboratory 7: PostGIS to REST API to GIS Clients by developing a comprehensive cadastral parcel analysis and Web GIS system. The project demonstrates the integration of PostgreSQL/PostGIS, Flask REST API, and web-based GIS technologies through a complete spatial data workflow.

- Cadastral parcel boundary data from the Municipality of Milaor, Camarines Sur were stored in a PostGIS spatial database and exposed through a Flask-based REST API. The system provides GeoJSON services for GIS visualization, parcel statistics, geometry validation reports, parcel search functionality, overlap detection, and interactive web mapping.

- The project highlights the application of spatial databases, geospatial web services, spatial analysis, and geospatial data interoperability in supporting cadastral parcel management and spatial decision-making.
---
## Objectives
### General Objective
- To develop a PostGIS-based cadastral parcel analysis and Web GIS system for the Municipality of Milaor, Camarines Sur using PostgreSQL, Flask REST API, and GIS technologies.
---
### Specific Objectives
- Store cadastral parcel boundary data in a PostgreSQL/PostGIS spatial database.
- Develop REST API endpoints for parcel retrieval and GeoJSON services.
- Generate parcel statistics and geometry validation reports.
- Detect overlapping cadastral parcels using PostGIS spatial functions.
- Implement parcel search functionality through API-based queries.
- Develop dashboard and reporting endpoints for spatial data summaries.
- Create an interactive Web GIS interface for parcel visualization and attribute retrieval.
- Demonstrate interoperability between spatial databases, web services, GIS software, and web mapping applications.
---
## Study Area
**Municipality of Milaor, Camarines Sur, Philippines**
- The dataset consists of cadastral parcel boundaries extracted from the Milaor parcel database and imported into PostGIS for spatial analysis and web service deployment.
---
## Technologies Used
### Database
- PostgreSQL 18
- PostGIS Extension
### Backend
- Python 3.14
- Flask
- Flask-CORS
- psycopg2-binary
- python-dotenv
### Web GIS
- Leaflet.js
- GeoJSON
- OpenStreetMap
### GIS Software
- QGIS
### Development Environment
- Visual Studio Code
---
## Project Development Process

The development of this project followed a four-phase workflow based on the concepts introduced in **Laboratory 7: PostGIS to REST API to GIS Clients**. The workflow consisted of database development, REST API development, spatial analysis implementation, and visualization.

### Phase 1: Database Development

A PostgreSQL database was created and configured with the PostGIS extension to support spatial data storage and analysis.

The cadastral parcel dataset for the Municipality of Milaor, Camarines Sur was imported into the PostGIS database through pgAdmin. Parcel geometries and attribute information were stored in a spatial table named **parcels**.

To improve query performance, a GiST spatial index was created on the geometry column.

**Activities Performed**

* Import Milaor cadastral parcels into PostGIS
* Store parcel geometries and attributes
* Create spatial indexes for efficient querying
---
### Phase 2: REST API Development

A Flask-based REST API was developed using Python to provide access to the parcel database.

The API established communication between the PostGIS database and GIS clients by exposing parcel information and analysis results through REST endpoints.

**Implemented Endpoints**

```text
/api/parcels
/api/parcels.geojson
/api/statistics
/api/validation
/api/overlaps
/api/search/<parcelid>
/api/dashboard
/api/report
```

**Activities Performed**

* Database connection configuration
* REST endpoint development
* JSON and GeoJSON response generation
* API request handling
---
### Phase 3: Spatial Analysis

PostGIS spatial functions were used to analyze cadastral parcel data and generate analytical outputs.

**Implemented Analyses**

* Geometry validation using `ST_IsValid()`
* Overlap detection using `ST_Intersects()`
* Overlap area calculation using `ST_Intersection()` and `ST_Area()`
* Parcel statistics generation using SQL aggregate functions
* Parcel search through SQL queries

**Activities Performed**

* Geometry validation
* Parcel statistics generation
* Overlap detection
* Parcel querying and retrieval
* Dashboard generation
* Report generation
---
### Phase 4: Visualization

The analytical outputs were visualized through both desktop GIS and web-based GIS platforms.

The GeoJSON service was connected to QGIS to verify successful parcel visualization and GIS interoperability.

A Web GIS interface was developed using HTML, JavaScript, Leaflet.js, and OpenStreetMap. The application retrieves parcel data from the GeoJSON endpoint and displays parcel boundaries on an interactive map with parcel information popups.

**Visualization Features**

* QGIS integration
* Web GIS implementation using Leaflet
* Interactive parcel visualization
* Parcel attribute popups
* Dynamic GeoJSON loading
---
### Testing and Validation

The completed system was tested through:

* Database connectivity testing
* API endpoint testing
* Geometry validation testing
* Overlap detection verification
* QGIS integration testing
* Web GIS functionality testing

### Results confirmed successful integration of PostgreSQL/PostGIS, Flask REST APIs, QGIS, and Web GIS technologies within a single cadastral parcel analysis and visualization system.
---
## Presentation Notes

When asked which code is executed when a user clicks a parcel in the Web GIS, the `fetch('/api/parcels.geojson')` function was initially identified because it retrieves parcel data from the Flask API. However, it was clarified that the `fetch()` function only executes when the Web GIS loads and is responsible for retrieving the GeoJSON dataset. The actual code executed during parcel selection is the `layer.on('click', function(){...})` event handler, which responds to user interaction by highlighting the selected parcel and modifying its display properties. This distinction highlights the difference between data retrieval and event handling in Web GIS applications, where `fetch()` loads spatial data while click events manage user interaction with map features.

---
### Author
- Audrey Marie Justine A. Reyes
- MS Geomatics Engineering (GeoInf)
