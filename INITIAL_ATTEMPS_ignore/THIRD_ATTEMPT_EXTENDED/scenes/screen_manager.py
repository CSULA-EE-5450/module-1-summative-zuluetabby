import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.9.0')

Builder.load_string(""" 
<PlayerInput>:
    multiline: False
    padding_x: 0
    background_normal: ''
    background_color: 0, 0, 0, 0
    cursor_color: (1, 1, 1, 1)
    canvas.before:
        Color:
            rgb: (.9, .9, .9)
        Rectangle:
            size: self.size[0], 1
            pos: self.pos[0], self.pos[1] + 7

<StyledButton>:
    background_normal: 'icons/button.jpg'
    background_down: self.background_normal
    background_disabled_normal: 'icons/button_disabled.png'
    opacity: 0.9
    on_press:
        self.background_active = self.background_normal
        self.opacity = 1
    on_release:
        self.opacity = 0.9

<Label>:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.4

        Rectangle:
            pos:
                int(self.center_x - self.texture_size[0] / 2.) + 1,\
                int(self.center_y - self.texture_size[1] / 2.) + 1

            size: root.texture_size
            texture: root.texture


<MainMenuButton@StyledButton>:
    background_color: 0, 0, 0, 0
    font_size: 32
    color: 0, 0, 0, 1
    on_press:
        self.bold = True
    on_release:
        self.bold = False

<ScreenOne>: 
    name: 'main'

    Image:
        source: 'icons/title_screen.jpg'
        allow_stretch: True
        keep_ratio: False
        keep_data: True

    FloatLayout:

        Image:
            source: 'icons/logo.png'
            size_hint_y: None
            center_y: root.height - 70

        BoxLayout:
            orientation: 'vertical'
            size_hint: 0.5, None
            size: 0, root.height - 200
            pos_hint: {'center_x': .5, 'center_y': .4}
            canvas.before:
                Color:
                    rgb: (20.0/255, 20.0/255, 28.0/255)
                Rectangle:
                    size: self.size[0], 3
                    pos: self.pos[0], 30
            canvas.after:
                Color:
                    rgb: (20.0/255, 20.0/255, 28.0/255)
                Rectangle:
                    size: self.size[0], 3
                    pos: self.pos[0], self.pos[1] + self.size[1] + 20

            Button:
                text: 'Alone'

            Button:
                text: 'Player versus Player'

            Button:
                text: 'Online'

            Button:
                text: 'Quit'



<ShipSizeButton>:
    size_hint: None, None
    size: 60, 60

<ShipCell@Button>:
    name: 'ship_cell'
    background_color: .3, .3, .3, .7
    background_normal: 'icons/cell.png'
    
<ScreenTwo>: 
    name: 'ship_selection'
    ship_grid: grid
    top_pane: pane
    start_button: start
    player_input: name

    AsyncImage:
        source: 'icons/screen.jpg'
        allow_stretch: True
        keep_ratio: False
        keep_data: True

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .8

        FloatLayout:

            TextInput:
                id: name
                hint_text: 'Player name...'
                font_size: 30
                size_hint: None, None
                size: root.width * .6, 60
                center: root.width / 2, root.height * 0.9

            GridLayout:
                id: grid
                direction_button: direction
                size_button: ship4
                size: min(root.height * 0.7, root.width), min(root.height * 0.7, root.width)
                size_hint: None, None
                spacing: 2
                rows: 10
                cols: 10
                center: root.width / 2, root.height / 2

        FloatLayout:

            TabbedPanel:
                id: pane
                rows: 5
                cols: 1
                spacing: 2
                pos: root.width / 10, 0

                Button:
                    id: direction
                    background_normal: 'icons/button.jpg'
                    size_hint: None, None
                    size: 60, 60

                Button:
                    id: ship4
                    how_many: 1
                    ship_size: 4
                    text: 'IV'
                    background_color: (0, 229.0/255.0, 0, 1)

                Button:
                    how_many: 2
                    ship_size: 3
                    text: 'III'

                Button:
                    how_many: 3
                    ship_size: 2
                    text: 'II'
                    
                Button:
                    how_many: 4
                    ship_size: 1
                    text: 'I'

    BoxLayout:
        orientation: 'horizontal'

        Button:
            text: 'Main menu'
            size_hint: 0.4, None
            size: 0, 60
            on_press:
                app.screen_manager.current = 'main'

        Button:
            size_hint: 0.1, None
            size: 0, 60
            Image:
                source: 'icons/random.png'
                pos: self.parent.pos[0] + 10, self.parent.pos[1] + 10
                size: self.parent.size[0] - 20, self.parent.size[1] - 20

        Button:
            size_hint: 0.1, None
            size: 0, 60
            Image:
                source: 'icons/erase.png'
                pos: self.parent.pos[0] + 10, self.parent.pos[1] + 10
                size: self.parent.size[0] - 20, self.parent.size[1] - 20

        Button:
            id: start
            text: 'Play'
            size_hint: 0.4, None
            size: 0, 60
            disabled: True


<ConnectionLabel@Label>:
    font_size: 26
    size_hint: None, None
    size: root.width * .6, 30
    
<ScreenThree>: 
    name: 'multiplayer'
    error_message: error
    address_field: ip
    port_field: port

    AsyncImage:
        source: 'icons/screen.jpg'
        allow_stretch: True
        keep_ratio: False
        keep_data: True

    AnchorLayout:
        anchor_y: 'top'

        FloatLayout:

            Label:
                font_size: 26
                size_hint: None, None
                size: root.width * .6, 30
                text: 'IP address of server'
                center: root.width / 2, root.height - 30

            TextInput:
                id: ip
                text: '127.0.1.1'
                font_size: 24
                size_hint: None, None
                size: root.width * .6, 45
                center: root.width / 2, root.height - 70

            Label:
                text: 'Server port'
                center: root.width / 2, root.height - 130
                font_size: 26
                size_hint: None, None
                size: root.width * .6, 30

            TextInput:
                id: port
                text: '7777'
                font_size: 24
                size_hint: None, None
                size: root.width * .6, 45
                center: root.width / 2, root.height - 170

            Label:
                id: error
                text: ''
                center: root.width / 2, root.height - 400
                font_size: 26
                color: 0.8, 0, 0, 0.8
                size_hint: None, None
                size: root.width * .6, 30

        FloatLayout:

            Button:
                text: 'Return'
                size_hint: .2, .1
                pos_hint: {'x': .3, 'y': 0}
                on_release:
                    app.screen_manager.current = 'main'

            Button:
                text: 'Connect'
                size_hint: .2, .1
                pos_hint: {'x': .5, 'y': 0}


<ScreenFour>: 
    name: 'connection'

    AsyncImage:
        source: 'icons/screen.jpg'
        allow_stretch: True
        keep_ratio: False
        keep_data: True

    FloatLayout:

        Label:
            center: root.width / 2, root.height / 2
            color: 0, 0, 0, 1
            text: 'Connecting...'
            font_size: 26
            size_hint: None, None
            size: root.width * .6, 30

<Cell>:
    background_normal: 'icons/cell.png'
    background_disabled_normal: self.background_normal
<ScreenFive>: 
    ship_grid: grid
    ship_counter: counter
    turn_indicator: turn

    AsyncImage:
        source: 'icons/title_screen.jpg'
        allow_stretch: True
        keep_ratio: False
        keep_data: True

    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'
        size_hint: 1, .8

        FloatLayout:

            Label:
                id: turn
                text: ''
                font_size: 26
                size_hint: 1, 0.1
                pos: 0, root.height * 0.02

            Label:
                id: counter
                text: '10 ships left'
                font_size: 26
                color: 0, 0, 0, 1
                size_hint: 1, 0.1
                pos: 0, root.height * 0.8

        GridLayout:
            id: grid
            size: min(root.height * 0.7, root.width), min(root.height * 0.7, root.width)
            size_hint: None, None
            rows: 10
            cols: 10
            spacing: 2


""")


# Create a class for all screens in which you can include
# helpful methods specific to that screen
class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    pass


class ScreenThree(Screen):
    pass


class ScreenFour(Screen):
    pass


class ScreenFive(Screen):
    pass


# The ScreenManager controls moving between screens
screen_manager = ScreenManager()

# Add the screens to the manager and then supply a name
# that is used to switch screens
screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFour(name="screen_four"))
screen_manager.add_widget(ScreenFive(name="screen_five"))


# Create the App class
class ScreenApp(App):
    def build(self):
        return screen_manager

    # run the app


sample_app = ScreenApp()
sample_app.run()
