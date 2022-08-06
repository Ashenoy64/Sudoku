from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse,Color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
import sudoku
from numpy import array
from kivy.uix.popup import Popup
class show_popup():
    pass
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

    def enable_button(self):
        for i in range(9):
            self.l[i].disabled=False




class Window(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=3
        self.rect=[]
        self.grid=[]
        self.diff=2
        self.pos_hint={"x":.25,"y":0.25}
        self.size_hint=(0.5,0.5)
        self.create_grid()
        for i in range(9):
            self.grid[i].bind(pos=self.update)
            self.grid[i].bind(size=self.update)


    def update(self,*args):
        for i in range(9):
            self.rect[i].pos=self.grid[i].pos
            self.rect[i].size=self.grid[i].size

    def check_ans(self,button):
        flag=1
        self.update_ans()
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
            self.parent.show_status("Congratulations You Completed the grid")
        else:
            print("Please Check Your Answer Again")
    def update_ans(self):
        for i in range(9):
            for j in range(9):
                self.ans[i,j]=int(self.button_value(i,j))


    def button_value(self,row,col):
        block_no=(row//3)*3+col//3
        grid_no=3*(row%3)+col%3
        return self.grid[block_no].l[grid_no].text

    def generate_hint(self):
        self.update_ans()
        sudoku.l2=self.ans.copy()
        if sudoku.solve(sudoku.l2):
            print("You Have Done Something Wrong")
            return
        else:
            self.sol=sudoku.l2.copy()
        i=0
        j=0
        while True:
            if self.ans[i,j]==0:
                return self.row_col(i,j,self.sol[i,j],self.assign)
            if j<9:
                j=j+1
            else:
                j=0
                i=i+1
            if i==8 and j==8:
                break
        print("No Spaces Left")    
            
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
    def assign(self,block_no,grid_no,ele):
        
        self.grid[block_no].l[grid_no].text=str(ele)
        
        if ele!=0:
            self.grid[block_no].l[grid_no].disabled=True
        else:
            self.grid[block_no].l[grid_no].disabled=False

    def row_col(self,row,col,ele,fxn):
        block_no=(row//3)*3+col//3
        grid_no=3*(row%3)+col%3
        fxn(block_no,grid_no,ele)

    def create_solvable(self):
        self.sol=sudoku.l2.copy()
        sudoku.generate(self.sol)
        self.ans=self.sol.copy()
        sudoku.generate_solvable(self.ans,self.diff)
        for i in range(9):
            for j in range(9):
                self.row_col(i,j,self.ans[i,j],self.assign)

    def submit(self):
        self.check_ans()        
class Top(BoxLayout):
    obj=Window()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box=BoxLayout()
        self.orientation="vertical"
        self.box.size_hint=(1,.05)
        self.add_widget(self.box)
        self.add_widget(self.obj)
        self.btn=Button(text="Submit",on_press=self.obj.check_ans,disabled=True)
        self.box.add_widget(self.btn)
        self.box.add_widget(Button(text="Difficulty:{}".format(self.obj.diff),on_press=self.set_difficulty))
        self.box.add_widget(Button(text="Create Game",on_press=self.create_game))
    def set_difficulty(self,button):
        if self.obj.diff==3:
            self.obj.diff=1
        else:
            self.obj.diff+=1
        button.text="Difficulty:{}".format(self.obj.diff)
    def create_game(self,button):
        self.btn.disabled=False
        self.obj.create_solvable()
    def correct(self,context):
        pop=Popup(title="Status",context=context)
        pop.open()

class ExampleApp(App):
    obj=Top()
    def build(self):
        return self.obj


app=ExampleApp()
app.run()
