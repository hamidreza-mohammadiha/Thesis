# Dynamic Pricing Serious Game Simulation
# written by : H. Reza
# 2022-2023

# Libraries 
import numpy as np
from numpy import random
import tkinter as tk
import customtkinter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import webbrowser
from scipy.interpolate import make_interp_spline
import requests
import pandas as pd

# Classes 
class Player:
    def __init__(self, **kwargs):
        self._type = kwargs['type'] if 'type' in kwargs else 'Person'
        self._name = kwargs['name'] if 'name' in kwargs else 'Decider'
        self._id = kwargs['id'] if 'id' in kwargs else 'null'
        self._brand_score = kwargs['brand_score'] if 'brand_score' in kwargs else 1.618
        self._share = kwargs['share'] if 'share' in kwargs else 0.333
        self._Cost = kwargs['Cost'] if 'Cost' in kwargs else 3
        self._Market_Cap = kwargs['Market_Cap'] if 'Market_Cap' in kwargs else 0
        self._Price = kwargs['Price'] if 'Price' in kwargs else 25
        self._Demand = kwargs['Demand'] if 'Demand' in kwargs else 200
        self._Revenue = kwargs['Revenue'] if 'Revenue' in kwargs else 2000
    def type(self, t = None):
        if t: self._type = t
        return self._type
    def name(self, n = None):
        if n: self._name = n
        return self._name
    def id(self, i = None):
        if i: self._id = i
        return self._id
    def brand_score(self, br = None):
        if br: self._brand_score = br
        return self._brand_score
    def share(self, s = None):
        if s: self._share = s
        return self._share
    def Cost(self, c=None):
        if c: self._Cost = c
        return self._Cost  
    def Market_Cap(self, M=None):
        if M: self._Market_Cap = M
        return self._Market_Cap
    def Price(self, pr=None):
        if pr: self._Price = pr
        return self._Price
    def Demand(self, D=None):
        if D: self._Demand = D
        return self._Demand
    def Revenue(self, R=None):
        if R: self._Revenue = R
        return self._Revenue
    def __str__(self):
        return f' PlayerNumber{self.id()}: "{self.name()}"  Market Cap "{self.Market_Cap()}"'
class Store:
    def __init__(self, **kwargs):
        self._type = kwargs['type'] if 'type' in kwargs else 'Store'
        self._name = kwargs['name'] if 'name' in kwargs else 'City'
        self._id = kwargs['id'] if 'id' in kwargs else 'null'
        self._location = kwargs['location'] if 'location' in kwargs else [0,0]
        self._population = kwargs['population'] if 'population' in kwargs else 100000
        self._payment = kwargs['payment'] if 'payment' in kwargs else 0
        self._elasticity = kwargs['elasticity'] if 'elasticity' in kwargs else 1.1

    def type(self, t = None):
        if t: self._type = t
        return self._type
    def name(self, n = None):
        if n: self._name = n
        return self._name
    def id(self, i = None):
        if i: self._id = i
        return self._id
    def location(self, l = None):
        if l: self._location = l
        return self._location
    def population(self, pop = None):
        if pop: self._population = pop
        return self._population
    def payment(self, pa = None):
        if pa: self._payment = pa
        return self._payment
    def elasticity(self, e = None):
        if e: self._elasticity = e
        return self._elasticity

    def __str__(self):
        return f' StoreNumber{self.id()}: {self.type()} = "{self.name()}"'   
class Product:
    def __init__(self, **kwargs):
        self._type = kwargs['type'] if 'type' in kwargs else 'Product'
        self._name = kwargs['name'] if 'name' in kwargs else 'Cheese'
        self._id = kwargs['id'] if 'id' in kwargs else 'null'
        self._AvgPrice = kwargs['AvgPrice'] if 'AvgPrice' in kwargs else 1

    def type(self, t = None):
        if t: self._type = t
        return self._type
    def name(self, n = None):
        if n: self._name = n
        return self._name
    def id(self, i = None):
        if i: self._id = i
        return self._id
    def AvgPrice(self, ap = None):
        if ap: self._AvgPrice = ap
        return self._AvgPrice
class History:
    def __init__(self, **kwargs):
        self._type = kwargs['type'] if 'type' in kwargs else 'Play'
        self._name = kwargs['name'] if 'name' in kwargs else 'Album'
        self._time = kwargs['time'] if 'time' in kwargs else 0
        self._AddedValue = kwargs['AddedValue'] if 'AddedValue' in kwargs else 0
        self._TakenValue = kwargs['TakenValue'] if 'TakenValue' in kwargs else 0
        self._Player = kwargs['Player'] if 'Player' in kwargs else 0

    def type(self, t = None):
        if t: self._type = t
        return self._type
    def name(self, n=None):
        if n: self._name = n
        return self._name
    def time(self, t=None):
        if t: self._time = t
        return self._time
    def AddedValue(self, E=None):
        if E: self._AddedValue = E
        return self._AddedValue
    def TakenValue(self, p = None):
        if p: self._TakenValue = p
        return self._TakenValue
    def Player(self, p = None):
        if p: self._Player = p
        return self._Player
class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

# Functions
def demand(Time):
    R = random.uniform(0.95,1.05)
    d = max(R * (0.0742*np.power(Time,3) - 5.7134*np.power(Time,2) + 101.050*np.power(Time,1) + 2311),10)
    return round(d,0)
def BitCoin_Price():
    # defining key/request url
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    # requesting data from url
    data = requests.get(key)
    data = data.json()
    #print(f"{data['symbol']} price is {data['price']}")
    #print(data['price'])
    return data['price']
def dashboard(Pricing, Demand, T):
    x = list(range(1, 53))
    colors = ["red", "blue", "purple", "brown"]
    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(12, 8))
    # Pricing subplot
    axs[0].plot(x, Pricing[0], color=colors[0], marker=".", label="Red")
    axs[0].plot(x, Pricing[1], color=colors[1], marker=".", label="Blue")
    axs[0].plot(x, Pricing[2], color=colors[2], marker=".", label="Purple")
    axs[0].set_title("Pricings")
    axs[0].set_ylabel("$")

    axs[0].axvline(x=14, color='black', linestyle='--',linewidth=0.5)
    axs[0].axvline(x=27, color='black', linestyle='--',linewidth=0.5)
    axs[0].axvline(x=40, color='black', linestyle='--',linewidth=0.5)

    axs[0].legend()

    # Demand subplot
    axs[1].plot(x, Demand[0], color=colors[0], marker=".", label="Red")
    axs[1].plot(x, Demand[1], color=colors[1], marker=".", label="Blue")
    axs[1].plot(x, Demand[2], color=colors[2], marker=".", label="Purple")
    axs[1].set_title("Demands")
    axs[1].set_xlabel("weeks")
    axs[1].set_ylabel("Q")
    axs[1].axvline(x=14, color='black', linestyle='--',linewidth=0.5)
    axs[1].axvline(x=27, color='black', linestyle='--',linewidth=0.5)
    axs[1].axvline(x=40, color='black', linestyle='--',linewidth=0.5)
    axs[1].legend()

    if T == 14:
        axs[0].axvline(x=14, color='yellow', linestyle='--',linewidth=1)
        axs[1].axvline(x=14, color='yellow', linestyle='--',linewidth=1)
    if T == 27:
        axs[0].axvline(x=27, color='yellow', linestyle='--',linewidth=1)
        axs[1].axvline(x=27, color='yellow', linestyle='--',linewidth=1)
    if T == 40:
        axs[0].axvline(x=40, color='yellow', linestyle='--',linewidth=1)
        axs[1].axvline(x=40, color='yellow', linestyle='--',linewidth=1)

    plt.tight_layout()
    plt.show()
def callback(url):
    webbrowser.open_new_tab(url)
def Result(u, c, z):
     
        x = range(1, 53)
        fig = plt.figure(figsize=(16, 8))
        
        ax = fig.add_subplot(1, 1, 1)

        ax.set_xticklabels(x)

        cmap = plt.get_cmap('viridis')

        spl = make_interp_spline(x, z)

        x_new = np.linspace(1, 52, 100)

        line, = ax.plot([], [], color=cmap(0.8), linewidth=2)

        scatter = ax.scatter(x, z, s=60, c=cmap(np.linspace(0, 1, len(x))), edgecolors='black', linewidths=1)

        BTC0 = int(float(BitCoin_Price()))
        ax.axhline(BTC0*10, linestyle='--', color='gray', linewidth=1.2)
        ax.axhline(BTC0*10*(1.21), linestyle='--', color='orange', linewidth=1.25)
        ax.axhline(BTC0*10*(2.00), linestyle='--', color='green', linewidth=1.3)

        ax.set_facecolor('none')

        def animate(i):
            # Evaluate the interpolated curve at the current i-value to get the corresponding y-values
            y_smooth = spl(x_new[:i])
            # Update the line data with the new x and y values
            line.set_data(x_new[:i], y_smooth)
            # Return the line object to be redrawn
            return line,

        ani = animation.FuncAnimation(fig, animate, frames=len(x_new), interval=10, blit=True)
        
        lineA, = ax.plot(x, u, color="Red")
        lineB, = ax.plot(x, c, color="Blue")
        line, = ax.plot(x, z, color="purple")


        ax.set_title('Market Capital')

        ax.set_xlabel('Weeks')

        ax.set_ylabel('$$$')

        ax.set_xticks([i + 0.5 for i in x])

        ax.set_xticklabels(x)

        ax.legend([line, lineA, lineB], ['Purple', 'Red', 'Blue'])

        cmap = plt.get_cmap('viridis')

        spl = make_interp_spline(x, z, k=5)

        smooth = spl(x)

        line, = ax.plot(x, smooth, color="purple", linestyle='--')
        
        plt.show()

# Main
def main():
#   Player Variables ---
    Max_Player_Num = 3
    Player_Num = 2 
    Auction_Num = 52
    Interest_rate = 0.21
    BTC0 = 26000
    BTC1 = 0
    ma = 0
    mb = 0
    bpa = 0
    bpb = 0
    t = 0


#   Global Variables ---
    A = 1
    Intro = 0

    Title_text = "Revenue Management Serious Game"
    Intro_text = "In this Game you are up to Manage your Product and set your Business Strategies.\n" \
                    "All Teams (+ AI player) will get a same Initial Capital Equal to 10 BitCoins. \n" \
                    "You will start the game by Investig it on these parts: \n\n" \
                    "- Improving your Brand Score\n-Optimizing your Finished Cost\n-Saving at Crypto Market\n\n"\
                    "Each BTC will lower your Finished Cost by 1 unit and raise your Brand Score by 2 score. For each one unit increase in the price of Bitcoin, there will be a one percent profit and for each unit price decrease, there will be a one percent loss.\n"\
                    " \n"\
                    "Then you should play your role as product manager in a virtual store by your price and marketing power.\n" \
                    "If you be market leader for a week, your brand score will improve by 0.2 point and if you finish a week as a runner-up your brand score will improve 0.1. This serious game will execute for 4 seasons of a year in week time slot and you can change your price at the beggining or each half. \n" \
                    " \n" \
                    "The highest market cap will win the game.\n" \
                    "Good Luck! \n" \
                    
    Tip_text = "Assign your BTCs based on your strategy. "

    
    Capitals =  [0] * Max_Player_Num
    Pricings =  [0] * Max_Player_Num
    Demands =   [0] * Max_Player_Num
    Revenues =  [0] * Max_Player_Num
    CashFlows = [0] * Max_Player_Num
    Marketings = [0] * Max_Player_Num
    Brands = [0] * Max_Player_Num

#   History Recording ---
    for i in range(Max_Player_Num):
        Time = [0] * Auction_Num
        Capitals[i] = [0] * Auction_Num
        Pricings[i] =  [25] * Auction_Num
        Demands[i] =   [0] * Auction_Num
        Revenues[i] =  [0] * Auction_Num
        CashFlows[i] = [0] * Auction_Num
        Marketings[i] = [0] * Auction_Num
        Brands[i] = [0] * Auction_Num
        BitCoins = [0] * Auction_Num

    BTC0 = int(float(BitCoin_Price()))
    Capitals[0][0] = 10*BTC0
    Capitals[1][0] = 10*BTC0
    Capitals[2][0] = 10*BTC0

#   Players ---
    Team_A = Player(id=1, Cost=25, brand_score=25, Market_Cap = 0)
    Team_B = Player(id=2, Cost=25, brand_score=25, Market_Cap = 0)
    AI_Player = Player(id=3, Cost=40, brand_score=45, Market_Cap = 0)
    Players = [Team_A, Team_B, AI_Player]

#   Run() ---
    while A < Auction_Num:
        BitCoins[A-1] = int(float(BitCoin_Price()))
        Time[A-1] = A
      
#   Feedback Loops ----------------------------------------------------------------------------------------------------   
        if A == 1 or A == 13 or A == 26 or A == 39:
            #print(Players[0].brand_score(),Players[1].brand_score(),Players[2].brand_score() )
            if A == 13 or A == 26 or A == 39:
                dashboard(Pricings, Demands, A+1)

                u = [0] * Auction_Num
                z = [0] * Auction_Num
                c = [0] * Auction_Num

                for w in range(Auction_Num):
                    u[w] = Capitals[0][w]/(np.power((1+Interest_rate/52),w-1))
                    c[w] = Capitals[1][w]/(np.power((1+Interest_rate/52),w-1))
                    z[w] = Capitals[2][w]/(np.power((1+Interest_rate/52),w-1))

                if A == 13:
                    Season_text = "Summer"

                if A == 26:
                    Season_text = "Autumn"
                    Result(u, c, z)

                if A == 39:
                    Season_text = "Winter"


                Intro_text = "Now You can update Your Pricing Strategy. What's your new end-season Price?"

                customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
                customtkinter.set_default_color_theme("dark-blue")  # Themes: "dark-blue" (standard), "green", "dark-blue"
                
                app = customtkinter.CTk()
                #app.geometry("1280x780")
                app.title("CustomTkinter simple_example.py")
                
                frame_1 = customtkinter.CTkFrame(master=app)
                frame_1.grid(row=0, column=0, padx=200, pady= 150)

                label_1 = customtkinter.CTkLabel(master=frame_1,text =Title_text, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=20, weight="bold"))
                label_1.grid(row=1, column=1, padx = 30 , pady = 20 )

                label_2 = customtkinter.CTkLabel(master=frame_1,text =Intro_text, wraplength=500, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=16, weight="bold" ))
                label_2.grid(row=2, column=1, padx = 30 , pady = 20 )

                label_3 = customtkinter.CTkLabel(master=frame_1,text =Season_text, wraplength=500, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=16, weight="bold" ))
                label_3.grid(row=3, column=1, padx = 30 , pady = 20 )

                def slider_callback_F(value):
                    label_F_Price.configure(text = f"Your Finishing Price: {int(value)}")
                    Pricings[0][A+12] = int(value)

                def slider_callback_FA(value):
                    label_FA_Price.configure(text = f"Your Finishing Price: {int(value)}")
                    Pricings[1][A+12] = int(value)
                    
                label_F_Price = customtkinter.CTkLabel(master=frame_1,text ="...", justify=customtkinter.LEFT)
                label_F_Price.grid(row=4, column=0, padx = 30 , pady = 10 )

                label_FA_Price = customtkinter.CTkLabel(master=frame_1,text ="...", justify=customtkinter.LEFT)
                label_FA_Price.grid(row=4, column=2, padx = 30 , pady = 10 )

                slider_2 = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_F(x), from_=25, to=75)
                slider_2.grid(row=5, column=0, padx = 30 , pady = 10 )
                slider_2.set(50)

                slider_2A = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_FA(x), from_=25, to=75)
                slider_2A.grid(row=5, column=2, padx = 30 , pady = 10 )
                slider_2A.set(50)

                combobox_var11 = customtkinter.StringVar(value="Choose Your Marketing Power")  # set initial value

                def combobox_callback11(choice):
                    Marketings[0][A] = Capitals[0][A-1]*float(choice)
                    Players[0].brand_score(Players[0].brand_score() + (Marketings[0][A]/5000))


                combobox11 = customtkinter.CTkComboBox(master=frame_1,
                                                    values=["0", "0.14", "0.28", "0.42", "0.57", "0.71", "0.85", "1"],
                                                    command=combobox_callback11,
                                                    variable=combobox_var11, width=222)
                combobox11.grid(row=6, column=0, padx=10, pady= 25)

                combobox_var22 = customtkinter.StringVar(value="Choose Your Marketing Power")  # set initial value

                def combobox_callback22(choice):
                    Marketings[1][A] = Capitals[1][A-1]*float(choice)
                    Players[1].brand_score(Players[1].brand_score() + (Marketings[1][A]/5000))

                combobox22 = customtkinter.CTkComboBox(master=frame_1,
                                                    values=["0", "0.14", "0.28", "0.42", "0.57", "0.71", "0.85", "1"],
                                                    command=combobox_callback22,
                                                    variable=combobox_var22, width=222)
                combobox22.grid(row=6, column=2, padx=10, pady= 25)

                button_2 = customtkinter.CTkButton(master=frame_1, command=app.destroy, text="Confirm")
                button_2.grid(row=7, column=1, padx = 30 , pady = 30 )

                app.mainloop()

                ma = (Pricings[0][A+12] - Pricings[0][A])/13
                bpa = Pricings[0][A]

                mb = (Pricings[1][A+12] - Pricings[1][A])/13
                bpb = Pricings[1][A]

                t = 26

                if A == 13:
                    Marketings[2][A] = Capitals[2][A-1]*0.42
                    Players[2].brand_score(Players[2].brand_score() + (Marketings[2][A]/5000))
                if A == 26:
                    Marketings[2][A] = Capitals[2][A-1]*0
                    Players[2].brand_score(Players[2].brand_score() + (Marketings[2][A]/5000))
                if A == 39:
                    Marketings[2][A] = Capitals[2][A-1]*0
                    Players[2].brand_score(Players[2].brand_score() + (Marketings[2][A]/5000))

            if A == 1:

                customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
                customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
                
                app = customtkinter.CTk()
                #app.geometry("1280x780")
                app.title("Introduction_Page.py")
                
                frame_1 = customtkinter.CTkFrame(master=app)
                frame_1.pack(pady=50, padx=100, fill="both", expand=True)

                label_1 = customtkinter.CTkLabel(master=frame_1,text =Title_text, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=21, weight="bold"))
                label_1.pack(padx=20, pady= 45)

                label_2 = customtkinter.CTkLabel(master=frame_1,text =Intro_text, wraplength=780, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=14))
                label_2.pack(padx=20, pady= 25)

                BTC0 = int(float(BitCoin_Price()))
                BTC_Price = f"Real-Time BitCoin Price:        {BTC0}"
                BTC_Value = f"Your Initial Capital:        {BTC0*10}"
                
                label_BTC = customtkinter.CTkLabel(master=frame_1,text = BTC_Price, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=13))
                label_BTC.pack(padx=20, pady= 5)

                label_BTC_Value = customtkinter.CTkLabel(master=frame_1,text = BTC_Value, justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=13))
                label_BTC_Value.pack(padx=20, pady= 5)

                button_2 = customtkinter.CTkButton(master=frame_1, command=app.destroy, text="Start")
                button_2.pack(padx=10, pady= 25)
                
                app.mainloop()

                ### Mechanics

                customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
                customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
                
                app = customtkinter.CTk()
                #app.geometry("1280x780")
                app.title("GamePlay1_Page.py")
                
                frame_1 = customtkinter.CTkFrame(master=app)
                frame_1.grid(row=0, column=0, padx=180, pady= 60)

                label_H = customtkinter.CTkLabel(master=frame_1,text ="Team A", justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=21, weight="bold"))
                label_H.grid(row=0, column=0, padx=200, pady= 5)

                label_A = customtkinter.CTkLabel(master=frame_1,text ="Team B", justify=customtkinter.CENTER, font=customtkinter.CTkFont(size=21, weight="bold"))
                label_A.grid(row=0, column=2, padx=200, pady= 5)

                combobox_var1 = customtkinter.StringVar(value="Choose Your Packaging Level")  # set initial value

                def combobox_callback1(choice):
                    if choice == "Level 1":
                        Players[0].brand_score(25)
                        Players[0].Cost(30)
                    else:
                        if choice == "Level 2":
                            Players[0].brand_score(35)
                            Players[0].Cost(35)
                        else:
                            Players[0].brand_score(45)
                            Players[0].Cost(40)

                combobox1 = customtkinter.CTkComboBox(master=frame_1,
                                                    values=["Level 1", "Level 2", "Level 3"],
                                                    command=combobox_callback1,
                                                    variable=combobox_var1, width=222)
                combobox1.grid(row=1, column=0, padx=10, pady= 15)

                combobox_var2 = customtkinter.StringVar(value="Choose Your Packaging Level")  # set initial value

                def combobox_callback2(choice):
                    if choice == "Level 1":
                        Players[1].brand_score(25)
                        Players[1].Cost(30)
                    else:
                        if choice == "Level 2":
                            Players[1].brand_score(35)
                            Players[1].Cost(35)
                        else:
                            Players[1].brand_score(45)
                            Players[1].Cost(40)

                label_Pack = customtkinter.CTkLabel(master=frame_1,text =" Level 1:  Brand Score = 25,  Finished Cost = 30 \n Level 2:  Brand Score = 35,  Finished Cost = 35 \n Level 3:  Brand Score = 45,  Finished Cost = 40   ", justify=customtkinter.LEFT, wraplength=300 )
                label_Pack.grid(row=1, column=1, padx=10, pady= 25)

                combobox2 = customtkinter.CTkComboBox(master=frame_1,
                                                    values=["Level 1", "Level 2", "Level 3"],
                                                    command=combobox_callback2,
                                                    variable=combobox_var2, width=222)
                combobox2.grid(row=1, column=2, padx=10, pady= 15)

                label_Inv = customtkinter.CTkLabel(master=frame_1,text ="Choose Your Investment Strategy", justify=customtkinter.CENTER)
                label_Inv.grid(row=2, column=1, padx=10, pady= 25)

                entry_H1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Branding")
                entry_H1.grid(row=3, column=0, padx=10, pady=5)

                entry_A1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Branding")
                entry_A1.grid(row=3, column=2, padx=10, pady=5)

                entry_H2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Cost Optimization")
                entry_H2.grid(row=4, column=0, padx=10, pady=5)

                entry_A2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Cost Optimization")
                entry_A2.grid(row=4, column=2, padx=10, pady=5)

                entry_H3 = customtkinter.CTkEntry(master=frame_1, placeholder_text="BTC Holding")
                entry_H3.grid(row=5, column=0, padx=10, pady=5)

                entry_A3 = customtkinter.CTkEntry(master=frame_1, placeholder_text="BTC Holding")
                entry_A3.grid(row=5, column=2, padx=10, pady=5)

                Done_text = "..."
                AA_text = "..."

                def Submit():
                    if int(entry_H1.get())+int(entry_H2.get())+int(entry_H3.get()) == 10 and int(entry_A1.get())+int(entry_A2.get())+int(entry_A3.get()) == 10:
                        Players[0].brand_score(Players[0].brand_score() + 2*int(float(entry_H1.get())))
                        Players[0].Cost(Players[0].Cost() - int(float(entry_H2.get())))
                        Players[0].Market_Cap(int(float(entry_H3.get())))

                        Players[1].brand_score(Players[1].brand_score() + 2*int(float(entry_A1.get())))
                        Players[1].Cost(Players[1].Cost() - int(float(entry_A2.get())))
                        Players[1].Market_Cap(int(float(entry_A3.get())))

                        label_Done.configure(text = f"   Done! \n\n Your Brand Score :  {Players[0].brand_score()} \n\n Finished Cost :  {Players[0].Cost()} \n\n Remaining :  {Players[0].Market_Cap()} BTC ")
                        label_AA.configure(text = f"   Done! \n\n Your Brand Score :  {Players[1].brand_score()} \n\n Finished Cost :  {Players[1].Cost()} \n\n Remaining :  {Players[1].Market_Cap()} BTC ")
                    else:
                        label_Done.configure(text = "Not Valid")
                        label_AA.configure(text = "Not Valid")
                    

                button_1 = customtkinter.CTkButton(master=frame_1, command=Submit, text="Submit")
                button_1.grid(row=6, column=1, padx=10, pady= 5)

                label_Done = customtkinter.CTkLabel(master=frame_1,text = Done_text, justify=customtkinter.LEFT)
                label_Done.grid(row=7, column=0, padx=10, pady= 5)

                label_AA = customtkinter.CTkLabel(master=frame_1,text = AA_text, justify=customtkinter.LEFT)
                label_AA.grid(row=7, column=2, padx=10, pady= 5)

                label_Pricing = customtkinter.CTkLabel(master=frame_1,text ="Now Choose Your Pricing Strategy", justify=customtkinter.CENTER)
                label_Pricing.grid(row=8, column=1, padx=10, pady= 5)
                
                def slider_callback_S(value):
                    label_S_Price.configure(text = f"Your Season Starting Price: {int(value)}")
                    Pricings[0][0] = int(value)

                def slider_callback_SA(value):
                    label_SA_Price.configure(text = f"Your Season Starting Price: {int(value)}")
                    Pricings[1][0] = int(value)

                label_S_Price = customtkinter.CTkLabel(master=frame_1,text ="...", justify=customtkinter.LEFT)
                label_S_Price.grid(row=9, column=0, padx=10, pady= 5)

                label_SA_Price = customtkinter.CTkLabel(master=frame_1,text ="???", justify=customtkinter.LEFT)
                label_SA_Price.grid(row=9, column=2, padx=10, pady= 5)

                slider_1 = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_S(x), from_=25, to=75)
                slider_1.grid(row=10, column=0, padx=10, pady= 5)
                slider_1.set(50)

                slider_1A = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_SA(x), from_=25, to=75)
                slider_1A.grid(row=10, column=2, padx=10, pady= 5)
                slider_1A.set(50)

                def slider_callback_F(value):
                    label_F_Price.configure(text = f"Your Season Finishing Price: {int(value)}")
                    Pricings[0][13] = int(value)

                def slider_callback_FA(value):
                    label_FA_Price.configure(text = f"Your Season Finishing Price: {int(value)}")
                    Pricings[1][13] = int(value)
                    

                label_F_Price = customtkinter.CTkLabel(master=frame_1,text ="...", justify=customtkinter.LEFT)
                label_F_Price.grid(row=11, column=0, padx=10, pady= 5)

                label_FA_Price = customtkinter.CTkLabel(master=frame_1,text ="???", justify=customtkinter.LEFT)
                label_FA_Price.grid(row=11, column=2, padx=10, pady= 5)

                slider_2 = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_F(x), from_=25, to=75)
                slider_2.grid(row=12, column=0, padx=10, pady= 5)
                slider_2.set(50)

                slider_2A = customtkinter.CTkSlider(master=frame_1, command = lambda x: slider_callback_FA(x), from_=25, to=75)
                slider_2A.grid(row=12, column=2, padx=10, pady= 5)
                slider_2A.set(50)

                button_2 = customtkinter.CTkButton(master=frame_1, command=app.destroy, text="Confirm")
                button_2.grid(row=13, column=1, padx=10, pady= 15)

                #app.attributes("-fullscreen", True)
                
                app.mainloop()

                ma = (Pricings[0][13] - Pricings[0][0])/13
                bpa = Pricings[0][0]

                mb = (Pricings[1][13] - Pricings[1][0])/13
                bpb = Pricings[1][0]
                #print(m)


                    
                Capitals[0][1] = 0
                Capitals[1][1] = 0
                Capitals[2][1] = 0


#   Calculations ------------------------------------------------------------------------------------------------------

        if A == 1:
            Players[2].Market_Cap(0)
            Players[2].brand_score(45+10)
            Players[2].Cost(45-5)
        
        MT = 0
        M = [0] * Max_Player_Num
        S = [0] * Max_Player_Num
        P = [0] * Max_Player_Num

        D0 = 0
        D1 = 0
        D2 = 0

        Players[0].Price(bpa + (A%13)*ma)
        Players[1].Price(bpb + (A%13)*mb)

        v = 55
        if A < 14:
            Players[2].Price(55)
        else:
            if A < 27:
                Players[2].Price(55)
            else:
                if A < 40:
                    Players[2].Price(55)
                else:
                    Players[2].Price(55)
        Pricings[2][0] = 55
   
 

    
        M[0] = Players[0].brand_score()/(Players[0].Price())
        M[1] = Players[1].brand_score()/(Players[1].Price())
        M[2] = Players[2].brand_score()/(Players[2].Price())

        MT += M[0]
        MT += M[1]
        MT += M[2]

        S[0] = M[0]/MT
        P[0] = -0.0003*np.power(Players[0].Price(),2) + 0.0136*Players[0].Price() + 0.8597

        S[1] = M[1]/MT
        P[1] = -0.0003*np.power(Players[1].Price(),2) + 0.0136*Players[1].Price() + 0.8597

        S[2] = M[2]/MT
        P[2] = -0.0003*np.power(Players[2].Price(),2) + 0.0136*Players[2].Price() + 0.8597

        Dt = demand(A)

        if A > 13 :
            D0 = min(max(Dt * P[0] * S[0], Demands[0][A-1]*0.75),Demands[0][A-1]*1.25)
            D1 = min(max(Dt * P[1] * S[1], Demands[1][A-1]*0.75),Demands[1][A-1]*1.25)
            D2 = min(max(Dt * P[2] * S[2], Demands[2][A-1]*0.75),Demands[2][A-1]*1.25)

            if D0 > D1:
                if D1 > D2:
                    Players[0].brand_score(max(Players[0].brand_score()+0.2,1))
                    Players[1].brand_score(max(Players[1].brand_score()+0.1,1))

                else:
                    if D0 > D2:
                        Players[0].brand_score(max(Players[0].brand_score()+0.2,1))
                        Players[2].brand_score(max(Players[2].brand_score()+0.1,1))
                    else:
                        Players[2].brand_score(max(Players[2].brand_score()+0.2,1))
                        Players[0].brand_score(max(Players[0].brand_score()+0.1,1))

            else:
                if D0 > D2:
                    Players[1].brand_score(max(Players[1].brand_score()+0.2,1))
                    Players[0].brand_score(max(Players[0].brand_score()+0.1,1))
                else:
                    if D1 > D2:
                        Players[1].brand_score(max(Players[1].brand_score()+0.2,1))
                        Players[2].brand_score(max(Players[2].brand_score()+0.1,1))
                    else:
                        Players[2].brand_score(max(Players[2].brand_score()+0.2,1))
                        Players[1].brand_score(max(Players[1].brand_score()+0.1,1))
                

        else:
            if A == 1:
                D0 = 100
                D1 = 100
                D2 = 100
            else:
                D0 = max(min(Dt * P[0] * S[0], Demands[0][A-1] * 2 ), 10)
                D1 = max(min(Dt * P[1] * S[1], Demands[1][A-1] * 2 ), 10)
                D2 = max(min(Dt * P[2] * S[2], Demands[2][A-1] * 2 ), 10)

        D = [D0, D1, D2]

        for i in range(Player_Num + 1):
            Players[i].Demand(D[i])
            Players[i].Revenue((Players[i].Price()-Players[i].Cost())*Players[i].Demand())

            Pricings[i][A] =  Players[i].Price()
            Demands[i][A] = Players[i].Demand()
            CashFlows[i][A] = Players[i].Revenue()
            Brands[i][A] = Players[i].brand_score()
            BitCoins[A] = int(float(BitCoin_Price()))

            Revenues[i][A] += CashFlows[i][A]
            Capitals[i][A] += CashFlows[i][A]
            Capitals[i][A] -= Marketings[i][A] 

        AA = A + 1
        while AA < Auction_Num:
            for i in range(Player_Num + 1):
                Pricings[i][AA] = Pricings[i][A]
                Demands[i][AA]  =  Demands[i][A]
                Revenues[i][AA] = Revenues[i][A]
                CashFlows[i][AA] = CashFlows[i][A]
                Capitals[i][AA] =  Capitals[i][A]

            AA += 1

    #   Print() -------------------------------------------------------------------------------------------------------
        A +=1

#   Animation() -------------------------------------------------------------------------------------------------------
    dashboard(Pricings, Demands, 52)

    u = [0] * Auction_Num
    z = [0] * Auction_Num
    c = [0] * Auction_Num
    btc = [0] * Auction_Num
    b0 = [0] * Auction_Num
    b1 = [0] * Auction_Num
    b2 = [0] * Auction_Num
    d = [0] * Auction_Num
    p0 = [0] * Auction_Num
    p1 = [0] * Auction_Num
    p2 = [0] * Auction_Num

    BTC1 =  int(float(BitCoin_Price()))
    BTC_factor = 1 + (BTC1 - BTC0)/100
    
    Capitals[0][51] += Players[0].Market_Cap() * BTC_factor * BTC0
    Capitals[1][51] += Players[1].Market_Cap() * BTC_factor * BTC0
    Capitals[2][51] += Players[2].Market_Cap() * BTC_factor * BTC0

    print("BTC interest rate: % ", (BTC_factor-1)*100)


    for w in range(Auction_Num):
        u[w] = Capitals[0][w]
        c[w] = Capitals[1][w]
        z[w] = Capitals[2][w]
        btc[w] = BitCoins[w]
        b0[w] = Brands[0][w]
        b1[w] = Brands[1][w]
        b2[w] = Brands[2][w]
        d[w] = Demands[0][w] + Demands[1][w] + Demands[2][w]
        p0[w] = Pricings[0][w]
        p1[w] = Pricings[1][w]
        p2[w] = Pricings[2][w]
    
    Result(u, c, z)


    x = list(range(1, 53))

    data = {'Time': x, 'Red - Capital': u, 'Blue - Capital': c, 'Puprple- Capital': z,
             'Red - Brand': b0, 'Blue - Brand': b1, 'Puprple - Brand': b2,
             'Red - Price': p0, 'Blue - Price': p1, 'Puprple - Price': p2,
             'Bitcoin ($)': btc,
             'Total Demand' : d,
            }
    

    # create a pandas dataframe from the dictionary
    df = pd.DataFrame(data)

    df.to_excel(excel_writer= "C:/Users/asus/OneDrive/Desktop/MSc Thesis/Tim.Kaj/LastOutput.xlsx")

    colors = ['red', 'blue', 'purple']

    timeline = range(0, 52)
    data = {
        'Red': u,
        'Blue': c,
        'Purple': z
    }

    df = pd.DataFrame(data, index=timeline)

    # Create a figure and axes
    fig, ax = plt.subplots()

    def update_bar_chart(i):
        ax.clear()
        ax.barh(df.columns, df.iloc[i], color=colors)
        ax.set_xlim(0, max(df.iloc[i]) + 2)
        ax.set_title(f'Agent Data - Week {i+1}')

    # Create the animation
    animation = FuncAnimation(fig, update_bar_chart, frames=len(df), interval=200, repeat=False)

    # Save the animation as a GIF file
    animation.save('bar_chart_animation.gif', writer='imagemagick')

    # Show the animation
    plt.show()
if __name__ == '__main__': main()
