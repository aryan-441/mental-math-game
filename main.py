'''Mental Math Game'''
from tkinter import *
import time
import random
import json

BG_COLOUR = '#B1DDC6'
TITLE = ("Ariel", 40, 'italic')
ANSWER_OR_QUESTION = ("Ariel", 60, 'bold')

try:
    with open('results.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = {
        'high_score': 0
    }

def generate_question():
    operation = random.choice(['+', '-', '*', 'clean_division', 'decimal_division'])
    if operation == '+':
        num1 = random.randint(10,1000)
        num2 = random.randint(10,1000)
        ans = num1 + num2
    elif operation == '-':
        num1 = random.randint(10,1000)
        num2 = random.randint(10,num1)
        ans = num1 - num2
    elif operation == '*':
        num1 = random.randint(1,100)
        num2 = random.randint(1,100)
        ans = num1*num2
    elif operation == 'clean_division':
        num2 = random.randint(2, 100)
        ans = random.randint(2, 100)
        num1 = num2 * ans

    elif operation == 'decimal_division':
        num1 = random.randint(10, 100)
        num2 = random.randint(2, 20)
        ans = int(num1 / num2 * 10) / 10  # to get 1 decimal place instead of 1 ROUNDED decimal place
    else:
        raise ValueError('Improper input.')
    symbols = {
    '+': '+',
    '-': '−',
    '*': '×',
    'decimal_division': '÷',
    'clean_division': '÷'
}
    question = f"{num1} {symbols[operation]} {num2}"
    return question, ans

'''for i in range(10):
    question, answer = generate_question()
    print(question, "=", answer)'''

def check_answer():
    user_answer = answer_entry.get()

    try:
        return float(user_answer) == answer
    except ValueError:
        return False

question, answer = generate_question()

q_no = 0
question_start_time = time.time()
#session_start_time = 0
question_times = []
correct = 0
wrong = 0

def submit_answer():
    global correct, wrong
    question_time = time.time() - question_start_time
    question_times.append(question_time)
    if check_answer():
        correct += 1
        #print("Correct")
        canvas.itemconfig(card_background,image=card_back_img)
        canvas.itemconfig(feedback, image=tick_image, state='normal')
        #canvas.itemconfig(card_title, text='Correct', fill='black')
        canvas.itemconfig(card_word, text=answer, fill='black')
    else:
        wrong += 1
        #print("Wrong!")
        canvas.itemconfig(card_background, image=card_back_img)
        canvas.itemconfig(feedback, image=cross_image, state='normal')
        #canvas.itemconfig(card_title='Wrong!', fill='black')
        canvas.itemconfig(card_word, text=answer,fill='black')
    window.after(3000, next_card)

def next_card():
    global question, answer, q_no, question_start_time
    question, answer = generate_question()
    q_no +=1
    question_start_time = time.time()
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(feedback, state='hidden')
    canvas.itemconfig(card_title, text=f'Question {q_no}', fill='black')
    canvas.itemconfig(card_word, text=question, fill='black')
    answer_entry.delete(0,END)

def end_session():
    total_questions = correct + wrong
    total_time = sum(question_times)
    if total_questions > 0:
        avg_time = total_time / total_questions
        accuracy = (correct/total_questions) * 100
        performance_score = (correct / total_time) * 1000
    else:
        avg_time = 0
        accuracy = 0
        performance_score = 0
    if performance_score > data['high_score']:
        data['high_score'] = performance_score

        with open('results.json', 'w') as file:
            json.dump(data, file, indent=4)

    main_frame.grid_remove()
    results_frame = Frame(window, bg=BG_COLOUR)
    results_frame.grid(row=0,column=0)
    Label(results_frame, text='SESSION COMPLETE', font=('Arial',40,'bold'), bg=BG_COLOUR).grid(row=0,columnspan=2, pady=30)
    Label(results_frame, text=f'Total Questions: {total_questions}',font=('Arial', 22),bg=BG_COLOUR).grid(row=1, column=0, columnspan=2, pady=10)
    Label(results_frame, text=f'Correct: {correct}', font=('Arial', 22), bg=BG_COLOUR).grid(row=2, column=0, columnspan=2, pady=10)

    Label(results_frame, text=f'Wrong: {wrong}', font=('Arial', 22), bg=BG_COLOUR).grid(row=3, column=0, columnspan=2, pady=10)

    Label(results_frame, text=f'Accuracy: {accuracy:.1f}%', font=('Arial', 22), bg=BG_COLOUR).grid(row=4, column=0, columnspan=2, pady=10)

    Label(results_frame, text=f'Total Time: {total_time:.1f} seconds', font=('Arial', 22), bg=BG_COLOUR).grid(row=5, column=0, columnspan=2, pady=10)

    Label(results_frame, text=f'Average Time: {avg_time:.1f} seconds/question', font=('Arial', 22), bg=BG_COLOUR).grid(row=6, column=0, columnspan=2, pady=10)  
    Label(results_frame, text=f'Performance Score: {performance_score:.1f}', font=('Arial', 22, 'bold'), bg=BG_COLOUR).grid(row=7, column=0, columnspan=2, pady=10)

    Label(results_frame, text=f'Highest Score: {data["high_score"]:.1f}', font=('Arial', 22, 'bold'), bg=BG_COLOUR).grid(row=8, column=0, columnspan=2, pady=10)

    
window = Tk()
window.title('Mental Math')
window.config(padx=50,pady=50,bg=BG_COLOUR)
window.state('zoomed')

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

main_frame = Frame(window, bg=BG_COLOUR, padx=50, pady=50)
main_frame.grid(row=0, column=0)

canvas = Canvas(main_frame,width=800, height=526, bg=BG_COLOUR, highlightthickness=0)

card_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
card_background = canvas.create_image(400, 263, image=card_img)
card_title = canvas.create_text(400, 150, text='', font=TITLE)
card_word = canvas.create_text(400, 263, text='', font=ANSWER_OR_QUESTION)
canvas.grid(row=0, column=0, columnspan=2)
answer_entry = Entry(main_frame, width=20, font=('Arial',25))
answer_entry.grid(row=1, column=0, columnspan=2, pady=20)
answer_entry.bind('<Return>', lambda event: submit_answer())
end_button = Button(main_frame, text='End Session', command=end_session, font=('Arial', 18))
end_button.grid(row=2, column=0, columnspan=2, pady=0)
#canvas.bind("<Button-1>", flip_card)

cross_image = PhotoImage(file='images/wrong.png')


tick_image = PhotoImage(file='images/right.png')
feedback=canvas.create_image(650,150,image=tick_image, state='hidden')


next_card()

window.mainloop()