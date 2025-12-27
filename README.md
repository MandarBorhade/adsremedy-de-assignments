# 📊 ADSRemedy Data Engineering Assignments

Welcome! This repository contains the **Data Engineering assignments** completed for **Ads Remedy Media LLP** as part of the interview/test process. :contentReference[oaicite:0]{index=0}

---

## 🚀 Project Overview

This project contains hands-on assignments designed to demonstrate fundamental skills in **Data Engineering**, including data processing, ingestion and transformation.

All assignments are structured and submitted in this repository for review and evaluation.

---

## 📁 Repository Structure

adsremedy-de-assignments/
├── assignment_1/ # Code and scripts for Assignment #1
├── .gitignore # Files to be ignored by Git
├── Data Engineer Aassignment 1.pdf # assignment_1 questions
├── Data Engineer Assignment 2.pdf # assignment_2 questions


### 📌 Folder / File Descriptions

#### 🗂️ `assignment_1/`
Contains the source code, notebooks, scripts, datasets (if included), and any related configuration files for **Assignment 1**. This is where you can find the logic and implementation for the tasks assigned in that specific exercise.

---

#### 📄 `Data Engineer Aassignment 1.pdf`
**Assignment #1** - includes problem statements

---

#### 📄 `Data Engineer Assignment 2.pdf`
**Assignment #2 submission** - includes problem statements

---

#### ⚙️ `.gitignore`
Lists folders and file patterns that are **excluded from version control** (e.g., temporary files, virtual environment folders, build artifacts).

---

## 🛠️ Setup & Getting Started

To run or work with this project locally:

### 1. **Clone the Repository**
```bash
git clone https://github.com/MandarBorhade/adsremedy-de-assignments.git
cd adsremedy-de-assignments
python3 -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
git clone https://github.com/MandarBorhade/adsremedy-de-assignments.git
```
create environment variables in .env file:
POSTGRES_USER= <username>
POSTGRES_PASSWORD= <password>
POSTGRES_DB= adsremedy
PGADMIN_DEFAULT_EMAIL= admin@admin.com
PGADMIN_DEFAULT_PASSWORD= admin

#### Docker setup
Make sure you have docker desktop installed and running.
```
cd adsremedy-de-assignments/assignment_1
docker compose up --build
docker ps
```

#### Check the logs to ensure Spark Master is ready to accept jobs
```
docker logs spark-master
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/scripts/python/data-generator.py
docker exec -it spark-master /opt/spark/bin/spark-submit /opt/spark/work-dir/scripts/python/data-cleaning.py
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077 --packages org.postgresql:postgresql:42.7.3 -c spark.jars.ivy=/opt/spark/work-dir/.ivy2 /opt/spark/work-dir/scripts/python/load-to-postgresdb.py
```
