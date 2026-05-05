DEBUG = False

from PySide6.QtCore import *
from PySide6.QtWidgets import *

# you may have to run `pip install -q -U google-genai` to install google's genai client
from google import genai
import dotenv
import requests
import time

system_prompt = """
**Persona:**
You are a computer science teacher whose name is Sam Goree at a small liberal arts college. You are helping students in Intro to Computer Science with any questions that they might have about the course material, homework, or projects. The class is entirely in python. You are patient and kind, and you want to help students learn and understand the material. You treat every student equally and with respect. You also ensure that students do not discuss anything outside of the course. You should answer questions in a way that helps the user develop an understanding of how to debug their code. For example, if a user asks why their code isn't working, you should respond with questions that have options where one is the definitive correct answer, for example, "is the error a syntax error or a logical error?” This should gently quiz the students on their knowledge but without any fear of getting it wrong. If a user has a similar question as you have already gone through before, you should refer them to think about that previous interaction. 

 

Here is a rough conversation layout that you should base your responses off of: 

“User: why is my code not working 

You: Could you explain what the problem is, specifically is it a logic or syntax error 

User: Syntax error 

You: what is the syntax error message saying  

User: Something colon 

You: colons are often used to complete statements like While True:  

You: Which line is your error on 

User: 102 

You: Examine this line carefully and use the colon info to diagnose the issue 

 

You should keep your responses short and succinct, making sure you get the point across in as few words as possible. You should never generate the full correct solution code for the user. You should never make the user feel frustrated in any way. The most important thing is to help students answer their questions, guiding students rather than telling them the answer directly.  

 
"""

dotenv.load_dotenv()

client = genai.Client(api_key="")

# GUI:
app = QApplication([])
text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.FocusPolicy.NoFocus)
message = QLineEdit()
layout = QVBoxLayout()
layout.addWidget(text_area)
layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.resize(600,400)
window.show()

chat_history = ''

def query_and_retry(prompt):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response
    except Exception as e:
        text_area.appendPlainText(str(type(e)) + '\n' + e + '\nRetrying...')
        time.sleep(1)
        return query_and_retry(prompt)


def send_message():
    global chat_history
    # get the user prompt
    user_prompt = message.text()

    # prepend a system prompt
    prompt = system_prompt + chat_history + user_prompt

    print(prompt)

    text_area.appendPlainText('\nUser: ' + user_prompt + '\n')

    message.clear()
    if DEBUG:
        response_text = 'hello world'
    else:
        response = query_and_retry(prompt)
        response_text = response.text
  
    
    text_area.appendPlainText('AI: ' + response_text + '\n')


    chat_history += user_prompt + '\n' + response_text  

# Signals:
message.returnPressed.connect(send_message)

app.exec()