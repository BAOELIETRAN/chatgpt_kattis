import random
import re
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import html
from autokattis import Kattis
import time
import os
import io
import pandas as pd

# Change directory
# os.chdir(r'./auto_mining')

# Get the current working directory
current_directory = os.getcwd()

os.chdir('./auto_mining')

# Specify the 'kattis_webpages' folder as relative to the current directory
base_folder = os.path.join(current_directory, 'kattis_webpages')

kt = Kattis('baongo', '123456Baodeptrai@')

result = []

for index in range(1, 2):
    # Construct the full path to the HTML file
    file_path = os.path.join(base_folder, f"{index}.txt")

    # Read the HTML code from the file
    with open(file_path, 'r', encoding='utf-16') as file:
        html_code = file.read()

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(html_code, "lxml")

    all_kattis_problem = soup.find_all('table', {'class': 'table2'})
    for item in all_kattis_problem:
        if tbody := item.find("tbody"):
            for row in tbody.find_all("tr"):
                # Create new dict
                dict = {}

                a_tag = row.find("a")
                # Find the first <span> tag within the row
                first_span = row.find("span")

                # Find the next sibling of the first <span> tag
                diff_rank = first_span.find_next_sibling(text=True).strip() if first_span else "N/A"
                title = html.unescape(a_tag.text)
                id = a_tag['href']
                url = "https://open.kattis.com" + id

                try:
                    problem = kt.problem(id[10::])
                    df = pd.DataFrame(problem)
                    dict["Title"] = title
                    dict["ID"] = id[10::]
                    dict["URL"] = url
                    dict["Full Text"] = df.loc[0,"text"]
                    dict["Difficulty Score"] = df.loc[0,"difficulty"]
                    dict["Difficulty Rank"] = diff_rank
                    result.append(dict)

                    # Create folder if not exists
                    sanitized_title = id[10::]
                    folder_path = os.path.join(os.getcwd(), sanitized_title)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    text_content = df.loc[0, "text"]

                    # Use io.StringIO to create a file-like object
                    text_file_like = io.StringIO(text_content)

                    # Read lines from the file-like object
                    lines = text_file_like.readlines()

                    index_of_input = lines.index('Input\n')
                    index_of_sample_input = lines.index('Sample Input 1\n')
                    
                    text_lines = lines[:index_of_input - 1]
                    input_lines = lines[index_of_input : index_of_sample_input - 1]
                    sample_input_lines = lines[index_of_sample_input::]

                    # Create text file
                    file_path = os.path.join(folder_path, f"Full_Text.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write("Solve the following problem with the sample inputs and ouputs\n")
                        for line in text_lines:
                            file.write(line.strip() + '\n')

                    # Create input file
                    file_path = os.path.join(folder_path, f"Input.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        for line in input_lines:
                            file.write(line.strip() + '\n')

                    # Create sample_input file
                    file_path = os.path.join(folder_path, f"Sample_Input.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        for line in sample_input_lines:
                            file.write(line.strip() + '\n')

                    # Create ID file
                    file_path = os.path.join(folder_path, f"ID.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(id[10::])

                    # Create url file
                    file_path = os.path.join(folder_path, f"URL.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(url)

                    # Create difficulty score file
                    file_path = os.path.join(folder_path, f"Difficulty_Score.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(str(df.loc[0,"difficulty"]))

                    # Create difficulty rank file
                    file_path = os.path.join(folder_path, f"Difficulty_Rank.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(diff_rank)
                    
                    print(f"Created folder and text file for {title}")
                except ValueError as e:
                    print(f"An error occurred for problem {id[10::]}: {e}")
                    print('=============================')
                    continue