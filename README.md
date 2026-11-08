# Brazilian Elections 2026 — Data Engineering Project

Data Engineering project built with **Databricks**, **PySpark**, **SQL**, and **Delta Lake**, using Brazilian electoral data from the Superior Electoral Court (TSE).

The project implements a Medallion Architecture (Bronze, Silver, and Gold), processes electoral datasets, applies dimensional modeling, and provides interactive dashboards for data analysis.

## Project Overview

The main goal is to build a structured data pipeline to ingest, transform, organize, and analyze Brazilian electoral data from 2026.

The project follows the Medallion Architecture, separating data processing into three layers:

### Bronze Layer
- Raw CSV files obtained from the TSE.
- Original data stored in Databricks Volumes.
- Data preserved in its original format.

### Silver Layer
- Data processing and transformation using PySpark.
- Standardization of columns and data types.
- Preparation of datasets for analytical modeling.

### Gold Layer
- Dimensional modeling using SQL.
- Creation of fact and dimension tables.
- Data organized for analytical queries and dashboards.

## Architecture

```text
TSE — Electoral Data (CSV)
          |
          v
     BRONZE LAYER
   Raw CSV Files
          |
          v
     SILVER LAYER
 PySpark Transformations
          |
          v
      GOLD LAYER
 Dimensional Modeling
 (Fact and Dimension Tables)
          |
          v
     DASHBOARDS
 Electoral Data Analysis
```

## Data Model

The Gold layer uses a dimensional model composed of fact and dimension tables.

### Fact Tables
- `fact_votacao`
- `fact_eleitorado`

### Dimension Tables
- `dim_eleicao`
- `dim_candidaturas`
- `dim_cargo`
- `dim_localidades`

## Dashboard

Interactive dashboards were developed to explore electoral data and provide analytical insights.

<!-- Add dashboard screenshots here -->

## Technologies Used

- Databricks
- Apache Spark
- PySpark
- SQL
- Delta Lake
- Python
- Databricks Jobs

## Repository Structure

```text
projeto-eleicoes-2026-databricks/
│
├── setup/
│   └── setup_environment.sql
│
├── notebooks/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── dashboard/
│
├── docs/
│
├── images/
│
└── README.md
```

## Data Source

Electoral datasets provided by the Brazilian Superior Electoral Court:

https://dadosabertos.tse.jus.br/

## Project Status

The data pipeline, Medallion Architecture, dimensional model, and dashboards have been developed as part of this project.

---

**Developed as a Data Engineering portfolio project.**
