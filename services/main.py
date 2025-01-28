import os
import csv
from groq import Groq

# read feedback from the CSV file
def read_feedback_from_csv(file_path):
    feedback_list = [] # empty list that will store the feedback from the CSV
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the header
        for row in reader:
            # assuming feedback is in the first column**
            # add feedback to the list
            feedback_list.append(row[0])  
    return feedback_list

# TODO **once the format of the CSV is established, this function 
# will likely need to be rewritten to properly access the feedback column

# Summarize Feedback function
def summarize_feedback():
    print("Initializing Groq client...")
    groq_client = Groq(api_key=os.environ['GROQ_API_KEY'])

    # read feedback from CSV
    file_path = './csv_files/test_student_feedback.csv'
    feedback_list = read_feedback_from_csv(file_path)

    print("Calling chat completion...")

    # send feedback to Groq for summarization
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are an assistant who needs to help a teacher summarize feedback from students.
                Your response should be a few sentences long including any frequently asked questions.
                If there are no questions from the students, mention that. 
                This is a Software Development class and you should not ask any questions about the student feedback."""
            },
            {
                "role": "user",
                "content": "\n".join(feedback_list)  # sending all feedback as a single message to Groq
            }
        ],
        model="llama3-8b-8192"
    )

    # extract content from Groq's first response and store in response variable
    response = chat_completion.choices[0].message.content

    # print Groq's response
    print(response)

# Run the summarization
summarize_feedback()
