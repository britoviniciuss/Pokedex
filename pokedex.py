from distutils.errors import LinkError
import io
import imp
from io import BytesIO
from tkinter import ANCHOR, CENTER, HORIZONTAL, NW, RIDGE, Button, ttk
from urllib.request import urlopen
from PIL import Image, ImageTk
import tkinter as tk
from cProfile import label
import requests
import colorama
import urllib3
from colorama import Fore
colorama.init(autoreset=True)

co0 = "#444466"  # Black
co1 = "#feffff"  # White
co2 = "#6f9fbd"  # Blue
co3 = "#38576b"  # Value
co4 = "#403d3d"   # Letter
co5 = "#ef5350"   # Red


class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Pokedex")
        self.window.geometry('550x510')
        self.window.configure(bg=co1)

        self.poke_frame = tk.Frame(self.window, width=550, height=290, relief='flat')
        self.poke_frame.grid(row=1, column=0)

        self.poke_name = tk.Label(self.poke_frame, text='Name', relief='flat',
                             anchor=CENTER, font=('Fixedsys 20'), bg=co1, fg=co0)
        self.poke_name.place(x=12, y=15)

        self.poke_category = tk.Label(self.poke_frame, text='Category', relief='flat',
                                  anchor=CENTER, font=('Ivy 10 bold'), bg=co1, fg=co0)
        self.poke_category.place(x=12, y=55)

        self.poke_ID = tk.Label(self.poke_frame, text='# ID', relief='flat',
                           anchor=CENTER, font=('Ivy 10 bold'), bg=co1, fg=co0)
        self.poke_ID.place(x=12, y=80)

        self.poke_status = tk.Label(self.window, text='Status', relief='flat',
                               anchor=CENTER, font=('Verdana 20'), bg=co1, fg=co0)
        self.poke_status.place(x=15, y=310)

        self.poke_hp = tk.Label(self.window, text='HP: -', relief='flat',
                           anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_hp.place(x=15, y=360)

        self.poke_attack = tk.Label(self.window, text='Attack: -', relief='flat',
                               anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_attack.place(x=15, y=380)

        self.poke_defense = tk.Label(self.window, text='Defesa: -', relief='flat',
                                anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_defense.place(x=15, y=400)

        self.poke_velocity = tk.Label(self.window, text='Vel: -', relief='flat',
                                 anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_velocity.place(x=15, y=420)

        self.poke_total = tk.Label(self.window, text='Total: -', relief='flat',
                              anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_total.place(x=15, y=440)

        self.poke_status = tk.Label(self.window, text='Skills', relief='flat',
                               anchor=CENTER, font=('Verdana 20'), bg=co1, fg=co0)
        self.poke_status.place(x=200, y=310)

        self.poke_skill_1 = tk.Label(self.window, text='', relief='flat',
                              anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_skill_1.place(x=210, y=360)

        self.poke_skill_2 = tk.Label(self.window, text='', relief='flat',
                              anchor=CENTER, font=('Verdana 10'), bg=co1, fg=co4)
        self.poke_skill_2.place(x=210, y=380)


        self.poke_enter_label = tk.Label(self.window, text='Pokemon: ', relief='flat',
                                    anchor=CENTER, font=('Verdana 10'), fg=co0)
        self.poke_enter_label.place(x=335, y=15)

        self.poke_enter = tk.Entry(self.window, relief='raised',
                              font=('Verdana 12'), bg=co1, fg=co2)
        self.poke_enter.place(x=410, y=15)


        self.button_search = Button(self.window, text="Search", width=30, relief='raised', command=self.change_poke,
                               overrelief=RIDGE, anchor=NW, padx=5, font=('Verdana 12'), bg=co1, fg=co0)
        self.button_search.place(x=360, y=50)

        self.button_descript = Button(self.window, text="Descrição", width=30, relief='raised', command=self.get_description,
                                 overrelief=RIDGE, anchor=NW, padx=5, font=('Verdana 12'), bg=co1, fg=co0)
        self.button_descript.place(x=360, y=90)

        self.button_descript = Button(self.window, text="Descrição", width=30, relief='raised',
                                 overrelief=RIDGE, anchor=NW, padx=5, font=('Verdana 12'), bg=co1, fg=co0)
        self.button_descript.place(x=360, y=90)

        ttk.Separator(self.window, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=272)

        self.panel = tk.Label(self.poke_frame, relief='flat', bg=co1, fg=co0)
        self.panel.place(x=70, y=80)

    def change_poke(self):
        pokemon = self.poke_enter.get()
        pokemon = self.entry_string_handler(pokemon)
        api = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        requisicao = requests.get(api)
        poke_dic = requisicao.json()

        ## Tipo de poke ##
        pokemon = pokemon.capitalize()
        self.poke_name['text'] = pokemon
        for i in poke_dic['types']:
            tipo = i['type']['name']
        self.poke_category['text'] = tipo

        self.poke_ID['text'] = f"#{poke_dic['id']}"

        self.poke_attack['text'] = f"Attack: {poke_dic['stats'][1]['base_stat']}"
        self.poke_hp['text'] = f"HP: {poke_dic['stats'][0]['base_stat']}"
        self.poke_defense['text'] = f"Defense: {poke_dic['stats'][2]['base_stat']}"
        self.poke_velocity['text'] = f"Velocity : {poke_dic['stats'][5]['base_stat']}"

        total = poke_dic['stats'][1]['base_stat'] + poke_dic['stats'][0]['base_stat'] + poke_dic['stats'][2]['base_stat'] + poke_dic['stats'][5]['base_stat']
        self.poke_total['text'] = f"Total : {total}"

        self.poke_skill_1['text'] = poke_dic['abilities'][0]['ability']['name']
        self.poke_skill_2['text'] = poke_dic['abilities'][1]['ability']['name']

        link = poke_dic['sprites']['other']['official-artwork']['front_default']

        img = self.get_image(link)
        self.draw_image(img)

    def get_image(self, link):
        response = requests.get(link)
        img = Image.open(io.BytesIO(response.content))
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)

        return img

    def draw_image(self, image):
        self.panel.configure(image=image)
        self.panel.image = image

    def get_description(self):
        pass

    @staticmethod
    def entry_string_handler(pokemon):
        if pokemon:
            pokemon = pokemon.lower()
            pokemon = pokemon.strip()
        else:
            print("Enter a correctly pokemon name..")
            exit()
        return pokemon

    def run(self):
        self.window.mainloop()


interface = Interface()

interface.run()
