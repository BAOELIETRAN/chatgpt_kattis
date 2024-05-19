from openai import OpenAI
import os
import subprocess
# set api
client = OpenAI(api_key = "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")

# function to make a call to the api
def api_call(input):
    # make the question to input clear
    question = "Write a python program for this problem: " + input
    # make a call to gpt-4
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "user", "content": question}
      ]
    )
    # get and return the answer
    answer = completion.choices[0].message.content
    return answer

# get python portion of the string
def get_python(message):
    # find the start of the python program
    start_code_block = message.find("```python");
    cut_string = message[start_code_block+10:]
    # find the end of the python program
    end_code_block = cut_string.find("```")
    only_python = cut_string[:end_code_block-1]
    # return just python portion of message
    return only_python

dir_path = './auto_mining'  # starting dir
file_name = 'problem_text'  # file to find in each folder
output_file = 'output.py'  # file name for .py program
text_output_file = 'output_text.txt'  # full answer to be outputted if needed
i = 1  # temp variable to stop after 1

for folder_name in os.listdir(dir_path):
    if i > 1:
        break

    # get the folder path
    folder_path = os.path.join(dir_path, folder_name)

    # create a 'submissions' folder in each 'folder_name'
    submissions_folder = os.path.join(folder_path, 'submissions')
    os.makedirs(submissions_folder, exist_ok=True)

    # get the file path
    file_path = os.path.join(folder_path, file_name)

    # read the problem_text file in folder and save in content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # make api call and prints both full text and then just the python
    api_answer = api_call(content)

    # code to save .py to the 'submissions' folder
    api_python = get_python(api_answer)
    output_path = os.path.join(submissions_folder, output_file)
    with open(output_path, 'w') as file:
        file.write(api_python)

    # code to save the full response to the 'submissions' folder
    text_output_path = os.path.join(submissions_folder, text_output_file)
    with open(text_output_path, 'w') as file:
        file.write(api_answer)

    #auto_submit the python file:
    output = subprocess.run(["python", "submit.py", "-p", folder_name, "-f", output_file], capture_output=True, shell = True)
    print(output.stdout)

    i = i + 1