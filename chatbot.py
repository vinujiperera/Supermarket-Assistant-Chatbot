import tkinter as tk
from tkinter import messagebox, scrolledtext
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Error: Failed to load NLP model.")

# Database
inventory = {
    "apples": "Shelf 1 (Produce)",
    "bananas": "Shelf 1 (Produce)",
    "milk": "Shelf 3 (Dairy)",
    "bread": "Shelf 2 (Bakery)",
    "soap": "Shelf 5 (Personal Care)",
    "shampoo": "Shelf 5 (Personal Care)",
    "eggs": "Shelf 3 (Dairy)",
    "cheese": "Shelf 3 (Dairy)",
    "chocolate": "Shelf 4 (Snacks)",
    "coffee": "Shelf 4 (Beverages)",
    "pasta": "Shelf 2 (Pantry)",
    "rice": "Shelf 2 (Pantry)",
    "cake": "Shelf 2 (Bakery)",
    "body wash": "Shelf 5 (Personal Care)",
    "perfume": "Shelf 5 (Personal Care)",
    "soft drinks": "Shelf 4 (Beverages)",
    "marshmellows": "Shelf 4 (Snacks)",
}


BG_COLOR = "#f4f7f6"        
HEADER_COLOR = "#0a0a9e"    
ACCENT_BLUE = "#05118D"     
TEXT_COLOR = "#101010"      
WHITE = "#ffffff"

class SupermarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Basket Buddy")
        self.root.geometry("500x600")
        self.root.configure(bg=BG_COLOR)
        
        
        self.main_frame = tk.Frame(root, bg=BG_COLOR, padx=30, pady=20)
        self.main_frame.pack(expand=True, fill="both")

       
        self.header = tk.Label(
            self.main_frame, 
            text="🛒 Basket Buddy", 
            font=("Trebuchet MS", 24, "bold"), 
            fg=HEADER_COLOR, 
            bg=BG_COLOR
        )
        self.header.pack(pady=(0, 5))

        self.subtitle = tk.Label(
            self.main_frame, 
            text="Your Smart Supermarket Guide", 
            font=("Helvetica", 10, "italic"), 
            fg="#7f8c8d", 
            bg=BG_COLOR
        )
        self.subtitle.pack(pady=(0, 20))

        
        self.instr = tk.Label(
            self.main_frame, 
            text="What are you looking for today?", 
            font=("Helvetica", 11), 
            fg=TEXT_COLOR, 
            bg=BG_COLOR
        )
        self.instr.pack(anchor="w")

        self.user_input = tk.Entry(
            self.main_frame, 
            font=("Helvetica", 12), 
            width=40, 
            bd=0, 
            highlightthickness=1, 
            highlightbackground="#bdc3c7"
        )
        self.user_input.pack(pady=10, ipady=8)
        self.user_input.bind('<Return>', lambda event: self.process_items())

       
        self.search_btn = tk.Button(
            self.main_frame, 
            text="Find My Items", 
            command=self.process_items, 
            bg=ACCENT_BLUE, 
            fg=WHITE, 
            font=("Helvetica", 11, "bold"), 
            activebackground="#2980b9", 
            activeforeground=WHITE,
            cursor="hand2", 
            bd=0, 
            padx=20, 
            pady=10
        )
        self.search_btn.pack(pady=10)

       
        self.res_label = tk.Label(self.main_frame, text="Location Results:", font=("Helvetica", 10, "bold"), bg=BG_COLOR, fg=HEADER_COLOR)
        self.res_label.pack(anchor="w", pady=(10, 0))

        
        self.result_area = scrolledtext.ScrolledText(
            self.main_frame, 
            width=50, 
            height=10, 
            font=("Consolas", 10), 
            bg=WHITE, 
            fg=TEXT_COLOR,
            bd=0,
            padx=10,
            pady=10,
            highlightthickness=1,
            highlightbackground="#dcdde1"
        )
        self.result_area.pack(pady=10)
        
        
        self.button_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame.pack(pady=10)

        self.print_btn = tk.Button(
            self.button_frame, 
            text="📄 Save Shelf List", 
            command=self.print_summary, 
            state=tk.DISABLED,
            font=("Helvetica", 10),
            bg="#95a5a6",
            fg=WHITE,
            bd=0,
            padx=15,
            pady=5
        )
        self.print_btn.pack(side="left", padx=5)

        self.current_results = "" 

    def process_items(self):
        text = self.user_input.get().lower()
        if not text.strip():
            messagebox.showwarning("Empty Search", "Please enter some items first!")
            return

        doc = nlp(text)
        found_results = []

        # NLP logic
        for chunk in doc.noun_chunks:
            c_text = chunk.text.strip()
            if c_text in inventory:
                found_results.append((c_text, inventory[c_text]))

        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] or token.lemma_ in inventory:
                item = token.lemma_ if token.lemma_ in inventory else token.text
                if item in inventory:
                    found_results.append((item, inventory[item]))

        # Display Results
        self.result_area.delete('1.0', tk.END)
        unique_results = list(set(found_results))

        if not unique_results:
            self.result_area.insert(tk.END, "❌ No items found.")
            self.print_btn.config(state=tk.DISABLED, bg="#95a5a6")
        else:
            header_text = f"{'ITEM':<20} {'LOCATION':<20}\n"
            header_text += "-" * 40 + "\n"
            self.result_area.insert(tk.END, header_text)
            
            self.current_results = "--- BASKET BUDDY RECEIPT ---\n\n" + header_text
            
            for item, shelf in unique_results:
                line = f"{item.title():<20} {shelf:<20}\n"
                self.result_area.insert(tk.END, line)
                self.current_results += line
            
            self.result_area.insert(tk.END, "\n Ready to shop!")
            self.print_btn.config(state=tk.NORMAL, bg="#2ecc71") 

    def print_summary(self):
        with open("basket_buddy_list.txt", "w") as f:
            f.write(self.current_results)
        messagebox.showinfo("List saved to basket_buddy_list.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = SupermarketApp(root)
    root.mainloop()