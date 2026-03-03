import pandas as pd

books_input_file_path = 'C:\\Users\\Admin\\Desktop\\DE5-M5\\data\\03_Library Systembook.csv'
customers_input_file_path  = 'C:\\Users\\Admin\\Desktop\\DE5-M5\\data\\03_Library SystemCustomers.csv'
books_output_file_path = "C:\\Users\\Admin\\Desktop\\DE5-M5\\data\\books_cleaned"
customers_output_file_path  = "C:\\Users\\Admin\\Desktop\\DE5-M5\\data\\customers_cleaned"

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def clean_df(df, string_cols, date_cols):
    df_cleaned = df.dropna()
    df_cleaned.columns = df_cleaned.columns.str.title()
    for col in string_cols:
        df_cleaned[col] = df_cleaned[col].str.title()
        df_cleaned[col] = df_cleaned[col].str.strip()
    for col in date_cols:
        df_cleaned[col] = df_cleaned[col].str.replace('"','')
        df_cleaned[col] = pd.to_datetime(df_cleaned[col],errors="coerce")
    return df_cleaned


def clean_customer_data(customer_df):
    df_cleaned = clean_df(customer_df,["Customer Name"],[])
    return df_cleaned


def clean_books_data(books_df):
    df_cleaned = clean_df(books_df,["Books"],["Book Checkout", "Book Returned"])
    df_cleaned["Days Allowed To Borrow"] = df_cleaned["Days Allowed To Borrow"].str.replace('weeks','')
    df_cleaned["Days Allowed To Borrow"] = df_cleaned["Days Allowed To Borrow"].astype(int)*7
    return df_cleaned

books_raw_df = load_csv(books_input_file_path)
customers_raw_df = load_csv(customers_input_file_path)

customers_cleaned_df = clean_customer_data(customers_raw_df)
books_cleaned_df = clean_books_data(books_raw_df)

print(customers_cleaned_df)
print(books_cleaned_df)

customers_cleaned_df.to_csv(customers_output_file_path)
books_cleaned_df.to_csv(books_output_file_path)