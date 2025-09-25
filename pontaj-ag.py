# %%
import pandas as pd
import re
from datetime import datetime, timedelta

# Define the path to your raw chat data
raw_file_path = "Conversatie Whatsapp.txt"

# %%
# # --- Part 1: Find the 15 newest unique dates ---
# # Define the regex pattern for a timestamp at the start of a line
# timestamp_pattern = r"^\d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}"

# # Read all lines to find all unique dates
# with open(raw_file_path, 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# unique_dates = set()
# for line in lines:
#     if re.match(timestamp_pattern, line):
#         try:
#             date_str = line.split(',')[0].strip()
#             date_obj = datetime.strptime(date_str, "%d.%m.%Y").date()
#             unique_dates.add(date_obj)
#         except (ValueError, IndexError):
#             continue

# # Sort the unique dates in descending order and get the newest 15
# sorted_dates = sorted(list(unique_dates), reverse=True)
# last_15_dates = set(sorted_dates[:15])

# if not last_15_dates:
#     print("No valid dates found in the file.")
#     exit()

# %%
# --- Part 1: Get user input and generate the date range ---
try:
    start_date_str = input("Data de inceput (DD.MM.YYYY): ")
    end_date_str = input("Data de sfarsit (DD.MM.YYYY): ")
    
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
    end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
    
    # Check if the end date is before the start date
    if end_date < start_date:
        print("Eroare: Data de inceput nu poate fi mai mica ca data de sfarsit.")
        exit()

except ValueError:
    print("Eroare: data introdusa nu este valida. Foloseste DD.MM.YYYY, de ex 24.03.2025.")
    exit()

# Generate a set of all dates in the specified range
date_range = set()
current_date = start_date
while current_date <= end_date:
    date_range.add(current_date)
    current_date += timedelta(days=1)

if not date_range:
    print("Nu au fost gasite date pentru intervalul specificat.")
    exit()

# Define the regex pattern for a timestamp at the start of a line
#timestamp_pattern = re.compile(r"^\d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}", re.DOTALL)

# Read all lines from the file
# with open(raw_file_path, 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# %%
# --- Part 2: Process the raw data and build the DataFrame ---
data_dict = {}
current_message_lines = []
current_date_in_loop = None

# %%
# Regex patterns for extraction (from your previous code)
#message_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4}),\s+(\d{2}:\d{2})\s+-\s+(.*)")
timestamp_pattern = re.compile(r"^\d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}\s+-\s+(.*)", re.DOTALL)
vehicles = [

    r'[Mm]a[sș]in[aă]\s?personal[aă]', r'[Ii]veco\s?prelat[ăa]', r'[Ii]veco\b', r'[Pp]relat[ăa]\b', r'Peugeot\s?Expert',
    r'Peugeot\b', r'[Mm]acara\b', r'[Pp]ersonal[ăa](?:\s+\w+)?', r'[Tt][Kk]\b', r'Renault\s?TK'
    ]
vehicle_pattern = re.compile(r"|".join(vehicles), re.IGNORECASE)
# start_keywords = re.compile(r'Am\.?\s?început|Am\.?\s?inceput', re.IGNORECASE)
#start_keywords = re.compile(r'[Aa][mn]\.?[ -]?[îi]nc[eău]p[uei]t', re.IGNORECASE)

start_keywords = re.compile(r'[Aa][mn][\.\s\-]*[îi]nc[eău]p[uei]t', re.IGNORECASE)
end_keywords = re.compile(r'[Aa][mn][\.\s\-]*terminat', re.IGNORECASE)
# Read all lines from the file
with open(raw_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# %%
# Iterate through all lines once
# for line in lines:
#     if re.match(timestamp_pattern, line):
#         # A new message starts, so process the previous one if it exists and is from a valid date
#         if current_message and current_date_in_loop in date_range:
#             match = message_pattern.match(current_message)
#             if match:
#                 date_str, time_str, message_content = match.groups()
                
#                 name_end_index = message_content.find(":")
#                 if name_end_index != -1:
#                     name_str = message_content[:name_end_index].strip()
#                     message_body = message_content[name_end_index+1:].strip()
#                 else:
#                     name_str = "Unknown"
#                     message_body = message_content.strip()

#                 ora_intrare = None
#                 if start_keywords.search(message_body):
#                     ora_intrare = time_str
                
#                 ora_iesire = None
#                 if end_keywords.search(message_body):
#                     ora_iesire = time_str

#                 masina = None
                
#                 # Remove keywords and punctuation before searching for vehicles
#                 body_without_keywords = start_keywords.sub('', message_body)
#                 body_without_keywords = end_keywords.sub('', body_without_keywords)
                
#                 # Clean up separators like '/' and '-' to allow vehicles to be matched
#                 cleaned_body = re.sub(r'[/,;:\-]', ' ', body_without_keywords)
                
#                 masina_list = []
                
#                 # Find all vehicles in the message body
#                 for m in vehicle_pattern.finditer(cleaned_body):
#                     found_vehicle = m.group(0).strip()
                    
#                     # Handle special case for 'Personala' or 'Personală'
#                     if 'personal' in found_vehicle.lower():
#                         try:
#                             words = message_body.split()
#                             personal_word_index = -1
#                             for i, word in enumerate(words):
#                                 if re.search(r'Personal(a|ă)', word, re.IGNORECASE):
#                                     personal_word_index = i
#                                     break
                            
#                             if personal_word_index + 1 < len(words):
#                                 masina_text = f"{found_vehicle} {words[personal_word_index + 1]}"
#                             else:
#                                 masina_text = found_vehicle
#                         except (ValueError, IndexError):
#                             masina_text = found_vehicle
#                     else:
#                         masina_text = found_vehicle
                    
#                     masina_list.append(masina_text.strip())

#                 masina = ', '.join(masina_list) if masina_list else None

#                 locatii = message_body
#                 locatii = start_keywords.sub('', locatii)
#                 locatii = end_keywords.sub('', locatii)
                

#                 # Remove all found vehicle texts from the Locatii string
#                 if masina_list:
#                     for found_vehicle_text in masina_list:
#                         locatii = locatii.replace(found_vehicle_text, '').strip()

#                 # Corrected cleanup: Add '.' to the set of characters to be removed
#                 locatii = re.sub(r'^\s*[-.,\s:]+', '', locatii).strip()
#                 locatii = re.sub(r'[-.,\s:]+$', '', locatii).strip()
#                 if not locatii:
#                     locatii = None
                

#                 key = (name_str, date_str)
#                 if key not in data_dict:
#                     data_dict[key] = {
#                         'Numele': name_str,
#                         'Data': date_str,
#                         'Ora intrare': ora_intrare,
#                         'Ora iesire': ora_iesire,
#                         'Masina': masina,
#                         'Locatii': locatii
#                     }
#                 else:
#                     if ora_intrare:
#                         data_dict[key]['Ora intrare'] = ora_intrare
#                     if ora_iesire:
#                         data_dict[key]['Ora iesire'] = ora_iesire
#                     if masina:
#                         data_dict[key]['Masina'] = masina
#                     if locatii:
#                         data_dict[key]['Locatii'] = locatii
# Iterate through all lines once
# Iterate through all lines once
# for line in lines:
#     line = line.strip()
#     if not line:
#         continue
    
#     match = timestamp_pattern.match(line)
#     if match:
#         # A new message starts, process the previous one if it exists
#         if current_message_lines:
            
#             # Combine all previous lines into one message string
#             full_message = " ".join(current_message_lines)
#             message_match = timestamp_pattern.match(full_message)

#             if message_match:
#                 message_content = message_match.group(1).strip()
                
#                 # Extract date and time from the first line of the message
#                 date_and_time_str = full_message.split(' - ')[0]
#                 date_str = date_and_time_str.split(',')[0].strip()
#                 time_str = date_and_time_str.split(',')[1].strip()

#                 name_end_index = message_content.find(":")
#                 if name_end_index != -1:
#                     name_str = message_content[:name_end_index].strip()
#                     message_body = message_content[name_end_index+1:].strip()
#                 else:
#                     name_str = "Unknown"
#                     message_body = message_content.strip()

#                 ora_intrare = None
#                 if start_keywords.search(message_body):
#                     ora_intrare = time_str
                
#                 ora_iesire = None
#                 if end_keywords.search(message_body):
#                     ora_iesire = time_str

#                 masina_list = []
#                 cleaned_body_for_vehicles = re.sub(r'[/,;:\-]', ' ', message_body)
#                 for m in vehicle_pattern.finditer(cleaned_body_for_vehicles):
#                     masina_list.append(m.group(0).strip())
#                 masina = ', '.join(masina_list) if masina_list else None

#                 locatii = message_body
#                 locatii = start_keywords.sub('', locatii)
#                 locatii = end_keywords.sub('', locatii)
                
#                 if masina_list:
#                     for found_vehicle_text in masina_list:
#                         locatii = re.sub(r'\b' + re.escape(found_vehicle_text) + r'\b', '', locatii, flags=re.IGNORECASE)

#                 locatii = re.sub(r'^\s*[-.,\s:]+', '', locatii).strip()
#                 locatii = re.sub(r'[-.,\s:]+$', '', locatii).strip()
#                 if not locatii:
#                     locatii = None
                
#                 current_date_in_loop = datetime.strptime(date_str, "%d.%m.%Y").date()

#                 if current_date_in_loop in date_range:
#                     key = (name_str, date_str)
#                     if key not in data_dict:
#                         data_dict[key] = {
#                             'Numele': name_str,
#                             'Data': date_str,
#                             'Ora intrare': ora_intrare,
#                             'Ora iesire': ora_iesire,
#                             'Masina': masina,
#                             'Locatii': locatii
#                         }
#                     else:
#                         if ora_intrare:
#                             data_dict[key]['Ora intrare'] = ora_intrare
#                         if ora_iesire:
#                             data_dict[key]['Ora iesire'] = ora_iesire
#                         if masina:
#                             data_dict[key]['Masina'] = masina
#                         if locatii:
#                             data_dict[key]['Locatii'] = locatii

#         # Start a new message
#         current_message_lines = [line]
#     else:
#         # If no timestamp, append to current message lines
#         current_message_lines.append(line)

# # Process the very last message in the file after the loop ends
# if current_message_lines:
#     full_message = " ".join(current_message_lines)
#     message_match = timestamp_pattern.match(full_message)

#     if message_match:
#         message_content = message_match.group(1).strip()
#         date_and_time_str = full_message.split(' - ')[0]
#         date_str = date_and_time_str.split(',')[0].strip()
#         time_str = date_and_time_str.split(',')[1].strip()

#         name_end_index = message_content.find(":")
#         if name_end_index != -1:
#             name_str = message_content[:name_end_index].strip()
#             message_body = message_content[name_end_index+1:].strip()
#         else:
#             name_str = "Unknown"
#             message_body = message_content.strip()

#         ora_intrare = None
#         if start_keywords.search(message_body):
#             ora_intrare = time_str
        
#         ora_iesire = None
#         if end_keywords.search(message_body):
#             ora_iesire = time_str

#         masina_list = []
#         cleaned_body_for_vehicles = re.sub(r'[/,;:\-]', ' ', message_body)
#         for m in vehicle_pattern.finditer(cleaned_body_for_vehicles):
#             masina_list.append(m.group(0).strip())
#         masina = ', '.join(masina_list) if masina_list else None

#         locatii = message_body
#         locatii = start_keywords.sub('', locatii)
#         locatii = end_keywords.sub('', locatii)
        
#         if masina_list:
#             for found_vehicle_text in masina_list:
#                 locatii = re.sub(r'\b' + re.escape(found_vehicle_text) + r'\b', '', locatii, flags=re.IGNORECASE)

#         locatii = re.sub(r'^\s*[-.,\s:]+', '', locatii).strip()
#         locatii = re.sub(r'[-.,\s:]+$', '', locatii).strip()
#         if not locatii:
#             locatii = None

#         current_date_in_loop = datetime.strptime(date_str, "%d.%m.%Y").date()

#         if current_date_in_loop in date_range:
#             key = (name_str, date_str)
#             if key not in data_dict:
#                 data_dict[key] = {
#                     'Numele': name_str,
#                     'Data': date_str,
#                     'Ora intrare': ora_intrare,
#                     'Ora iesire': ora_iesire,
#                     'Masina': masina,
#                     'Locatii': locatii
#                 }
#             else:
#                 if ora_intrare:
#                     data_dict[key]['Ora intrare'] = ora_intrare
#                 if ora_iesire:
#                     data_dict[key]['Ora iesire'] = ora_iesire
#                 if masina:
#                     data_dict[key]['Masina'] = masina
#                 if locatii:
#                     data_dict[key]['Locatii'] = locatii      
    #     # Start a new message
    #     current_message = line.strip()
    #     current_date_str = line.split(',')[0].strip()
    #     current_date_in_loop = datetime.strptime(current_date_str, "%d.%m.%Y").date()
    # else:
    #     # If no timestamp, append to current message
    #     current_message += " " + line.strip()

# %%
# Iterate through all lines once
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    match = timestamp_pattern.match(line)
    if match:
        # A new message starts, process the previous one if it exists
        if current_message_lines:
            
            # Combine all previous lines into one message string
            full_message = " ".join(current_message_lines)
            message_match = timestamp_pattern.match(full_message)

            if message_match:
                date_and_time_str = full_message.split(' - ')[0]
                date_str = date_and_time_str.split(',')[0].strip()
                time_str = date_and_time_str.split(',')[1].strip()
                message_content = message_match.group(1).strip()
                
                name_end_index = message_content.find(":")
                if name_end_index != -1:
                    name_str = message_content[:name_end_index].strip()
                    message_body = message_content[name_end_index+1:].strip()
                else:
                    name_str = "Unknown"
                    message_body = message_content.strip()

                ora_intrare = None
                if start_keywords.search(message_body):
                    ora_intrare = time_str
                
                ora_iesire = None
                if end_keywords.search(message_body):
                    ora_iesire = time_str

                masina_list = []
                cleaned_body_for_vehicles = re.sub(r'[/,;:\-]', ' ', message_body)
                for m in vehicle_pattern.finditer(cleaned_body_for_vehicles):
                    masina_list.append(m.group(0).strip())
                masina = ', '.join(masina_list) if masina_list else None

                locatii = message_body
                locatii = start_keywords.sub('', locatii)
                locatii = end_keywords.sub('', locatii)
                
                if masina_list:
                    for found_vehicle_text in masina_list:
                        locatii = re.sub(r'\b' + re.escape(found_vehicle_text) + r'\b', '', locatii, flags=re.IGNORECASE)

                locatii = re.sub(r'^\s*[-.,\s:]+', '', locatii).strip()
                locatii = re.sub(r'[-.,\s:]+$', '', locatii).strip()
                if not locatii:
                    locatii = None
                
                current_date_in_loop = datetime.strptime(date_str, "%d.%m.%Y").date()

                if current_date_in_loop in date_range:
                    key = (name_str, date_str)
                    if key not in data_dict:
                        data_dict[key] = {
                            'Numele': name_str,
                            'Data': date_str,
                            'Ora intrare': ora_intrare,
                            'Ora iesire': ora_iesire,
                            'Masina': masina,
                            'Locatii': locatii
                        }
                    else:
                        # # Append to existing entry instead of overwriting
                        # if ora_intrare and not data_dict[key]['Ora intrare']:
                        #     data_dict[key]['Ora intrare'] = ora_intrare
                        # if ora_iesire and not data_dict[key]['Ora iesire']:
                        #     data_dict[key]['Ora iesire'] = ora_iesire
                        # if masina and masina not in data_dict[key]['Masina']:
                        #     if data_dict[key]['Masina']:
                        #         data_dict[key]['Masina'] += f", {masina}"
                        #     else:
                        #         data_dict[key]['Masina'] = masina
                        # if locatii and locatii not in data_dict[key]['Locatii']:
                        #     if data_dict[key]['Locatii']:
                        #         data_dict[key]['Locatii'] += f", {locatii}"
                        #     else:
                        #         data_dict[key]['Locatii'] = locatii
                        # Initialize Masina and Locatii to an empty string if they are None
                        if data_dict[key]['Masina'] is None:
                            data_dict[key]['Masina'] = ''
                        if data_dict[key]['Locatii'] is None:
                            data_dict[key]['Locatii'] = ''

                        # Append to existing entry instead of overwriting
                        if ora_intrare and not data_dict[key]['Ora intrare']:
                            data_dict[key]['Ora intrare'] = ora_intrare
                        if ora_iesire and not data_dict[key]['Ora iesire']:
                            data_dict[key]['Ora iesire'] = ora_iesire

                        if masina:
                            # Check if the vehicle is not already in the string to avoid duplicates
                            if masina not in data_dict[key]['Masina']:
                                if data_dict[key]['Masina']:
                                    data_dict[key]['Masina'] += f", {masina}"
                                else:
                                    data_dict[key]['Masina'] = masina

                        if locatii:
                            # Check if the location is not already in the string to avoid duplicates
                            if locatii not in data_dict[key]['Locatii']:
                                if data_dict[key]['Locatii']:
                                    data_dict[key]['Locatii'] += f", {locatii}"
                                else:
                                    data_dict[key]['Locatii'] = locatii

        # Start a new message
        current_message_lines = [line]
    else:
        # If no timestamp, append to current message lines
        current_message_lines.append(line)

# Process the very last message in the file after the loop ends
if current_message_lines:
    full_message = " ".join(current_message_lines)
    message_match = timestamp_pattern.match(full_message)

    if message_match:
        date_and_time_str = full_message.split(' - ')[0]
        date_str = date_and_time_str.split(',')[0].strip()
        time_str = date_and_time_str.split(',')[1].strip()
        message_content = message_match.group(1).strip()
        
        name_end_index = message_content.find(":")
        if name_end_index != -1:
            name_str = message_content[:name_end_index].strip()
            message_body = message_content[name_end_index+1:].strip()
        else:
            name_str = "Unknown"
            message_body = message_content.strip()

        ora_intrare = None
        if start_keywords.search(message_body):
            ora_intrare = time_str
        
        ora_iesire = None
        if end_keywords.search(message_body):
            ora_iesire = time_str

        masina_list = []
        cleaned_body_for_vehicles = re.sub(r'[/,;:\-]', ' ', message_body)
        for m in vehicle_pattern.finditer(cleaned_body_for_vehicles):
            masina_list.append(m.group(0).strip())
        masina = ', '.join(masina_list) if masina_list else None

        locatii = message_body
        locatii = start_keywords.sub('', locatii)
        locatii = end_keywords.sub('', locatii)
        
        if masina_list:
            for found_vehicle_text in masina_list:
                locatii = re.sub(r'\b' + re.escape(found_vehicle_text) + r'\b', '', locatii, flags=re.IGNORECASE)

        locatii = re.sub(r'^\s*[-.,\s:]+', '', locatii).strip()
        locatii = re.sub(r'[-.,\s:]+$', '', locatii).strip()
        if not locatii:
            locatii = None

        current_date_in_loop = datetime.strptime(date_str, "%d.%m.%Y").date()

        if current_date_in_loop in date_range:
            key = (name_str, date_str)
            if key not in data_dict:
                data_dict[key] = {
                    'Numele': name_str,
                    'Data': date_str,
                    'Ora intrare': ora_intrare,
                    'Ora iesire': ora_iesire,
                    'Masina': masina,
                    'Locatii': locatii
                }
            else:
                if ora_intrare and not data_dict[key]['Ora intrare']:
                    data_dict[key]['Ora intrare'] = ora_intrare
                if ora_iesire and not data_dict[key]['Ora iesire']:
                    data_dict[key]['Ora iesire'] = ora_iesire
                if masina and masina not in data_dict[key]['Masina']:
                    if data_dict[key]['Masina']:
                        data_dict[key]['Masina'] += f", {masina}"
                    else:
                        data_dict[key]['Masina'] = masina
                if locatii and locatii not in data_dict[key]['Locatii']:
                    if data_dict[key]['Locatii']:
                        data_dict[key]['Locatii'] += f", {locatii}"
                    else:
                        data_dict[key]['Locatii'] = locatii

# %%
# # --- Part 2: Process the raw data and build the DataFrame ---
# data_dict = {}
# current_message = ""
# current_date = None

# # Regex patterns for extraction (from your previous code)
# message_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4}),\s+(\d{2}:\d{2})\s+-\s+(.*)")
# vehicles = [
#     r'[Ii]veco\s?prelat[ăa]', r'[Ii]veco', r'[Pp]relat[ăa]', r'Peugeot\s?Expert',
#     r'Peugeot', r'[Mm]acara', r'[Pp]ersonal[ăa]', r'[Tt][Kk]', r'Renault\s?TK'
#     ]
# vehicle_pattern = re.compile(r"|".join(vehicles), re.IGNORECASE)
# # start_keywords = re.compile(r'Am\.?\s?început|Am\.?\s?inceput', re.IGNORECASE)
# #start_keywords = re.compile(r'[Aa][mn]\.?[ -]?[îi]nc[eău]p[uei]t', re.IGNORECASE)

# start_keywords = re.compile(r'[Aa][mn][\.\s\-]*[îi]nc[eău]p[uei]t', re.IGNORECASE)
# end_keywords = re.compile(r'[Aa][mn][\.\s\-]*terminat', re.IGNORECASE)

# # Iterate through all lines once
# for line in lines:
#     if re.match(timestamp_pattern, line):
#         # A new message starts, so process the previous one if it exists and is from a valid date
#         if current_message and current_date in last_15_dates:
#             match = message_pattern.match(current_message)
#             if match:
#                 date_str, time_str, message_content = match.groups()
                
#                 # ... (Parsing logic from your previous Step 2) ...
#                 name_end_index = message_content.find(":")
#                 if name_end_index != -1:
#                     name_str = message_content[:name_end_index].strip()
#                     message_body = message_content[name_end_index+1:].strip()
#                 else:
#                     name_str = "Unknown"
#                     message_body = message_content.strip()

#                 ora_intrare = None
#                 if start_keywords.search(message_body):
#                     ora_intrare = time_str
                
#                 ora_iesire = None
#                 if end_keywords.search(message_body):
#                     ora_iesire = time_str

#                 masina = None
#                 body_without_keywords = start_keywords.sub('', message_body)
#                 body_without_keywords = end_keywords.sub('', body_without_keywords)
                
#                 masina_found = False
#                 for m in vehicle_pattern.finditer(body_without_keywords):
#                     found_vehicle = m.group(0).strip()
#                     if 'personal' in found_vehicle.lower():
#                         try:
#                             words = message_body.split()
#                             personal_word_index = words.index(found_vehicle)
#                             if personal_word_index + 1 < len(words):
#                                 masina = f"{found_vehicle} {words[personal_word_index + 1]}"
#                             else:
#                                 masina = found_vehicle
#                             masina_found = True
#                             break
#                         except (ValueError, IndexError):
#                             pass
                    
#                     if masina is None:
#                         masina = found_vehicle
#                         masina_found = True
#                         break

#                 locatii = message_body
#                 locatii = start_keywords.sub('', locatii)
#                 locatii = end_keywords.sub('', locatii)
                
#                 if masina_found and masina is not None:
#                     locatii = locatii.replace(masina, '').strip()
                
#                 locatii = re.sub(r'^\s*[-,\s:]+', '', locatii).strip()
#                 locatii = re.sub(r'[-,\s:]+$', '', locatii).strip()
#                 if not locatii:
#                     locatii = None

#                 key = (name_str, date_str)
#                 if key not in data_dict:
#                     data_dict[key] = {
#                         'Numele': name_str,
#                         'Data': date_str,
#                         'Ora intrare': ora_intrare,
#                         'Ora iesire': ora_iesire,
#                         'Masina': masina,
#                         'Locatii': locatii
#                     }
#                 else:
#                     if ora_intrare:
#                         data_dict[key]['Ora intrare'] = ora_intrare
#                     if ora_iesire:
#                         data_dict[key]['Ora iesire'] = ora_iesire
#                     if masina:
#                         data_dict[key]['Masina'] = masina
#                     if locatii:
#                         data_dict[key]['Locatii'] = locatii
        
#         # Start a new message
#         current_message = line.strip()
#         current_date_str = line.split(',')[0].strip()
#         current_date = datetime.strptime(current_date_str, "%d.%m.%Y").date()
#     else:
#         # If no timestamp, append to current message
#         current_message += " " + line.strip()

# # Process the very last message in the file after the loop ends
# if current_message and current_date in last_15_dates:
#     match = message_pattern.match(current_message)
#     if match:
#         date_str, time_str, message_content = match.groups()
#         # ... (rest of the parsing logic for the final message) ...
#         name_end_index = message_content.find(":")
#         if name_end_index != -1:
#             name_str = message_content[:name_end_index].strip()
#             message_body = message_content[name_end_index+1:].strip()
#         else:
#             name_str = "Unknown"
#             message_body = message_content.strip()

#         ora_intrare = None
#         if start_keywords.search(message_body):
#             ora_intrare = time_str
        
#         ora_iesire = None
#         if end_keywords.search(message_body):
#             ora_iesire = time_str

#         masina = None
#         body_without_keywords = start_keywords.sub('', message_body)
#         body_without_keywords = end_keywords.sub('', body_without_keywords)
        
#         masina_found = False
#         for m in vehicle_pattern.finditer(body_without_keywords):
#             found_vehicle = m.group(0).strip()
#             if 'personal' in found_vehicle.lower():
#                 try:
#                     words = message_body.split()
#                     personal_word_index = words.index(found_vehicle)
#                     if personal_word_index + 1 < len(words):
#                         masina = f"{found_vehicle} {words[personal_word_index + 1]}"
#                     else:
#                         masina = found_vehicle
#                     masina_found = True
#                     break
#                 except (ValueError, IndexError):
#                     pass
            
#             if masina is None:
#                 masina = found_vehicle
#                 masina_found = True
#                 break

#         locatii = message_body
#         locatii = start_keywords.sub('', locatii)
#         locatii = end_keywords.sub('', locatii)
        
#         if masina_found and masina is not None:
#             locatii = locatii.replace(masina, '').strip()
        
#         locatii = re.sub(r'^\s*[-,\s:]+', '', locatii).strip()
#         locatii = re.sub(r'[-,\s:]+$', '', locatii).strip()
#         if not locatii:
#             locatii = None

#         key = (name_str, date_str)
#         if key not in data_dict:
#             data_dict[key] = {
#                 'Numele': name_str,
#                 'Data': date_str,
#                 'Ora intrare': ora_intrare,
#                 'Ora iesire': ora_iesire,
#                 'Masina': masina,
#                 'Locatii': locatii
#             }
#         else:
#             if ora_intrare:
#                 data_dict[key]['Ora intrare'] = ora_intrare
#             if ora_iesire:
#                 data_dict[key]['Ora iesire'] = ora_iesire
#             if masina:
#                 data_dict[key]['Masina'] = masina
#             if locatii:
#                 data_dict[key]['Locatii'] = locatii



# %%
# # Process the very last message in the file after the loop ends
# if current_message and current_date_in_loop in date_range:
#     match = message_pattern.match(current_message)
#     if match:
#         date_str, time_str, message_content = match.groups()
        
#         name_end_index = message_content.find(":")
#         if name_end_index != -1:
#             name_str = message_content[:name_end_index].strip()
#             message_body = message_content[name_end_index+1:].strip()
#         else:
#             name_str = "Unknown"
#             message_body = message_content.strip()

#         ora_intrare = None
#         if start_keywords.search(message_body):
#             ora_intrare = time_str
        
#         ora_iesire = None
#         if end_keywords.search(message_body):
#             ora_iesire = time_str

#         # masina = None
#         # body_without_keywords = start_keywords.sub('', message_body)
#         # body_without_keywords = end_keywords.sub('', body_without_keywords)
        
#         # masina_found = False
#         # for m in vehicle_pattern.finditer(body_without_keywords):
#         #     found_vehicle = m.group(0).strip()
#         #     if 'personal' in found_vehicle.lower():
#         #         try:
#         #             words = message_body.split()
#         #             personal_word_index = words.index(found_vehicle)
#         #             if personal_word_index + 1 < len(words):
#         #                 masina = f"{found_vehicle} {words[personal_word_index + 1]}"
#         #             else:
#         #                 masina = found_vehicle
#         #             masina_found = True
#         #             break
#         #         except (ValueError, IndexError):
#         #             pass
            
#         #     if masina is None:
#         #         masina = found_vehicle
#         #         masina_found = True
#         #         break

#         # locatii = message_body
#         # locatii = start_keywords.sub('', locatii)
#         # locatii = end_keywords.sub('', locatii)
        
#         # if masina_found and masina is not None:
#         #     locatii = locatii.replace(masina, '').strip()
        
#         # locatii = re.sub(r'^\s*[-,\s:]+', '', locatii).strip()
#         # locatii = re.sub(r'[-,\s:]+$', '', locatii).strip()
#         # if not locatii:
#         #     locatii = None
#         # Extract all vehicles and locations
#         masina_list = []
#         masina_text = ""

#         # Remove keywords before looking for Masina, to prevent false positives
#         body_without_keywords = start_keywords.sub('', message_body)
#         body_without_keywords = end_keywords.sub('', body_without_keywords)
#         body_without_keywords = body_without_keywords.strip('- ')

#         # Find all vehicles in the message body
#         for m in vehicle_pattern.finditer(body_without_keywords):
#             found_vehicle = m.group(0).strip()
            
#             # Handle special case for 'Personala' or 'Personală'
#             if 'personal' in found_vehicle.lower():
#                 try:
#                     words = message_body.split()
#                     # Find the index of the matched 'Personal' vehicle
#                     personal_word_index = -1
#                     for i, word in enumerate(words):
#                         if re.search(r'Personal(a|ă)', word, re.IGNORECASE):
#                             personal_word_index = i
#                             break
                    
#                     # Check for word after "Personala"
#                     if personal_word_index + 1 < len(words):
#                         masina_text = f"{found_vehicle} {words[personal_word_index + 1]}"
#                     else:
#                         masina_text = found_vehicle
#                 except (ValueError, IndexError):
#                     masina_text = found_vehicle
#             else:
#                 masina_text = found_vehicle
            
#             masina_list.append(masina_text.strip())

#             # The 'Masina' field should be a comma-separated string of all found vehicles
#             masina = ', '.join(masina_list) if masina_list else None

#             # Extract Locatii by starting with the original message body
#             locatii = message_body.strip()
#             locatii = start_keywords.sub('', locatii)
#             locatii = end_keywords.sub('', locatii)

#             # Remove all found vehicle texts from the Locatii string
#             if masina_list:
#                 for found_vehicle_text in masina_list:
#                     locatii = locatii.replace(found_vehicle_text, '').strip()

#             # Clean up remaining text in Locatii
#             locatii = re.sub(r'^\s*[-,\s:]+', '', locatii).strip()
#             locatii = re.sub(r'[-,\s:]+$', '', locatii).strip()
#             if not locatii:
#                 locatii = None

#         key = (name_str, date_str)
#         if key not in data_dict:
#             data_dict[key] = {
#                 'Numele': name_str,
#                 'Data': date_str,
#                 'Ora intrare': ora_intrare,
#                 'Ora iesire': ora_iesire,
#                 'Masina': masina,
#                 'Locatii': locatii
#             }
#         else:
#             if ora_intrare:
#                 data_dict[key]['Ora intrare'] = ora_intrare
#             if ora_iesire:
#                 data_dict[key]['Ora iesire'] = ora_iesire
#             if masina:
#                 data_dict[key]['Masina'] = masina
#             if locatii:
#                 data_dict[key]['Locatii'] = locatii

# %%
# # --- Part 3: Convert to DataFrame and finalize calculations ---
# if data_dict:
#     final_df = pd.DataFrame(list(data_dict.values()))
    
#     final_df['Data'] = pd.to_datetime(final_df['Data'], format='%d.%m.%Y')
#     final_df['Entry_Time_DT'] = pd.to_datetime(final_df['Ora intrare'], format='%H:%M', errors='coerce')
#     final_df['Exit_Time_DT'] = pd.to_datetime(final_df['Ora iesire'], format='%H:%M', errors='coerce')
    
#     final_df['Timp total de lucru'] = (final_df['Exit_Time_DT'] - final_df['Entry_Time_DT']).dt.total_seconds() / 3600
#     final_df['Timp total de lucru'] = final_df['Timp total de lucru'].round(2)
    
#     final_df = final_df[['Numele', 'Data', 'Ora intrare', 'Ora iesire', 'Masina', 'Locatii', 'Timp total de lucru']]
#     final_df = final_df.sort_values(by='Data', ascending=False).reset_index(drop=True)
    
#     print("Final DataFrame with the last 15 dates:")
#     #print(final_df.to_string())
#     print(final_df.head(25))

# else:
#     print("No valid data was found for the last 15 dates.")

# %%
# --- Part 3: Convert to DataFrame and finalize calculations ---
if data_dict:
    final_df = pd.DataFrame(list(data_dict.values()))
    
    final_df['Data'] = pd.to_datetime(final_df['Data'], format='%d.%m.%Y')
    final_df['Entry_Time_DT'] = pd.to_datetime(final_df['Ora intrare'], format='%H:%M', errors='coerce')
    final_df['Exit_Time_DT'] = pd.to_datetime(final_df['Ora iesire'], format='%H:%M', errors='coerce')
    
    final_df['Timp total de lucru'] = (final_df['Exit_Time_DT'] - final_df['Entry_Time_DT']).dt.total_seconds() / 3600
    final_df['Timp total de lucru'] = final_df['Timp total de lucru'].round(2)
    
    final_df = final_df[['Numele', 'Data', 'Ora intrare', 'Ora iesire', 'Masina', 'Locatii', 'Timp total de lucru']]
    final_df = final_df.sort_values(by='Data', ascending=False).reset_index(drop=True)
    
    # Optional: Add your custom 'De verificat' column
    # final_df['De verificat'] = ''
    # final_df.loc[final_df['Ora intrare'].isnull(), 'De verificat'] = 'a'
    # final_df.loc[final_df['Ora iesire'].isnull(), 'De verificat'] = 'b'

    print("Final DataFrame with the specified date range:")
    #print(final_df.to_string())

else:
    print("No valid data was found for the specified date range.")

# %%
# if data_dict:
#     final_df = pd.DataFrame(list(data_dict.values()))
    
#     final_df['Data'] = pd.to_datetime(final_df['Data'], format='%d.%m.%Y')
#     final_df['Entry_Time_DT'] = pd.to_datetime(final_df['Ora intrare'], format='%H:%M', errors='coerce')
#     final_df['Exit_Time_DT'] = pd.to_datetime(final_df['Ora iesire'], format='%H:%M', errors='coerce')
    
#     final_df['Timp total de lucru'] = (final_df['Exit_Time_DT'] - final_df['Entry_Time_DT']).dt.total_seconds() / 3600
#     final_df['Timp total de lucru'] = final_df['Timp total de lucru'].round(2)
    
#     final_df = final_df[['Numele', 'Data', 'Ora intrare', 'Ora iesire', 'Masina', 'Locatii', 'Timp total de lucru']]
#     final_df = final_df.sort_values(by='Data', ascending=False).reset_index(drop=True)
    
#     # Optional: Add your custom 'De verificat' column
#     final_df['De verificat'] = ''
#     final_df.loc[final_df['Ora intrare'].isnull(), 'De verificat'] = 'a'
#     final_df.loc[final_df['Ora iesire'].isnull(), 'De verificat'] = 'b'

#     print("Final DataFrame with the specified date range:")
#     print(final_df.to_string())

# else:
#     print("No valid data was found for the specified date range.")

# %%
#final_df.tail(25)

# %%
#final_df.shape

# %%
# Create the new column and initialize it with an empty string
final_df['De verificat'] = ''

# Fill with 'a' where 'Ora intrare' is missing
final_df.loc[final_df['Ora intrare'].isnull(), 'De verificat'] = 'Ora inceput'

# Fill with 'b' where 'Ora iesire' is missing
final_df.loc[final_df['Ora iesire'].isnull(), 'De verificat'] = 'Ora sfarsit'
#final_df.tail(25)

# %%
# Aggregate the data to get the total and average work time for each person
agregat_df = final_df.groupby('Numele')['Timp total de lucru'].agg(
    total=('sum'), 
    average=('mean'),
    count=('count')
).reset_index()

# Rename the columns
agregat_df = agregat_df.rename(columns={
    'total': 'Total ore lucrate',
    'average': 'Ore pe zi (in medie)',
    'count': 'Zile lucrate'
})

# %%
#agregat_df

# %%
# Create the filename using the start and end dates
final_df['Data'] = final_df['Data'].dt.strftime('%d.%m.%Y')
excel_filename = f'pontaj {start_date_str} - {end_date_str}.xlsx'

# Save the DataFrame to the Excel file
# The 'index=False' argument prevents pandas from writing the DataFrame's index as a column
final_df.to_excel(excel_filename, index=False)

print(f"\nDataFrame successfully saved to '{excel_filename}'.")

# %%
# Create the filename using the start and end dates
excel_filename_stats = f'statistici pontaj {start_date_str} - {end_date_str}.xlsx'

# Save the DataFrame to the Excel file
# The 'index=False' argument prevents pandas from writing the DataFrame's index as a column
agregat_df.to_excel(excel_filename_stats, index=False)

print(f"\nDataFrame successfully saved to '{excel_filename_stats}'.")

# %%


# %%



