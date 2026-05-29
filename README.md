# GME 205 FINAL PROJECT: Spatial Analysis and Boundary Integrity Assessment of Cadastral Parcels Using PostGIS and REST API in Milaor, Camarines Sur

---
## Description
This project is an application and extension of the methodologies presented in Laboratory 7: PostGIS to REST API to GIS Clients. It demonstrates the integration of PostgreSQL/PostGIS, Flask REST API, and GIS clients through a spatial data workflow for parcel boundary assessment. Parcel boundary data from the Municipality of Milaor, Camarines Sur were stored in a PostGIS database and exposed through a Flask-based REST API as GeoJSON services. Additional analytical endpoints were developed to generate parcel statistics and geometry validation reports. The project highlights geospatial data interoperability and the role of web-based spatial services in supporting parcel data management and assessment.
---
## Objectives
- Store parcel boundary data in a PostGIS-enabled PostgreSQL database.
- Develop a Flask REST API to access spatial data.
- Convert PostGIS geometries into GeoJSON format.
- Serve parcel data to GIS clients through HTTP endpoints.
- Generate parcel statistics from the spatial database.
- Perform geometry validation using PostGIS functions.
- Demonstrate interoperability between PostGIS, Flask, and GIS applications.
---
## Study Area
**Municipality of Milaor, Camarines Sur, Philippines**
The dataset consists of cadastral parcel boundaries extracted from the Milaor parcel database and imported into PostGIS for spatial analysis and web service deployment.
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
### GIS Software
- QGIS
### Development Environment
- Visual Studio Code
---
### Author
- Audrey Marie Justine A. Reyes
- MS Geomatics Engineering (GeoInf)
