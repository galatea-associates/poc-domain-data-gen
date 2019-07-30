import json
import os
from datetime import timedelta, date

def main():
    # Set todays date, and subtract the required number of dates to find starting point
    todays_date = date.today()
    day_count = 2
    start_date = todays_date - timedelta(day_count-1)
    
    # Iterate from start date through todays date, generating swaps positions for each
    for n in range(day_count):
            current_date = start_date + timedelta(n)

            # Open configuration file #
            config_file_path = "src/config.json"
            with open(config_file_path) as config_file:
                config = json.load(config_file)
            
            # Rewrite start and end dates to be the current iterations #
            current_date_string = date.strftime(current_date, '%Y%m%d')
            config['shared_domain_object_args'] = "{'start_date':'"+current_date_string+", 'end_date': '"+current_date_string+"'}"
            
            # Replace output file names to append dates to ensure unique
            # Hardcoded search through config, quickest method, may be worth updating config structure
            config['domain_objects'][0]['file_name'] = 'instruments_'+current_date_string
            config['domain_objects'][1]['file_name'] = 'counterparty_'+current_date_string
            config['domain_objects'][9]['file_name'] = 'swap_contract_'+current_date_string
            config['domain_objects'][10]['file_name'] = 'swap_position_'+current_date_string
            config['domain_objects'][11]['file_name'] = 'cashflow_'+current_date_string

            # TODO: Merge files rather than having individual ones for each day
            #   This could be achieved by .gz and appending

            # Replace old configuration file with new
            os.remove(config_file_path)
            with open(config_file_path, 'w') as f:
                    json.dump(config, f, indent=2)

            # Generate data for this day #
            os.system("python src/app.py")
            

if __name__ == '__main__':   
    main()