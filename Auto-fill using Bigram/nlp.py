
import nltk
import os
import csv
from operator import itemgetter
import tkinter as tk
from PIL import ImageTk, Image
import re  
from tkinter import END
from nltk.util import ngrams



path = 'C:/Users/Hazem/Documents/VS Python/NLP/sports/'
os.chdir(path)
files = []
Bigrams = []
unigrams = []
unigramCount = {}
bigramCount = {}


for folder in os.listdir(path):
   with open(path + folder, encoding="utf8") as input:
       files.append(input.read())


def extract_ngrams(data, num):
    n_grams = ngrams(nltk.word_tokenize(data), num)
    return [' '.join(grams) for grams in n_grams]


for i in files:
    unigrams.append(extract_ngrams(i, 1))
    Bigrams.append(extract_ngrams(i, 2))
   


for text in unigrams:
    for word in text:
      if word in unigramCount:
        unigramCount[word] = unigramCount[word] + 1
      else:
        unigramCount[word] = 1
    

for word in Bigrams:
    for i in word:
        temp=i.split()
        word1=temp[0]
        word2=temp[1]
        result=(word1, word2)
        if result in bigramCount:
            bigramCount[result] = bigramCount[result] + 1
        else:
            bigramCount[result] = 1
          
    
def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):
    listOfProb = {}
    for bigram in listOfBigrams:
        for i in bigram:
            temp=i.split()
            word1=temp[0]
            word2=temp[1]
            result=(word1, word2)
            listOfProb[result] = bigramCounts[result]/unigramCounts[word1]
    return listOfProb


listOfProb = calcBigramProb(Bigrams, unigramCount, bigramCount)

listOfProbSorted = dict(sorted(listOfProb.items(), key=itemgetter(1), reverse=True)) 




def suggestion(word):
  fill = []
  for k in listOfProbSorted.keys():
      if word == k[0]:
          w=k[0] + " " + k[1]
          fill.append(w)
  return fill  



#--------------------------------------------------------#
#writing report
f = open('C://Users//Hazem//Documents//VS Python//NLP//report.csv', 'w')
headerList = ['Word1', 'Word2', 'Probability', 'Count']
writer = csv.writer(f)
writer.writerow(headerList)

for words in listOfProbSorted.keys():
    row = [words[0], words[1], listOfProbSorted[words], bigramCount[words]]
    writer.writerow(row)
f.close()
#---------------------------------------------------------#




win = tk.Tk()
win.geometry("400x400") 
win.title("Google Search Engine")
font=('Times', 24, 'bold')
img = ImageTk.PhotoImage(Image.open("C://Users//Hazem//Documents//VS Python//NLP//google.jpg"))
button = tk.Button(win, text="Search")
label=tk.Label(text = 'Google Autofill', font=font, image=img)
label.grid(row=0, column=1) 
button.grid(row=1, column=2)




def my_upd(my_widget): # On selection of option 
    my_w = my_widget.widget
    index = int(my_w.curselection()[0]) # position of selection
    value = my_w.get(index) # selected value 
    str.set(value)    # set value for string variable of Entry 
    suggestList.delete(0, END)    # Delete all elements of Listbox


def my_down(my_widget): # down arrow is clicked 
    suggestList.focus()  # move focus to Listbox
    suggestList.selection_set(0) # select the first option 
    
str=tk.StringVar()  # string variable   
entry = tk.Entry(win, textvariable=str, font=font) # entry    
entry.grid(row=1, column=1, padx=10, pady=0)

# Suggested List
suggestList = tk.Listbox(win, height=6, font=font, relief='flat', bg='SystemButtonFace', highlightcolor='SystemButtonFace')
suggestList.grid(row=2, column=1) 

def retrieveData(*args):
    search = entry.get() # user entered string
    search = search.strip()
    search = search.split(" ")
    
    suggestions = suggestion(search[-1])
   
    suggestList.delete(0, END)
    for word in suggestions:
        if(re.match(search[-1], word)):
            suggestList.insert(tk.END, word) #add matching options to Listbox

entry.bind('<Down>', my_down) # down arrow key is pressed
suggestList.bind('<Right>', my_upd) # right arrow key is pressed
suggestList.bind('<Return>', my_upd)# return key is pressed 
str.trace('w', retrieveData) #    

win.mainloop() 