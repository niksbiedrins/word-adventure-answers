import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import re

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Adventure's Answer Viewer")
        self.iconbitmap("logo.ico")
        self.image_label = tk.Label(self)
        self.image_label.pack()
        self.level = 20
        self.month = 10

        self.last_word_label = tk.Label(self, text="Last Word:", font=("Helvetica", 14, "bold"))
        self.last_word_label.pack()

        self.word_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.word_label.pack()

        self.level_label = tk.Label(self, text=f"Level: {self.level}")
        self.level_label.pack()

        self.month_label = tk.Label(self, text=f"Month: {self.month}")
        self.month_label.pack()

        back_button = tk.Button(self, text="Back", command=self.previous_image)
        back_button.pack(side="left")

        next_button = tk.Button(self, text="Next", command=self.next_image)
        next_button.pack(side="right")

        self.level_entry = tk.Entry(self)
        self.level_entry.pack()

        go_to_button = tk.Button(self, text="Go To", command=self.go_to_level)
        go_to_button.pack()

        self.display_image_and_extract_word()

    def display_image_and_extract_word(self):
        image_url = f"https://www.realqunb.com/wp-content/uploads/2023/{self.month:02d}/Word-Farm-Adventure-Level-{self.level}-Answers.jpeg"
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((400, 500))
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.level_label.config(text=f"Level: {self.level}")
        self.month_label.config(text=f"Month: {self.month}")

        website_url = f"https://www.realqunb.com/word-farm-adventure-level-{self.level}-answers/"
        phrase_to_search = "LAST WORD:"
        extracted_word = self.find_last_word_after_phrase(website_url, phrase_to_search)
        self.word_label.config(text=f"{extracted_word}", font=("Helvetica", 12, "bold"))

    def next_image(self):
        if self.level < 1200:
            self.level += 1
            if self.level > 270:
                self.month = 11
            self.display_image_and_extract_word()

    def previous_image(self):
        if self.level > 20:
            self.level -= 1
            if self.level <= 270:
                self.month = 10
            self.display_image_and_extract_word()

    def go_to_level(self):
        try:
            new_level = int(self.level_entry.get())
            if 20 <= new_level <= 1200:
                self.level = new_level
                if self.level > 270:
                    self.month = 11
                else:
                    self.month = 10
                self.display_image_and_extract_word()
        except ValueError:
            pass

    def find_last_word_after_phrase(self, url, phrase):
        try:
            # Fetch the website content
            response = requests.get(url)
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find all text on the page
            text = ' '.join(soup.stripped_strings)
            # Look for the phrase
            match = re.search(rf'{phrase}\s*([^\s]+)', text, re.IGNORECASE)
            if match:
                last_word = match.group(1)
                extracted_word = last_word.replace("LAST WORD: ", "")
                print(f"Found '{phrase}{last_word}' on the website.")
                print(f"Extracted word: {extracted_word}")
                return extracted_word
            else:
                print(f"Did not find '{phrase}' followed by a word on the website.")
                return ""
        except Exception as e:
            print("An error occurred: " + str(e))
            return ""

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
