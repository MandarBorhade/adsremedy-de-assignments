FROM apache/spark:latest

# Switch to root to install packages
USER root

# Install Python dependencies
RUN pip install --no-cache-dir faker psycopg2-binary

# Download Postgres JDBC Driver (Required for Spark to talk to Postgres)
ADD https://jdbc.postgresql.org/download/postgresql-42.7.1.jar /opt/spark/jars/postgresql-42.7.1.jar
RUN chmod 644 /opt/spark/jars/postgresql-42.7.1.jar

# Switch back to the spark user
USER spark