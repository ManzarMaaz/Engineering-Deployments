from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from Environment import *
from Agent import *

main = tkinter.Tk()
main.title("IOT Based Smart Irrigation System using Reinforcement Learning")
main.geometry("1300x1200")

global filename
global dataset
global X, Y, X_train, X_test, y_train, y_test, scaler
global rewards, penalty, env, agent

def uploadDataset():
    global filename, dataset
    filename = filedialog.askopenfilename(initialdir="Dataset")
    pathlabel.config(text=filename)
    text.delete('1.0', END)
    text.insert(END, 'Smart Irrigation Dataset loaded\n\n')
    dataset = pd.read_csv(filename)
    dataset.fillna(0, inplace=True)
    text.insert(END, str(dataset))
    
    # Graphing class distribution
    labels, count = np.unique(dataset['class'], return_counts=True)
    height = count
    bars = labels
    y_pos = np.arange(len(bars))
    plt.figure(figsize=(4,3))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.xlabel("Irrigation Condition Labels")
    plt.ylabel("Count")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def splitDataset():
    text.delete('1.0', END)
    global X, Y, X_train, X_test, y_train, y_test
    # Logic to split dataset would go here (implied from context)
    text.insert(END, "Dataset Train & Test Splits for Reinforcement Learning\n")

def trainRL():
    global env, agent, rewards, penalty
    env = Environment()
    agent = Agent(env)
    rewards, penalty = agent.step(X_train, y_train, X_test, y_test)
    text.insert(END, "Reinforcement Learning Completed\n\n")
    text.insert(END, "Total Training Rewards = " + str(rewards) + "\n")
    text.insert(END, "Total Training Penalties = " + str(penalty) + "\n")

def graph():
    global rewards, penalty
    height = [rewards, penalty]
    bars = ('Rewards', 'Penalty')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.title("Rewards & Penalty Graph")
    plt.show()

# Button Layout
font1 = ('times', 13, 'bold')
upload = Button(main, text="Upload Irrigation Dataset", command=uploadDataset)
upload.place(x=800, y=100)
upload.config(font=font1)

pathlabel = Label(main)
pathlabel.config(bg='lawn green', fg='dodger blue')
pathlabel.config(font=font1)
pathlabel.place(x=800, y=150)

trainButton = Button(main, text="Train Reinforcement Learning Algorithm", command=trainRL)
trainButton.place(x=800, y=300)
trainButton.config(font=font1)

main.config(bg='light salmon')
main.mainloop()