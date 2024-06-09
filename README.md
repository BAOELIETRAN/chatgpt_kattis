# Chat GpT Kattis

## Step 1: Collect all the Kattis problem in the Kattis website
- Run the webpagemining.ipynb file to collect all the HTML codes of each page in the "Problem" session.
- Run the mining_data.ipynb file to collect all the problems, the code will store all the problems and their
  metadata in the corresponding folders named after the problems' name in the auto_mining folder.

## Step 2: Generate solutions via ChatGPT API

- Access the framework folder, run the test.ipynb notebook to prompt the ChatGPT for the solution of each problem in each folder in the auto_mining folder.
The notebook will also submit the generated solution to the Kattis website and store the result from Kattis in each problem's folder.
- The framework will create 2 folders in each problem's folder in the auto_mining folder:
  - Submission: Store all the solution file got from ChatGPT under python format in each problem's folder.
  - Result: Store all the result received from Kattis under text format in each problem's folder.
