Member Cleanup Script:
This project contains a Python script designed to clean messy marketing signup data and generate a CRM-ready “Golden Record” dataset. 
The original data export combined signups from multiple landing pages and contained inconsistent formatting, duplicate entries, low-quality test data, and users enrolled in multiple plans. 
The goal of this script was to standardize, validate, and transform the raw export into a reliable dataset suitable for CRM ingestion.
The script first ensures the data is structured correctly and readable. 
It then standardizes all signup dates into a consistent YYYY-MM-DD format to maintain uniformity across records. 
To improve data quality, it identifies and isolates low-quality leads. 
Records that contain obvious test values (such as “test” or “dummy”), invalid email formats, or missing critical information like email or signup date are moved into a separate quarantine.csv file instead of being included in the final dataset.
For deduplication, email address is treated as the unique identifier for each member. 
If multiple records exist for the same email, the script keeps only the most recent signup based on the signup date. 
In cases where a user signed up for both Plan A and Plan B, the script retains the most recent record and adds a boolean flag is_multi_plan = True to preserve important business context. 
This ensures that multi-plan activity is not lost during deduplication.
The final cleaned dataset is exported as members_final.csv, which serves as the CRM-ready Golden Record. 
The script uses Python and the Pandas library for data processing, along with basic validation logic to handle real-world data inconsistencies. 
This project demonstrates practical data cleaning techniques, business-rule-driven logic, and handling of imperfect exports commonly encountered in real-world marketing and CRM workflows.
