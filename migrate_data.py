#!/usr/bin/env python
"""
Migrate company and job data from SQLite (placement.db) to MySQL
"""
import sys
import sqlite3
import pymysql

# MySQL connection details
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'Rahi@120'
mysql_db = 'placement_system'

print(f"Connecting to MySQL: {mysql_user}@{mysql_host}/{mysql_db}")
print(f"Reading from SQLite: backend/instance/placement.db\n")

try:
    # Connect to SQLite
    sqlite_conn = sqlite3.connect('backend/instance/placement.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to MySQL
    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db)
    mysql_cursor = mysql_conn.cursor()
    
    # Migrate Companies
    print("Migrating companies...")
    sqlite_cursor.execute("SELECT id, name, description, created_at FROM companies")
    companies = sqlite_cursor.fetchall()
    
    if companies:
        for company in companies:
            company_id, name, description, created_at = company
            try:
                mysql_cursor.execute(
                    "INSERT INTO companies (id, name, description, created_at) VALUES (%s, %s, %s, %s)",
                    (company_id, name, description, created_at)
                )
                print(f"  ✓ Company: {name}")
            except pymysql.err.IntegrityError as e:
                print(f"  ! Company {name} already exists (skipping): {e}")
        mysql_conn.commit()
        print(f"✓ {len(companies)} company(ies) migrated\n")
    else:
        print("  No companies found in SQLite\n")
    
    # Migrate Jobs
    print("Migrating jobs...")
    sqlite_cursor.execute("SELECT id, company_id, title, description, salary, posted_at FROM jobs")
    jobs = sqlite_cursor.fetchall()
    
    if jobs:
        for job in jobs:
            job_id, company_id, title, description, salary, posted_at = job
            try:
                mysql_cursor.execute(
                    "INSERT INTO jobs (id, company_id, title, description, salary, posted_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    (job_id, company_id, title, description, salary, posted_at)
                )
                print(f"  ✓ Job: {title}")
            except pymysql.err.IntegrityError as e:
                print(f"  ! Job {title} already exists (skipping): {e}")
        mysql_conn.commit()
        print(f"✓ {len(jobs)} job(s) migrated\n")
    else:
        print("  No jobs found in SQLite\n")
    
    print("Migration complete!")
    
    # Verify
    mysql_cursor.execute("SELECT COUNT(*) FROM companies")
    company_count = mysql_cursor.fetchone()[0]
    mysql_cursor.execute("SELECT COUNT(*) FROM jobs")
    job_count = mysql_cursor.fetchone()[0]
    
    print(f"\nMySQL now has:")
    print(f"  - {company_count} companies")
    print(f"  - {job_count} jobs")
    
    sqlite_conn.close()
    mysql_conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
