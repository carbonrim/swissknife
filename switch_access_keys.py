import configparser
import os
import csv
import argparse

def replace_aws_access_key_from_csv(profile_name, csv_file_path, aws_config_path="~/.aws/credentials"):
    # Expand the user path for AWS config file
    aws_config_path = os.path.expanduser(aws_config_path)
    
    # Create a config parser
    config = configparser.ConfigParser()
    
    # Read the existing config file
    config.read(aws_config_path)

    # Check if the profile exists in the config file
    if profile_name not in config:
        raise ValueError(f"Profile '{profile_name}' not found in {aws_config_path}")
    
    # Read the CSV file to get the access key and secret access key
    # Add encoding not to include BOM (Byte Order Mark) into read file
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Ensure the CSV contains the necessary columns
        if 'Access key ID' not in reader.fieldnames or 'Secret access key' not in reader.fieldnames:
            raise ValueError("CSV file must contain 'Access key ID' and 'Secret access key' columns")
        
        # Assuming the CSV contains only one row with the keys
        for row in reader:
            new_access_key = row['Access key ID']
            new_secret_key = row['Secret access key']
            break
    
    # Replace the access key and secret key in the config
    config[profile_name]['aws_access_key_id'] = new_access_key
    config[profile_name]['aws_secret_access_key'] = new_secret_key
    
    # Write the updated config back to the file
    with open(aws_config_path, 'w') as configfile:
        config.write(configfile)
    
    print(f"Access key and secret key for profile '{profile_name}' updated successfully.")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Replace AWS access keys in the AWS credentials file.")
    parser.add_argument("profile_name", help="The AWS profile name to update.")
    parser.add_argument("csv_file_path", help="The path to the CSV file containing the new access key and secret key.")
    parser.add_argument("--aws_config_path", default="~/.aws/credentials", help="The path to the AWS credentials file (default: ~/.aws/credentials).")

    # Parse arguments
    args = parser.parse_args()

    # Replace access key from CSV
    replace_aws_access_key_from_csv(args.profile_name, args.csv_file_path, args.aws_config_path)

if __name__ == "__main__":
    main()
