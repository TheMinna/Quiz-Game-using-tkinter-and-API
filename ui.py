from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#438D83"
WRONG_ANSWER_COLOR = "#FFA9A9"
CORRECT_ANSWER_COLOR = "#AEFFA9"
FONT = ('Arial', 14, 'normal')

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Do you know?")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.score_label = Label(self.window, text='Score 0', font=FONT, fg='white', bg=THEME_COLOR)

        self.canvas = Canvas(bg='white', width=300, height=250)
        self.question_label = self.canvas.create_text(
            150, 
            125,
            width=280,
            text='Question here', 
            fill=THEME_COLOR, 
            font=FONT
            )
        
        button_true_image = PhotoImage(file='images/true.png') 
        button_false_image = PhotoImage(file='images/false.png') 
        self.button_true = Button(image=button_true_image, highlightthickness=0, command=self.click_true)
        self.button_false = Button(image=button_false_image, highlightthickness=0, command=self.click_false)

        self.score_label.grid(row=0, column=1)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)
        self.button_true.grid(row=2, column=0)
        self.button_false.grid(row=2, column=1)

        self.get_next_question()

        self.window.mainloop() 

    def click_true(self):
        if self.quiz.check_answer(user_answer="True"):
            self.quiz.score +=1
            self.score_label.config(text=f"Score {self.quiz.score}")
            self.screen_color_change('correct')
        else:
            self.screen_color_change('not_correct')
        if self.quiz.still_has_questions():
            self.canvas.after(200, self.get_next_question)
        else:
            self.no_more_questions()


    def click_false(self):
        if self.quiz.check_answer(user_answer="False"):
            self.quiz.score +=1
            self.score_label.config(text=f"Score {self.quiz.score}")
            self.screen_color_change('correct')
        else:
            self.screen_color_change('not_correct')
        if self.quiz.still_has_questions():
            self.canvas.after(200, self.get_next_question)
        else:
            self.no_more_questions()

    def screen_to_white(self):
        self.canvas.configure(bg='white')


    def screen_color_change(self, correct_or_not: str):
        self.correct_or_not = correct_or_not
        if self.correct_or_not == 'correct':
            self.canvas.configure(bg=WRONG_ANSWER_COLOR)
            self.canvas.after(200, self.screen_to_white)
            
        else:
            self.canvas.configure(bg=CORRECT_ANSWER_COLOR)
            self.canvas.after(200, self.screen_to_white)


    def no_more_questions(self):
        self.screen_to_white()
        self.button_true.config(state=DISABLED)
        self.button_false.config(state=DISABLED)
        self.button_false.destroy()
        self.button_true.destroy()

        if self.quiz.score == 10:
            end_text = "WOW!"
        elif self.quiz.score > 8:
            end_text = "Excellent!"
        elif self.quiz.score >= 6:
            end_text = "Well done!"
        elif self.quiz.score > 0:
            end_text = ""
        elif self.quiz.score == 0:
            end_text = "Ummm..."
        self.canvas.itemconfig(self.question_label, text=f"{end_text}\nYour final score: {self.quiz.score}", justify='center') 
        
        # self.button_again = Button(highlightthickness=0, text="Again", command=self.play_again)
        self.button_quit = Button(highlightthickness=0, text="Quit", command=self.quit_game, font=FONT, bg=CORRECT_ANSWER_COLOR)
        
        # self.button_again.grid(row=2, column=0)
        self.button_quit.grid(row=2, column=0, columnspan=2)       

    # def play_again(self):
    #     print("again")
    #     return True
        
    
    def quit_game(self):
        self.canvas.itemconfig(self.question_label, text="Thank you for playing!\n\nBye!", justify='center') 
        self.canvas.after(1000, self.destroy_window)
    
    def destroy_window(self):
        self.window.destroy()
    

    def get_next_question(self):
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_label, text=q_text)