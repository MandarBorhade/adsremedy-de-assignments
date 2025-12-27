import csv
import random
import os
import time
import logging
from faker import Faker
from datetime import datetime

# Configure logging to file
# log_dir = "/scripts/logs"
# os.makedirs(log_dir, exist_ok=True)


# Configure logging to file inside the work-dir
log_dir = "/opt/spark/work-dir/scripts/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(log_dir, "data_generator.log"),
    filemode='a'
)
logger = logging.getLogger(__name__)

fake = Faker()

try:
    # Define the target directory relative to the script location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_folder = os.path.join(base_dir, "data")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"employees_{ts}.csv"
    full_path = os.path.join(target_folder, filename)
    
    logger.info(f"Starting data generation for {filename}")
    os.makedirs(target_folder, exist_ok=True)

    # Configuration
    num_records = 1000
    job_titles_by_dept = {
        "IT": ["IT Support Specialist", "Systems Administrator", "DevOps Engineer", "Security Analyst", "IT Manager"],
        "Analytics": ["Data Analyst", "Business Intelligence Analyst", "Data Engineer", "Product Analyst", "Analytics Manager"],
        "HR": ["HR Assistant", "Talent Acquisition Specialist", "HR Generalist", "Learning & Development Lead", "HR Manager"],
        "Sales": ["Sales Associate", "Account Executive", "Business Development Representative", "Sales Operations Analyst", "Sales Manager"],
    }
    statuses = ["Active", "ACTIVE", "Terminated", "On Leave", None]

    def generate_salary():
        base = random.randint(40000, 150000)
        if random.random() > 0.5:
            return f"${base:,}"
        return base

    def generate_email(first, last):
        rand = random.random()
        if rand < 0.05: return f"{first}@{last}"
        elif rand < 0.10: return f"{first}.{last}company.com"
        elif rand < 0.20: return f"{first.lower()}.{last.lower()}@COMPANY.COM"
        return f"{first}.{last}@company.com"

    start_id = int(time.time())
    records = []
    employee_ids = []
    manager_pool = []

    for i in range(num_records):
        first = fake.first_name()
        last = fake.last_name()
        department = random.choice(list(job_titles_by_dept.keys()))
        job_title = random.choice(job_titles_by_dept[department])

        if i > 0 and random.random() < 0.02:
            records.append(records[-1])
            continue

        if random.random() < 0.2:
            department = " " + department.lower() + " "
            job_title = job_title.lower()

        if random.random() < 0.05:
            hire_date = fake.date_between(start_date="+1y", end_date="+5y")
        else:
            hire_date = fake.date_between(start_date="-10y", end_date="today")

        emp_id = start_id + i
        employee_ids.append(emp_id)

        if "manager" in job_title.lower():
            manager_pool.append(emp_id)

        if manager_pool and random.random() > 0.2:
            manager_id = random.choice(manager_pool)
            if manager_id == emp_id: manager_id = ""
        else:
            manager_id = random.choice(["", "N/A", random.randint(9999, 12000)])

        row = [emp_id, first.lower() if random.random() > 0.5 else first, last.upper() if random.random() > 0.5 else last,
               generate_email(first, last), hire_date, job_title, department, generate_salary(), manager_id,
               fake.street_address(), fake.city(), fake.state_abbr(), fake.zipcode(),
               fake.date_of_birth(minimum_age=22, maximum_age=65), random.choice(statuses)]
        records.append(row)

    with open(full_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["employee_id", "first_name", "last_name", "email", "hire_date", "job_title", "department", "salary", "manager_id", "address", "city", "state", "zip_code", "birth_date", "status"])
        writer.writerows(records)

    logger.info(f"Successfully generated {len(records)} records in {filename}")

except Exception as e:
    logger.error(f"Failed to generate data: {str(e)}", exc_info=True)
    raise