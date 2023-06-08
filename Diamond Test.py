import tkinter as tk
import psycopg2
from tkinter import ttk

host = "127.0.0.1"
user = "postgres"
password = "qwerty"
db_name = "anime_db"

root = tk.Tk()
root.title("Аниме Справочник")
root.configure(background='light green')
root.resizable(False, False)

connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
)
connection.autocommit = True
cursor = connection.cursor()

def show_details():
    selected_item = treeview.focus()
    anime_details = treeview.item(selected_item)
    details_text.delete("1.0", tk.END)
    if 'values' in anime_details:
        values = anime_details['values']
        if len(values) >= 1:
            details_text.insert(tk.END, f"Описание: {values[2]}\n")

def add_window():
    def add_entry():
        name = name1_entry.get()
        year = year1_entry.get()
        genre = genre1_entry.get()
        description = description1_entry.get()

        if name and year and genre and description:
            insert_query = "INSERT INTO anime_table (anime_name, age_vyh, genre, soderjanie) VALUES (%s, %s, %s, %s)"
            data = (name, year, genre, description)
            cursor.execute(insert_query, data)
            connection.commit()
            name1_entry.delete(0, tk.END)
            year1_entry.delete(0, tk.END)
            genre1_entry.delete(0, tk.END)
            description1_entry.delete(0, tk.END)
            output_table()
        window_add.destroy()

    window_add = tk.Tk()
    window_add.title("Добавление записи")
    window_add.geometry("400x300")
    window_add.configure(background='light green')
    window_add.resizable(False, False)
    redac_label = ttk.Label(window_add, text="Название:", background='light green')
    redac_label.pack()
    name1_entry = ttk.Entry(window_add)
    name1_entry.pack()

    year1_label = ttk.Label(window_add, text="Год:", background='light green')
    year1_label.pack()
    year1_entry = ttk.Entry(window_add)
    year1_entry.pack()

    genre1_label = ttk.Label(window_add, text="Жанр:", background='light green')
    genre1_label.pack()
    genre1_entry = ttk.Entry(window_add)
    genre1_entry.pack()

    description1_label = ttk.Label(window_add, text="Описание:", background='light green')
    description1_label.pack()
    description1_entry = ttk.Entry(window_add)
    description1_entry.pack()

    add1_button = tk.Button(window_add, text="Добавить", font=("Helvetica", 15), command=add_entry, bg='aquamarine')
    add1_button.pack(pady=5)


def delete_entry():
    selected_item = treeview.focus()
    if selected_item:
        anime_name = treeview.item(selected_item, "text")
        delete_query = "DELETE FROM anime_table WHERE anime_name = %s"
        cursor.execute(delete_query, (anime_name,))
        connection.commit()
        treeview.delete(selected_item)
        output_table()

def edit_window():
    def update_entry():
        selected_item = treeview.focus()
        if selected_item:
            name = name_entry.get()
            year = year_entry.get()
            genre = genre_entry.get()
            description = description_entry.get()

            if name and year and genre and description:
                update_query = "UPDATE anime_table SET age_vyh = %s, genre = %s, soderjanie = %s WHERE anime_name = %s"
                data = (year, genre, description, name)
                cursor.execute(update_query, data)
                connection.commit()
                treeview.item(selected_item, text=name, values=(year, genre, description))
                output_table()
                edit_window.destroy()

    selected_item = treeview.focus()
    if selected_item:
        edit_window = tk.Toplevel(root)
        edit_window.title("Редактирование записи")
        edit_window.geometry("400x300")
        edit_window.configure(background='light green')
        edit_window.resizable(False, False)
        anime_details = treeview.item(selected_item)
        values = anime_details['values']

        name_label = ttk.Label(edit_window, text="Название:", background='light green')
        name_label.pack()
        name_entry = ttk.Entry(edit_window)
        name_entry.pack()
        name_entry.insert(tk.END, anime_details['text'])

        year_label = ttk.Label(edit_window, text="Год:", background='light green')
        year_label.pack()
        year_entry = ttk.Entry(edit_window)
        year_entry.pack()
        year_entry.insert(tk.END, values[0])

        genre_label = ttk.Label(edit_window, text="Жанр:", background='light green')
        genre_label.pack()
        genre_entry = ttk.Entry(edit_window)
        genre_entry.pack()
        genre_entry.insert(tk.END, values[1])

        description_label = ttk.Label(edit_window, text="Описание:", background='light green')
        description_label.pack()
        description_entry = ttk.Entry(edit_window)
        description_entry.pack()
        description_entry.insert(tk.END, values[2])

        save_button = tk.Button(edit_window, text="Сохранить", font=("Helvetica", 15), command=update_entry, bg='light goldenrod')
        save_button.pack(pady=5)

def output_table():
    treeview.delete(*treeview.get_children())
    select_query = "SELECT * FROM anime_table"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        name = row[0]
        year = row[1]
        genre = row[2]
        description = row[3]
        treeview.insert("", tk.END, text=name, values=(year, genre, description))

treeview = ttk.Treeview(root)
treeview["columns"] = ("year", "genre", "description")
treeview.heading("#0", text="Название")
treeview.heading("year", text="Год")
treeview.heading("genre", text="Жанр")
treeview.heading("description", text="Описание")
treeview.pack(pady=10)


details_text = tk.Text(root, height=4, width=40)
details_text.pack(pady=5)

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg='light green')
button_frame.pack(pady=5)

details_button = tk.Button(button_frame, text="Показать детали", font=("Helvetica", 15), command=show_details, bg='light blue')
details_button.grid(row=0, column=0, padx=5)

add_button = tk.Button(button_frame, text="Добавить", font=("Helvetica", 15), command=add_window, bg='aquamarine')
add_button.grid(row=0, column=1, padx=5)

edit_button = tk.Button(button_frame, text="Редактировать", font=("Helvetica", 15), command=edit_window, bg='light goldenrod')
edit_button.grid(row=0, column=2, padx=5)

delete_button = tk.Button(button_frame, text="Удалить", font=("Helvetica", 15), command=delete_entry, bg='coral1')
delete_button.grid(row=0, column=3, padx=5)

output_button = tk.Button(button_frame, text="Выйти?", font=("Helvetica", 15), command=root.destroy, bg='tomato3')
output_button.grid(row=0, column=4, padx=5)

def on_closing():
    cursor.close()
    connection.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
output_table()
root.mainloop()

