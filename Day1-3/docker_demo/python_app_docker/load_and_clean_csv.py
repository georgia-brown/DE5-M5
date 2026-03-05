# ======================================================================
# Import Packages
# ======================================================================

import pandas as pd
import sqlalchemy
# import pyodbc
import argparse

# ======================================================================
# Define Constants
# ======================================================================

# directory = "C:\\Users\\\Admin\\Desktop\\DE5-M5\\docker_demo\\python_app_docker"
books_input_file_path = "data/03_Library Systembook.csv"
customers_input_file_path  = "data/03_Library SystemCustomers.csv"
books_output_file_path = "data/books_cleaned"
customers_output_file_path  = "data/customers_cleaned"
data_quality_metrics_output_path = "data/data_metrics.csv"

sql_server = "STUDENT02"

# ======================================================================
# Define Functions
# ======================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Library ETL Pipeline"
    )
    parser.add_argument(
        "--write-sql",
        action="store_true",
        help = "Write cleaned data to SQL Server"
    )
    return parser.parse_args()

def load_csv(file_path):
    """Loads csv into dataframe
    Args:
        file_path: File path of csv to load

    Returns: 
        df: Dataframe from csv data
    """
    df = pd.read_csv(file_path)
    return df

def clean_df(df, string_cols, date_cols):
    """Cleans dataframe, including null rows, filed names, string and date cleaning
    Args:
        df: Dataframe to clean
        string_cols: List of columns to apply string cleaning to
        date_cols: List of columns to apply date cleaning to 

    Returns: 
        df_cleaned: Dataframe with cleaning applied
    """
    df_cleaned = df.dropna(how='all')
    df_cleaned.columns = df_cleaned.columns.str.title()
    for col in string_cols:
        df_cleaned[col] = df_cleaned[col].str.title()
        df_cleaned[col] = df_cleaned[col].str.strip()
    for col in date_cols:
        df_cleaned[col] = df_cleaned[col].str.replace('"','')
        df_cleaned[col] = pd.to_datetime(df_cleaned[col],errors="coerce")
    return df_cleaned


def clean_customer_data(customer_df):
    """Cleans customer dataframe
    Args:
        customer_df: Customer dataframe to clean

    Returns: 
        customer_cleaned_df: Customer dataframe with cleaning applied
    """
    customer_cleaned_df = clean_df(customer_df,["Customer Name"],[])
    return customer_cleaned_df


def clean_books_data(books_df):
    """Cleans books dataframe
    Args:
        books_df: Books dataframe to clean

    Returns: 
        books_cleaned_df: Books dataframe with cleaning applied
    """
    books_cleaned_df = clean_df(books_df,["Books"],["Book Checkout", "Book Returned"])
    books_cleaned_df["Days Allowed To Borrow"] = books_cleaned_df["Days Allowed To Borrow"].str.replace('weeks','')
    books_cleaned_df["Days Allowed To Borrow"] = books_cleaned_df["Days Allowed To Borrow"].astype(int)*7
    return books_cleaned_df

def enrich_books_data(books_df):
    """ Creates a new col to work out the "Time on loan". ie the difference between the date checked out and date checked in.
    Args:
        books_df: Book dataframe to enrich

    Returns: 
        books_enriched: Book dataframe with added "Time on loan" column
    """
    books_enriched = books_df.copy()
    books_enriched["Time On Loan"] = (books_enriched["Book Returned"] - books_enriched["Book Checkout"]).dt.days
    return books_enriched

def write_data_metrics_to_csv(raw_df,cleaned_df, table_name, output_path):
    count_rows_dropped = len(raw_df)-len(cleaned_df)

    metrics = {
        "Table": table_name,
        "Raw Row Count": len(raw_df),
        "Cleaned Row Count": len(cleaned_df),
        "Rows Dropped": count_rows_dropped
    }

    # Count nulls per column in cleaned data
    for col in cleaned_df.columns:
        metrics[f"Null Count - {col}"] = cleaned_df[col].isna().sum()

    metrics_df = pd.DataFrame([metrics])

    # Append if file exists
    try:
        existing = pd.read_csv(output_path)
        metrics_df = pd.concat([existing, metrics_df], ignore_index=True)
    except FileNotFoundError:
        pass

    metrics_df.to_csv(output_path, index=False)


def write_to_sql(df, server, database, table_name):
    """ Writes a dataframe to SQL Server table
    Args:
        df: Dataframe to write to table
        server: SQL server location to write to
        database: Database to write to
        table_name: Table name to write to
    """
    connection_string = (f"mssql+pyodbc://{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes")
    engine = sqlalchemy.create_engine(connection_string)
    df.to_sql(table_name, engine, if_exists="replace",index=False)

# ======================================================================
# Main
# ======================================================================

def main():
    args = parse_args()

    books_raw_df = load_csv(books_input_file_path)
    books_cleaned_df = clean_books_data(books_raw_df)
    books_enriched_df = enrich_books_data(books_cleaned_df)

    write_data_metrics_to_csv(raw_df=books_raw_df,
                              cleaned_df= books_enriched_df, 
                              table_name="Books", 
                              output_path=data_quality_metrics_output_path
                            )

    customers_raw_df = load_csv(customers_input_file_path)
    customers_cleaned_df = clean_customer_data(customers_raw_df)
    
    write_data_metrics_to_csv(raw_df=customers_raw_df,
                              cleaned_df= customers_cleaned_df, 
                              table_name="Customers", 
                              output_path=data_quality_metrics_output_path
                            )
    
    print(books_enriched_df.head(5))
    print(customers_cleaned_df.head(5))
    print("Data Cleaning Done")
    

    # if args.write_sql:
    #     write_to_sql(books_enriched_df, sql_server, "Library", "Books")
    #     write_to_sql(customers_cleaned_df, sql_server, "Library", "Customers")
    # else:
    #     print("Skipped write to SQL")

    # print(customers_cleaned_df)
    # print(books_enriched_df)

    # customers_cleaned_df.to_csv(customers_output_file_path)
    # books_enriched_df.to_csv(books_output_file_path)

    
if __name__ == "__main__":
    main()