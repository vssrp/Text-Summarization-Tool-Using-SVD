# importing all the required modules like Tkinter, Themed Tkinter, numerical python
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from tkinter import *
import numpy as np


# Definition to open file dialog box and return the selected file path
def browse_file():
    # creating the variable for file path
    file_path = filedialog.askopenfilename()
    # for deleting already existing text in tkinter
    file_path_entry.delete(0, tk.END)
    # inserts the selected file path in the text field in tkinter
    file_path_entry.insert(0, file_path)


# Definition to generate summary
def generate_summary():
    file_path = file_path_entry.get()
    # reading the text from filepath in read mode
    with open(file_path, "r", encoding='utf-8') as file:
        # reading the entire content of the file
        text = file.read()

    # retrieving the length from user input
    summary_length = length_var.get()
    # converting to int as the gui considers it as a string
    summary_length = int(summary_length)
    # retrieving the topics from user input
    num_topics = topic_var.get()
    # converting to int as the gui considers it as a string
    num_topics = int(num_topics)

    # converting the text to lower case
    text = text.lower()

    # stop words from EECS 767 course materials
    stop_words_767 = ['i', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'com', 'de', 'en', 'for', 'from', 'how',
                      'in', 'is', 'it', 'la', 'of','on', 'or', 'that', 'the', 'this', 'to', 'was', 'what',
                      'when', 'where', 'who', 'will', 'with', 'www']
    # basic stop words from web -> reference provided
    stop_words_web = ['am', 'all', 'and', 'but', 'both', 'did', 'do', 'does', 'doing', 'each', 'few', 'had', 'has',
                      'have', 'he', 'her', 'him', 'his', 'me', 'my', 'no', 'nor', 'not', 'off', 'our', 'other',
                      'such', 'their', 'theirs', 'them', 'then', 'these', 'they', 'those', 'through', 'up', 'very',
                      'which', 'why', 'you', 'your', 'yours', 'yourself']

    # appending both and removing the duplicates using the set data structure
    stop_words = stop_words_767 + stop_words_web
    stop_words = list(set(stop_words))

    # creating a list for punctuation's to avoid unnecessary space in dictionaries for similar words
    punctuation = [',', ';', ':', '?', '!', '-', '(', ')', '[', ']', '{', '}', '/', '\\', '*', '_', '|', '&', '$', '#',
                   '@', '%', '+']

    # replace the punctuations in the text with empty
    for p in punctuation:
        text = text.replace(p, "")

    # Split the text into sentences
    sentences = text.split('.')

    # Building dictionaries
    word_to_index = {}
    # index_to_word = {}
    word_index = 0
    for s in sentences:
        # splitting sentences to words
        words = s.split()
        for word in words:
            # Remove stop words and punctuation i.e. do not create a key value pairs for unnecessary words
            if word in stop_words or word in punctuation:
                continue
            # if the word is not present in the dictionary then pass the below if
            if word not in word_to_index:
                # creating new index for the word
                index = len(word_to_index)
                word_to_index[word] = index
                # index_to_word[index] = word
                word_index = word_index + 1

    # Create a term-document matrix for freq of each word
    term_doc_matrix = []
    for s in sentences:
        words = s.split()
        row = [0] * len(word_to_index)
        for word in words:
            # Don't count if the word is either stop words or punctuation
            if word in stop_words or word in punctuation:
                continue
            # counts the freq of occurrence of each word in current sentence
            row[word_to_index[word]] += 1
        term_doc_matrix.append(row)

    # Perform singular value decomposition (SVD)
    U, S, Vt = np.linalg.svd(term_doc_matrix)
    # U: left singular matrix; this gives relationship between sentences and the topics in the text
    # S: diagonal matrix of singular values; this represents the importance of each topic
    # Vt: right singular matrix; this gives relationship between words and the topics in the text

    # Extract the top-k singular vectors
    U_k = U[:, :num_topics]
    # Vt_k = Vt[:num_topics, :]

    # Computing the document vectors in the reduced space
    doc_vectors = np.matmul(U_k.T, term_doc_matrix)

    # summary vector would be the first column
    summary_vector = doc_vectors[:, 0]
    # Empty list for scores
    similarity_scores = []

    for i in range(len(sentences)):
        sentence_vector = doc_vectors[:, i]
        # Compute the cosine similarity between each sentence and the summary vector
        similarity_score = np.dot(sentence_vector, summary_vector) / (
                np.linalg.norm(sentence_vector) * np.linalg.norm(summary_vector))
        similarity_score = round(similarity_score,2)
        # appending the scores
        similarity_scores.append(similarity_score)
    print("Length:", len(similarity_scores))
    print(similarity_scores)
    # Selecting the top-k sentences based on their similarity to the summary vector
    summary_indices = np.argsort(similarity_scores)[-summary_length:]
    # sorting
    summary_indices.sort()
    # joining as sentences
    summary = '.'.join([sentences[i].strip().capitalize() for i in summary_indices])

    # delete any existing text to the summary text field created below
    output_textbox.delete("1.0", END)
    # insert the summary text to the text field created below
    output_textbox.insert(END, summary)


# Create GUI window
# creating an instance of Tk object
window = tk.Tk()

# setting the properties of the window
window.title("Information Summary Tool")
window.configure(background='black')

# Create a style for the buttons and configuring them
style = ttk.Style()
style.configure("TButton", padding=2, relief="flat", bg="#0f4c81", fg="white", font=("Courier", 12, "bold"))

style.configure("TRadioButton", font=("Courier", 10),
                bg="#0f4c81", fg="white", padding=10)

# Creating heading labels and configuring the fonts, paddings, colors
heading = tk.Label(window, text="Information Summary tool", fg="white", bg="black")
heading.config(font=("Courier", 20))
heading.grid(row=1, column=0, columnspan=2, padx=100)
sub_heading = Label(window, text="EECS 767 S2023_Project", fg="white", bg="black")
sub_heading.config(font=("Courier", 16))
sub_heading.grid(row=2, column=0, columnspan=2, padx=100)

# Creating File label
file_path_label = tk.Label(window, text="File", fg="white", bg="black")
file_path_label.grid(row=4, column=0, pady=10, sticky=W)

# Creating a text entry field for the file path
file_path_entry = tk.Entry(window, width=50, fg="white", bg="#0f4c81")
file_path_entry.grid(row=4, column=1, pady=10, sticky=W)

# Creating the button for Browse feature and using the above created themed style for the browse button
browse_button = ttk.Button(window, text="Browse", command=browse_file, style="TButton")
browse_button.grid(row=4, column=2, pady=10, sticky=W)

# Creating length selection dropdown menu
length_label = tk.Label(window, text="Summary length", fg="white", bg="black")
length_label.grid(row=16, column=0, pady=10, sticky=W)

# setting the range to be about to 3 to 15 sentences of summary
length_options = list(range(3, 15))
length_var = tk.StringVar(window)

# setting default value to be 3
# Tkinter expects a string as dropdown options. So we need to change it to int(applied above) to follow the guidelines.
length_var.set(length_options[0])

# setting values for the dropdown
length_dropdown = tk.OptionMenu(window, length_var, *length_options)

# configuring the length dropdown
length_dropdown.config(fg="white", bg="#0f4c81", width=10, font=("Courier", 12))
length_dropdown["menu"].config(fg="white", bg="#0f4c81", font=("Courier", 12))
length_dropdown.grid(row=16, column=1, pady=10, sticky=W)

# Creating topics selection dropdown menu
topic_label = tk.Label(window, text="Topics involved", fg="white", bg="black")
topic_label.grid(row=22, column=0, pady=10, sticky=W)

# setting the range to be about to 1 to 10 distinct topics
topic_options = list(range(1, 10))
topic_var = tk.StringVar(window)

# setting default value to be 1
# Tkinter expects a string as dropdown options. So we need to change it to int(applied above) to follow the guidelines.
topic_var.set(topic_options[0])

# setting values for the dropdown
topic_dropdown = tk.OptionMenu(window, topic_var, *topic_options)

# configuring the topic dropdown
topic_dropdown.config(fg="white", bg="#0f4c81", width=10, font=("Courier", 12))
topic_dropdown["menu"].config(fg="white", bg="#0f4c81", font=("Courier", 12))
topic_dropdown.grid(row=22, column=1, pady=10, sticky=W)

# Creating generate summary button and using the above created themed style
generate_button = ttk.Button(window, text="Generate Summary", command=generate_summary, style="TButton")
generate_button.grid(row=100, column=1, pady=10, sticky=W)

# Create a text box that can be scrolled for output/summary of user text
output_textbox = scrolledtext.ScrolledText(window, width=40, height=15, wrap=tk.WORD)

# configuring the output text box
output_textbox.config(background='#0f4c81',
                      foreground='gold',
                      font=('Courier', 14, 'italic'),
                      relief="groove",
                      borderwidth=2)
output_textbox.grid(row=170, column=0, padx=10, pady=20, ipadx=5, ipady=5)


# Our Extended work
def user_satisfaction():
    # reading the variable
    selected = satisfaction_var.get()
    # if user selects "Yes" then just insert the below text.
    if selected == 1:
        user_textbox.delete(1.0, tk.END)
        user_textbox.insert(tk.END, "Thanks for confirming! Hope you liked the generated summary.")
    # if user selects "No" then requesting user to try changing the lengths/topics to check if user could get one.
    else:
        user_textbox.delete(1.0, tk.END)
        user_textbox.insert(tk.END, "Thanks for letting us know! We value your feedback. Please try changing the "
                                    "length/topics to check if you get desired summary.")


# creating a variable
satisfaction_var = tk.IntVar()

# creating the Label to ask the user
user_label = tk.Label(window, text="Are you satisfied with the summary?", fg="white", bg="black")
user_label.grid(row=190, column=0, pady=10, sticky=W)

# creating the radio buttons with themed Tkinter using the above defined style
yes_button = ttk.Radiobutton(window, text="Yes", variable=satisfaction_var, value=1, command=user_satisfaction)
no_button = ttk.Radiobutton(window, text="No", variable=satisfaction_var, value=0, command=user_satisfaction)

# aligning them in UI
yes_button.grid(row=190, column=1, pady=10, sticky=W)
no_button.grid(row=190, column=2, pady=20, sticky=W)

# text box for giving suggestions
user_textbox = scrolledtext.ScrolledText(window, width=100, height=1, wrap=tk.WORD)

# configuring the text box
user_textbox.config(background='#0f4c81',
                    foreground='gold',
                    font=('Courier', 10, 'italic'),
                    relief="groove",
                    borderwidth=2)
user_textbox.grid(row=195, column=0, padx=10, pady=20, ipadx=5, ipady=5)


# Start GUI loop
window.mainloop()