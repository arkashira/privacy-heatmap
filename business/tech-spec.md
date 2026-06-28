# Tech Spec: v1
## Stack
- **Language**: TypeScript
- **Framework**: Next.js (for server-side rendering and static site generation)
- **Runtime**: Node.js (14.x) with Docker (20.x)
- **Database**: PostgreSQL (13.x) with TimescaleDB for time-series data
- **Storage**: Local file system for storing heatmaps, funnels, and session analytics data

## Hosting
- **Free-tier-first**: DigitalOcean (droplet) for development and testing
- **Specific platforms**: AWS (EC2, RDS) for production
- **Containerization**: Docker Compose for local development and production

## Data Model
- **Tables/Collections**:
  - `sites`: stores WordPress site metadata (id, name, url, etc.)
  - `heatmaps`: stores heatmap data (id, site_id, timestamp, etc.)
  - `funnels`: stores funnel data (id, site_id, timestamp, etc.)
  - `sessions`: stores session analytics data (id, site_id, timestamp, etc.)
- **Key fields**:
  - `id`: unique identifier for each record
  - `site_id`: foreign key referencing the `sites` table
  - `timestamp`: timestamp for each record

## API Surface
- **Endpoints**:
  - `GET /sites`: retrieve list of WordPress sites
  - `GET /sites/{site_id}`: retrieve WordPress site metadata
  - `POST /heatmaps`: create new heatmap data
  - `GET /heatmaps/{heatmap_id}`: retrieve heatmap data
  - `POST /funnels`: create new funnel data
  - `GET /funnels/{funnel_id}`: retrieve funnel data
  - `POST /sessions`: create new session analytics data
  - `GET /sessions/{session_id}`: retrieve session analytics data
  - `GET /analytics/{site_id}`: retrieve aggregated analytics data for a site
  - `GET /healthcheck`: retrieve healthcheck status

## Security Model
- **Auth**: JSON Web Tokens (JWT) for authentication and authorization
- **Secrets**: environment variables for storing sensitive data (e.g. database credentials)
- **IAM**: role-based access control (RBAC) for managing user permissions

## Observability
- **Logs**: use a logging library (e.g. Winston) to log events and errors
- **Metrics**: use a metrics library (e.g. Prometheus) to collect and expose metrics
- **Traces**: use a tracing library (e.g. OpenTelemetry) to collect and expose traces

## Build/CI
- **Build**: use a build tool (e.g. Webpack) to bundle and optimize code
- **CI**: use a CI tool (e.g. GitHub Actions) to automate testing and deployment
- **Testing**: use a testing framework (e.g. Jest) to write and run unit tests and integration tests