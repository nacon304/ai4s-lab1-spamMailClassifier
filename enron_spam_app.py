import re
import nltk
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import filedialog, messagebox
from pandastable import Table, Toplevel

nltk.data.path.append('nltk_data')
nltk.download('stopwords', download_dir='nltk_data')
nltk.download('wordnet', download_dir='nltk_data') # (if errors occur, wordnet pkg may need unzipped manually)
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class SpamHamPredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Spam/Ham Prediction")
        self.root.geometry("500x400")

        # Load model and encoder
        self.model = joblib.load('model/enron_spam_pipeline.pkl')
        # self.encoder = joblib.load('enron_spam_label_encoder.pkl')
        self.loaded_emails_df = None

        self.lemmatizer = WordNetLemmatizer()
        self.stopwords = set(stopwords.words('english'))

        # Initialize UI components
        self.create_menu()
        self.create_inputs()
        self.create_result_box()
        self.create_buttons()

    def create_menu(self):
        # Create Menu Bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Add 'File' menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load CSV", command=self.load_csv_file)
        menu_bar.add_command(label='Exit', command=self.root.destroy)

    def create_inputs(self):
        # Subject input
        subject_label = tk.Label(self.root, text="Subject")
        subject_label.pack(pady=5)
        self.subject_entry = tk.Text(self.root, height=2, width=40)
        self.subject_entry.pack(pady=5)

        # Message input
        message_label = tk.Label(self.root, text="Message")
        message_label.pack(pady=5)
        self.message_entry = tk.Text(self.root, height=2, width=40)
        self.message_entry.pack(pady=5)

        # Frame for email listbox and the "Display emails" button
        email_lists_frame = tk.Frame(self.root)
        email_lists_frame.pack(pady=10)

        display_emails_df_button = tk.Button(email_lists_frame, text="All emails", command=self.display_emails_df)
        display_emails_df_button.grid(row=0, column=1, padx=5)

        email_list_label = tk.Label(email_lists_frame, text="Loaded Emails (from CSV):")
        email_list_label.grid(row=0, column=0, padx=5)

        self.email_listbox = tk.Text(self.root, height=2, width=40)
        self.email_listbox.pack(pady=5)

    def create_buttons(self):
        # Button frame for Predict Single and Predict Multiple buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Predict Single button
        predict_button = tk.Button(button_frame, text="Predict Single", command=self.predict_single_action)
        predict_button.grid(row=0, column=0, padx=5)

        # Predict Multiple button
        predict_multiple_button = tk.Button(button_frame, text="Pred & Eval", command=self.predict_and_eval_multiple_emails)
        predict_multiple_button.grid(row=0, column=1, padx=5)

    def create_result_box(self):
        # Result text box
        result_text_label = tk.Label(self.root, text="Result:")
        result_text_label.pack(pady=5)
        self.result_text = tk.Text(self.root, height=1, width=40)
        self.result_text.pack(pady=10)

    # Function to normalize text
    def norm_text(self, text):
        text = re.sub(r'\\r\\n', ' ', text)
        text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^b\s+', '', text)
        text = text.lower()
        text = [word for word in text.split() if word not in self.stopwords]
        text = " ".join([self.lemmatizer.lemmatize(word) for word in text])
        return text

    # Function to load CSV file with multiple emails
    def load_csv_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.loaded_emails_df = pd.read_csv(file_path)
                # the csv file should have 3 columns: 'Subject', 'Message', 'Spam/Ham'
                self.loaded_emails_df = self.loaded_emails_df[['Subject', 'Message', 'Spam/Ham']]
                self.loaded_emails_df = self.loaded_emails_df.dropna(subset=['Subject', 'Message'], how='all')
                self.loaded_emails_df.drop_duplicates(inplace=True)
                self.loaded_emails_df.reset_index(drop=True, inplace=True)
                self.loaded_emails_df['Subject'] = self.loaded_emails_df['Subject'].fillna('').apply(self.norm_text)
                self.loaded_emails_df['Message'] = self.loaded_emails_df['Message'].fillna('').apply(self.norm_text)
                
                self.email_listbox.delete(1.0, tk.END)
                self.result_text.delete(1.0, tk.END)
                self.email_listbox.insert(tk.END, f"Loaded {len(self.loaded_emails_df)} emails from {file_path}.")
            except Exception as e:
                messagebox.showerror("File Error", f"Error loading file: {str(e)}")

    def display_emails_df(self):
        if self.loaded_emails_df is None:
            messagebox.showerror("File Error", "Please load a CSV file first.")
            return

        frame = Toplevel(self.root)
        table = Table(frame, dataframe=self.loaded_emails_df, showtoolbar=True, showstatusbar=True, width=800, height=600)
        table.show()

    # Function for single prediction
    def predict_single_action(self):
        subject = self.subject_entry.get('1.0', 'end-1c')
        message = self.message_entry.get('1.0', 'end-1c')

        if not subject and not message:
            messagebox.showerror("Input Error", "Both Subject and Message are not available.")
            return

        # Get prediction
        prediction = self.predict_single(subject, message)

        # Display prediction in the result box
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Prediction: {prediction}")

    # Predict Single Email
    def predict_single(self, subject, message) -> str:
        sample = pd.DataFrame({
            'Subject': [subject],
            'Message': [message]
        })
        sample['Subject'] = sample['Subject'].fillna('').apply(self.norm_text)
        sample['Message'] = sample['Message'].fillna('').apply(self.norm_text)
        sample['email'] = sample['Subject'] + " " + sample['Message']

        pred = self.model.predict(sample['email'])
        pred = ['Spam' if x == 1 else 'Ham' for x in pred]
        return pred[0]

    # Predict and evaluate multiple emails
    def predict_and_eval_multiple_emails(self):
        if self.loaded_emails_df is None:
            messagebox.showerror("File Error", "Please load a CSV file first.")
            return

        # Perform predicting and evaluation
        try:
            X_val = self.loaded_emails_df['Subject'] + " " + self.loaded_emails_df['Message']
            y_val = self.loaded_emails_df['Spam/Ham'].apply(lambda x: 1 if x == 'spam' else 0)

            pred = self.model.predict(X_val)
            accuracy = accuracy_score(y_val, pred)
            pred = ['spam' if x == 1 else 'ham' for x in pred]
            self.loaded_emails_df['Prediction'] = pred

            # Display the accuracy in the result box
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Accuracy: {accuracy:.9f}")

        except Exception as e:
            messagebox.showerror("Prediction Error", f"Error predicting multiple emails: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpamHamPredictionApp(root)
    root.mainloop()
