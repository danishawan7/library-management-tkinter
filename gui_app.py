import tkinter as tk
from tkinter import messagebox, simpledialog
from book_library import Book, EBook, Library, BookNotAvailableError

library = Library()

root = tk.Tk()
root.title("Library Management System")
root.geometry("700x600")

def toggle_size_entry():
    if ebook_var.get():
        size_entry.config(state="normal")
    else:
        size_entry.delete(0, tk.END)
        size_entry.config(state="disabled")

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    isbn = isbn_entry.get()
    is_ebook = ebook_var.get()
    size = size_entry.get()

    if not title or not author or not isbn:
        messagebox.showerror("Error", "Title, Author, and ISBN are required.")
        return

    if is_ebook:
        if not size or not size.isdigit():
            messagebox.showerror("Error", "Please enter a valid download size (number) for the eBook.")
            return
        book = EBook(title, author, isbn, int(size))
    else:
        book = Book(title, author, isbn)

    library.add_book(book)
    messagebox.showinfo("Success", f"Book '{title}' added.")
    update_book_list()

def lend_book():
    isbn = simpledialog.askstring("Lend Book", "Enter ISBN of the book to lend:")
    if isbn:
        try:
            library.lend_book(isbn)
            messagebox.showinfo("Success", "Book lent successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def return_book():
    isbn = simpledialog.askstring("Return Book", "Enter ISBN of the book to return:")
    if isbn:
        try:
            library.return_book(isbn)
            messagebox.showinfo("Success", "Book returned successfully.")
            update_book_list()
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

def remove_book():
    isbn = simpledialog.askstring("Remove Book", "Enter ISBN of the book to remove:")
    if isbn:
        library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed.")
        update_book_list()

def view_books_by_author():
    author = simpledialog.askstring("Search by Author", "Enter author's name:")
    if author:
        books = list(library.books_by_author(author))
        listbox.delete(0, tk.END)
        if books:
            listbox.insert(tk.END, f"Books by {author}:")
            for book in books:
                listbox.insert(tk.END, str(book))
        else:
            messagebox.showinfo("Not Found", "No books found by this author.")

def update_book_list():
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "Available Books:")
    for book in library:
        listbox.insert(tk.END, str(book))

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(frame, width=40)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Author:").grid(row=1, column=0, sticky="w")
author_entry = tk.Entry(frame, width=40)
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="ISBN:").grid(row=2, column=0, sticky="w")
isbn_entry = tk.Entry(frame, width=40)
isbn_entry.grid(row=2, column=1, padx=5, pady=5)

ebook_var = tk.BooleanVar()
ebook_check = tk.Checkbutton(frame, text="Is eBook?", variable=ebook_var, command=toggle_size_entry)
ebook_check.grid(row=3, column=0, sticky="w")

tk.Label(frame, text="Download Size (MB):").grid(row=4, column=0, sticky="w")
size_entry = tk.Entry(frame, width=20, state="disabled")
size_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

tk.Button(frame, text="Add Book", command=add_book, bg="#d0f0c0").grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Lend Book", command=lend_book).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Return Book", command=return_book).grid(row=7, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Remove Book", command=remove_book).grid(row=8, column=0, columnspan=2, pady=5)
tk.Button(frame, text="View Books by Author", command=view_books_by_author).grid(row=9, column=0, columnspan=2, pady=5)

tk.Label(root, text="Library Inventory", font=("Arial", 12, "bold")).pack(pady=(10, 0))
listbox = tk.Listbox(root, width=80, height=10)
listbox.pack(pady=10)

update_book_list()
root.mainloop()
