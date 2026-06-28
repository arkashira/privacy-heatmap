# dataflow.md

## External Data Sources
External data sources for the privacy-heatmap platform include:

* WordPress site data (e.g. page views, clicks, etc.)
* User input data (e.g. configuration settings, etc.)

### ASCII Block Diagram
```
+---------------+
|  External     |
|  Data Sources  |
+---------------+
       |
       |  (via API)
       v
+---------------+
|  Ingestion    |
|  Layer        |
+---------------+
```

## Ingestion Layer
The ingestion layer is responsible for collecting data from external sources and preparing it for processing.

* Components:
	+ WordPress API client (e.g. `wp-api-client`)
	+ User input handler (e.g. `user-input-handler`)
* Auth Boundary: API keys or authentication tokens for WordPress sites and users

### ASCII Block Diagram
```
+---------------+
|  Ingestion    |
|  Layer        |
+---------------+
       |
       |  (via API)
       v
+---------------+
|  Processing  |
|  /Transform  |
|  Layer       |
+---------------+
```

## Processing/Transform Layer
The processing/transform layer is responsible for processing and transforming the ingested data into a format suitable for storage and querying.

* Components:
	+ Data processor (e.g. `data-processor`)
	+ Data transformer (e.g. `data-transformer`)
* Auth Boundary: None (data is processed in a secure environment)

### ASCII Block Diagram
```
+---------------+
|  Processing  |
|  /Transform  |
|  Layer       |
+---------------+
       |
       |  (via database)
       v
+---------------+
|  Storage     |
|  Tier        |
+---------------+
```

## Storage Tier
The storage tier is responsible for storing the processed data in a durable and accessible manner.

* Components:
	+ Database (e.g. `postgresql`)
	+ Data storage (e.g. `s3`)
* Auth Boundary: Database credentials and storage access keys

### ASCII Block Diagram
```
+---------------+
|  Storage     |
|  Tier        |
+---------------+
       |
       |  (via database)
       v
+---------------+
|  Query/Serve |
|  Layer       |
+---------------+
```

## Query/Serving Layer
The query/serving layer is responsible for serving data to users and responding to queries.

* Components:
	+ Query engine (e.g. `pgbouncer`)
	+ Serving layer (e.g. `flask`)
* Auth Boundary: API keys or authentication tokens for users

### ASCII Block Diagram
```
+---------------+
|  Query/Serve |
|  Layer       |
+---------------+
       |
       |  (via API)
       v
+---------------+
|  Egress to   |
|  User        |
+---------------+
```

## Egress to User
The egress to user layer is responsible for presenting data to users in a usable format.

* Components:
	+ User interface (e.g. `react`)
	+ Data visualizer (e.g. `d3`)
* Auth Boundary: None (data is served to authenticated users)

### ASCII Block Diagram
```
+---------------+
|  Egress to   |
|  User        |
+---------------+
```