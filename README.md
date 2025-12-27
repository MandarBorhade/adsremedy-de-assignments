# 📊 ADSRemedy Data Engineering Assignments

Welcome! This repository contains the **Data Engineering assignments** completed for **Ads Remedy Media LLP** as part of the test process

---

## 🚀 Project Overview

This project contains hands-on assignments designed to demonstrate fundamental skills in **Data Engineering**, including data processing, ingestion and transformation.

All assignments are structured and submitted in this repository for review and evaluation.
---

## 📁 Repository Structure
```
└───assignment_1
    ├───.ivy2
    │   ├───cache
    │   │   ├───org.checkerframework
    │   │   │   └───checker-qual
    │   │   │       └───jars
    │   │   └───org.postgresql
    │   │       └───postgresql
    │   │           └───jars
    │   └───jars
    └───scripts
        ├───data
        │   └───cleaned_output
        ├───database
        ├───logs
        └───python
```

## 🛠️ Setup & Getting Started

To run or work with this project locally:

### **Clone the Repository**
```bash
git clone https://github.com/MandarBorhade/adsremedy-de-assignments.git
cd adsremedy-de-assignments
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
git clone https://github.com/MandarBorhade/adsremedy-de-assignments.git
```
### **Create environment variables in .env file**
```
POSTGRES_USER= <username>
POSTGRES_PASSWORD= <password>
POSTGRES_DB= adsremedy
PGADMIN_DEFAULT_EMAIL= admin@admin.com
PGADMIN_DEFAULT_PASSWORD= admin
```
### Docker setup
Make sure you have docker desktop installed and running.
```
cd adsremedy-de-assignments/assignment_1
docker compose up --build
docker ps
```

### Check the logs to ensure Spark Master is ready to accept jobs
```
docker logs spark-master
```
### Run the below scripts
```
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/scripts/python/data-generator.py
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/scripts/python/data-cleaning.py
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.postgresql:postgresql:42.7.3 -c spark.jars.ivy=/opt/spark/work-dir/.ivy2 /opt/spark/work-dir/scripts/python/load-to-postgresdb.py
```
