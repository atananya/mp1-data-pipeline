The pipeline loads a CSV file, then validates it, cleans it and saves the results. The pipeline code runs each stem and the modules for them life in the src folder. The data_loaders file reads the input and the config files. The data_validator file checks for required columns and removes rows with invalid numbers. the data processor file removes duplicates, missing values and outliers. The data_output saves the cleaned CSV and utils handles logging and file checks.
INPUT: python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
OUTPUT:  INFO     src.utils — Input file validated: fixtures/sample_data.csv
INFO     src.utils — Input file validated: config/config.yaml
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config/config.yaml
WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
INFO     __main__ — Validation complete: 100 -> 98 rows
INFO     __main__ — Processing complete: 98 -> 92 rows
INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}