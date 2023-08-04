import sudoku
from kivy.app import App
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout


#Each 3x3 grid
class Box(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=3
        self.l=[]
        self.create_box()
        
    def create_box(self):
        for i in range(9):
            self.l.append(Button(text="0",background_disabled_normal="",background_color=(1,1,1,0.2),disabled_color=(1,1,1,1),pos=self.pos,size=self.size,on_press=self.increment))
            self.add_widget(self.l[i])

    def increment(self,button):
        n=int(button.text)
        if n<9:
            n+=1
        else:
            n=0
        button.text=str(n)

    def disable_buttons(self):
        for i in range(9):
            self.l[i].disabled=True

    def enable_buttons(self):
        for i in range(9):
            self.l[i].disabled=False


#Sudoku grid
class Grid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=3
        self.rect=[]
        self.grid=[]
        self.difficulty=2

        self.pos_hint={"x":.25,"y":0.25}
        self.size_hint=(0.5,0.5)

        self.create_grid()

        for i in range(9):
            self.grid[i].bind(pos=self.update)
            self.grid[i].bind(size=self.update)


    def create_grid(self):
        for i in range(9):
            self.grid.append(Box())
            with self.grid[i].canvas.before:
                if i%2==0:
                    Color(0.5,0.5,0.1)
                else:
                    Color(0.1,0.6,0.2)

                self.rect.append(Rectangle(size=self.grid[i].size,pos=self.grid[i].pos))

            self.add_widget(self.grid[i])


    def update(self,*args):
        for i in range(9):
            self.rect[i].pos=self.grid[i].pos
            self.rect[i].size=self.grid[i].size

    #checks if answer submitted correct
    def check_answer(self,button):
        flag=1
        self.update_answer()
        for i in range(9):
            s1=set(self.ans[i,:])
            l1=len(s1)
            s2=set(self.ans[:,i])
            l2=len(s2)
            s3=self.ans[(i//3)*3:(i//3+1)*3,(i%3)*3:(i%3+1)*3].copy()
            s3=set(s3.flatten())
            l3=len(s3)
            if l1!=9 or 0 in s1 or l2!=9 or 0 in s2 or l3!=9 or 0 in s3 :
                flag=0
                break
        if flag:
            self.parent.show_status(text="Congratulations You Completed the grid")
        else:
            self.parent.show_status(text="Please Check You answer")
        
    #Updating answer matrix
    def update_answer(self):
        for i in range(9):
            for j in range(9):
                self.ans[i,j]=int(self.get_button_value(i,j))

    #get button value
    def get_button_value(self,row,col):
        block_no=(row//3)*3+col//3
        grid_no=3*(row%3)+col%3
        return self.grid[block_no].l[grid_no].text

    def generate_hint(self):
        self.update_answer()
        sudoku.l2=self.ans.copy()
        if sudoku.solve(sudoku.l2):
            return
        else:
            self.sol=sudoku.l2.copy()
        i=0
        j=0
        while True:
            if self.ans[i,j]==0:
                return self.row_col(i,j,self.sol[i,j])
            if j<9:
                j=j+1
            else:
                j=0
                i=i+1
            if i==8 and j==8:
                break
            
    
    #assign value to button
    def assign_value(self,block_no,grid_no,ele):
        self.grid[block_no].l[grid_no].text=str(ele)
        if ele!=0:
            self.grid[block_no].l[grid_no].disabled=True
        else:
            self.grid[block_no].l[grid_no].disabled=False

    #convert row col to block number and grid
    def row_col(self,row,col,ele):
        block_no=(row//3)*3+col//3
        grid_no=3*(row%3)+col%3
        self.assign_value(block_no,grid_no,ele)

    def create_solvable(self):
        self.sol=sudoku.l2.copy()
        sudoku.generate(self.sol)
        self.ans=self.sol.copy()
        sudoku.generate_solvable(self.ans,self.difficulty)
        for i in range(9):
            for j in range(9):
                self.row_col(i,j,self.ans[i,j])


#Main toplevel window
class Top(BoxLayout):
    grid=Grid()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box=BoxLayout()
        self.orientation="vertical"
        self.box.size_hint=(1,.05)

        self.add_widget(self.box)
        self.add_widget(self.grid)

        self.submit_button=Button(text="Submit",on_press=self.grid.check_answer,disabled=True)
        self.box.add_widget(self.submit_button)
        self.box.add_widget(Button(text="Difficulty:{}".format(self.grid.difficulty),on_press=self.set_difficulty))
        self.box.add_widget(Button(text="Create Game",on_press=self.create_game))

    def set_difficulty(self,button):
        if self.grid.difficulty==3:
            self.grid.difficulty=1
        else:
            self.grid.difficulty+=1
        button.text="Difficulty:{}".format(self.grid.difficulty)

    def create_game(self,button):
        self.submit_button.disabled=False
        self.grid.create_solvable()

    def show_status(self,text):
        context=GridLayout(cols=1,padding=10)
        popup_label=Label(text=text)
        popup_close_button=Button(text="Close")
        
        context.add_widget(popup_label)
        context.add_widget(popup_close_button)
        
        popup=Popup(title="Status",content=context,size_hint=(None, None), size=(200, 200))
        popup.open()
        popup_close_button.bind(on_press=popup.dismiss)

class App(App):

    def build(self):
        return Top()


App().run()
