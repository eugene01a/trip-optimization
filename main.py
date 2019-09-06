from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from lib import maps
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import gps
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup

global search_params
search_params = {'origin': '', 'end': '', 'tolerance': 0.0, 'query': {}}
global result_widgets
result_widgets= []


class ScreenManagement(ScreenManager):
    pass

class StartScreen(Screen):

    def on_press(self):
        print('button pressed')
        self.collect_input()
        self.parent.current = "result"

    def collect_input(self):
        print("collecting input")
        global search_params
        search_params = {'origin': self.ids.origin.text,
                         'end': self.ids.end.text,
                         'tolerance': self.ids.tolerance.value,
                         'query': {'keyword': self.ids.name.text} }

    def current_location(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except NotImplementedError:
            popup = Popup(title="GPS Error",
                    content=Label(text="GPS support is not active on your platform")
                    ).open()
            Clock.schedule_once(lambda d: popup.dismiss(), 3)

    @mainthread
    def on_location(self, **kwargs):
        print(kwargs)

class ResultScreen(Screen):
    def add_result_widget(self, widget):
        self.ids.results_box.add_widget(widget)
        global result_btns
        result_widgets.append(widget)

    def create_screen(self):
        results = self.collect_output()
        print('Done searching')
        self.display_output(results)

    def collect_output(self):
        print("collecting results for: ")
        print(search_params)
        if search_params['origin'] == u'' or search_params['end'] == u'' or search_params['tolerance'] < 0.0 or search_params['query'] == {}:
            pass
        else:
            try:
                self.origin = search_params['origin']
                self.end = search_params['end']
                self.tolerance = search_params['tolerance']
                self.query = search_params['query']
                print(self.query)
                return maps.filter_along_route(self.origin, self.end, self.tolerance, **self.query)
            except:
                error_label = Label(text="Error searching maps!")
                self.add_result_widget(error_label)
        return None

    def display_output(self, results):
        if results:
            for idx, result in enumerate(results):
                print(result)
                result_text = result['name'] + '\n' + result['vicinity'] + '\n' + result['new_distance']
                result_button = Button(text=result_text)
                self.add_result_widget(result_button)

            completed_label = Label(text="Search completed")
            self.add_result_widget(completed_label)
        else:
            no_results_label = Label(text="No Results")
            self.add_result_widget(no_results_label)

        return result_widgets



    def erase_screen(self):
        for wdgt in result_widgets:
            self.ids.results_box.remove_widget(wdgt)


class MyApp(App):
    def build(self):
        # Builder.load_file("my.kv")
        return ScreenManagement()


if __name__ == '__main__':
    MyApp().run()
