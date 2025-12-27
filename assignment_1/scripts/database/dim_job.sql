
--- CREATE TABLE ---
CREATE TABLE dev.dim_job (
    job_key     INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    job_title   VARCHAR(150),
    department  VARCHAR(100)
);

--- POPULATE TABLE ---
INSERT INTO dev.dim_job (job_title, department)
SELECT DISTINCT job_title, department
FROM dev.employees_clean;

