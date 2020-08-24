from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current ="sign_up_screen"
    def login(self, uname, pword):
        with open("users.json") as file:
            users=json.load(file)
        if uname in users:
            if users[uname]['password']==pword:
                self.manager.current="login_screen_success"
            else:
                self.ids.login_wrong.text = "Incorrent Password"
        else:
            self.ids.login_wrong.text = "Incorrect Username"
    def forgotpass(self):
        self.manager.current = "forgot_password_screen"

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users=json.load(file)
        users[uname]={'username':uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction ="right"
        self.manager.current ="login_screen"

    def get_quote(self, feel):
        feel=feel.lower()
        available_feeling=glob.glob("quotes/*.txt")
        available_feeling=[Path(filename).stem for filename in available_feeling]
        if feel in available_feeling:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes=file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Quotes not available for this feeling"

class ForgotPasswordScreen(Screen):
    def resetpass(self, uname, passw, re_pass):
        if passw!=re_pass:
            self.ids.incorrect_pass.text = "The re-entered password doesn't match"
        else:
            with open("users.json") as file:
                users=json.load(file)
            if uname in users:
                if users[uname]['password']==passw:
                    self.ids.incorrect_pass.text = "Password doesn't need to be changed"
                else:
                    users[uname]['password']=passw
                    with open("users.json", 'w') as file:
                        json.dump(users, file)
            else:
                self.ids.incorrect_pass.text = "Check Username or Sign Up"
    def go_to_login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "login_screen"

    def go_to_sign_up(self):
        self.manager.transition.direction ="right"
        self.manager.current ="sign_up_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image ):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__=="__main__":
    MainApp().run()
