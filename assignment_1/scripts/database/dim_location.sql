--- CREATE TABLe ---
CREATE TABLE dev.dim_location (
    location_key INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    address      VARCHAR(255),
    city         VARCHAR(100),
    state        VARCHAR(50),
    zip_code     VARCHAR(20)
);


--- POPULATE TABLE ---
INSERT INTO dim_location (address, city, state, zip_code)
SELECT DISTINCT address, city, state, zip_code
FROM employees_clean;
