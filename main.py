from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Welcome to T.A DATA RECORDER", font_size=24)
        self.start_button = Button(text="Start", size_hint=(None, None), size=(200, 50))
        self.start_button.bind(on_press=self.switch_to_data_recorder)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.start_button)
        self.add_widget(self.layout)

    def switch_to_data_recorder(self, instance):
        self.manager.current = 'data_recorder'


class DataRecorderScreen(Screen):
    def __init__(self, **kwargs):
        super(DataRecorderScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        self.project_name_input = TextInput(hint_text='Project Name')
        
        self.backsight_label = Label(text='Enter Backsight:')
        self.backsight_input = TextInput()
        
        self.intermediate_label = Label(text='Enter Intermediate (comma-separated if multiple):')
        self.intermediate_input = TextInput()
        
        self.foresight_label = Label(text='Enter Foresight:')
        self.foresight_input = TextInput()
        
        self.distance_label = Label(text='Enter Distance:')
        self.distance_input = TextInput()
        
        self.comment_label = Label(text='Enter Comment:')
        self.comment_input = TextInput()
        
        self.save_button = Button(text='Save', size_hint=(None, None), size=(200, 50))
        self.save_button.bind(on_press=self.save_data)
        
        self.layout.add_widget(self.project_name_input)
        self.layout.add_widget(self.backsight_label)
        self.layout.add_widget(self.backsight_input)
        self.layout.add_widget(self.intermediate_label)
        self.layout.add_widget(self.intermediate_input)
        self.layout.add_widget(self.foresight_label)
        self.layout.add_widget(self.foresight_input)
        self.layout.add_widget(self.distance_label)
        self.layout.add_widget(self.distance_input)
        self.layout.add_widget(self.comment_label)
        self.layout.add_widget(self.comment_input)
        self.layout.add_widget(self.save_button)
        
        self.add_widget(self.layout)

    def save_data(self, instance):
        project_name = self.project_name_input.text
        backsight = self.backsight_input.text
        intermediate = self.intermediate_input.text
        foresight = self.foresight_input.text
        distance = self.distance_input.text
        comment = self.comment_input.text

        try:
            backsight = float(backsight)
            foresight = float(foresight)
        except ValueError:
            print("Backsight and Foresight must be numbers.")
            return

        rise = max(0, foresight - backsight)
        fall = max(0, backsight - foresight)
        
        if project_name and backsight and foresight and intermediate and distance and comment:
            self.manager.get_screen('data_display').table.add_row([backsight, intermediate, foresight, rise, fall, distance, comment])
            # Clear values except for project name
            self.backsight_input.text = ''
            self.intermediate_input.text = ''
            self.foresight_input.text = ''
            self.distance_input.text = ''
            self.comment_input.text = ''
            self.manager.current = 'data_display'
        else:
            print("Please fill all fields.")


class DataTable(GridLayout):
    def __init__(self, **kwargs):
        super(DataTable, self).__init__(**kwargs)
        self.cols = 7  # Number of columns
        self.spacing = 5
        self.padding = 5
        self.add_widget(Label(text='Backsight'))
        self.add_widget(Label(text='Intermediate'))
        self.add_widget(Label(text='Foresight'))
        self.add_widget(Label(text='Rise'))
        self.add_widget(Label(text='Fall'))
        self.add_widget(Label(text='Distance'))
        self.add_widget(Label(text='Comment'))
    
    def add_row(self, row_data):
        for item in row_data:
            self.add_widget(Label(text=str(item)))


class DataDisplayScreen(Screen):
    def __init__(self, **kwargs):
        super(DataDisplayScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.back_button = Button(text='Back to Data Recorder', size_hint=(None, None), size=(200, 50))
        self.back_button.bind(on_press=self.back_to_data_recorder)
        self.table = DataTable()
        self.layout.add_widget(self.table)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def back_to_data_recorder(self, instance):
        self.manager.current = 'data_recorder'


class DataRecorderApp(App):
    def build(self):
        self.icon = 'totalstation256.png'  # Change icon here
        self.sm = ScreenManager()
        self.sm.add_widget(WelcomeScreen(name='welcome'))
        self.sm.add_widget(DataRecorderScreen(name='data_recorder'))
        self.sm.add_widget(DataDisplayScreen(name='data_display'))
        return self.sm


if __name__ == '__main__':
    DataRecorderApp().run()







