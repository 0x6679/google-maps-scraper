import pandas as pd
import glob

def merge_csvs_remove_duplicates(directory, output_file):
    # Path pattern to match all CSV files in the directory
    csv_files = glob.glob(directory + '/*.csv')
    
    # List to hold dataframes
    dataframes = []
    
    # Read each CSV file and append to the list
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
    
    # Concatenate all dataframes into one
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    # Remove duplicates based on the 'phone_number' column
    # Adjust the column name if it varies
    #combined_df = combined_df.drop_duplicates(subset='Phone')
    
    # Save the combined dataframe to a CSV file
    combined_df.to_csv(output_file, index=False)

# Usage
merge_csvs_remove_duplicates('./', 'combined2_output.csv')