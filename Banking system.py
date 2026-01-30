import tkinter as tk
from tkinter import messagebox
import os
import winsound

# ---------------- SETTINGS ----------------
DATA_FILE = "bank_data.txt"
TRANS_FILE = "transactions.txt"
accounts = {}
dark_mode = True

# ---------------- SOUND ----------------
def click():
    winsound.Beep(1000, 80)

# ---------------- FILE ----------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            for line in f:
                acc, name, pin, bal = line.strip().split(",")
                accounts[acc] = {"name": name, "pin": pin, "balance": float(bal)}

def save_data():
    with open(DATA_FILE, "w") as f:
        for acc, d in accounts.items():
            f.write(f"{acc},{d['name']},{d['pin']},{d['balance']}\n")

def save_transaction(acc, t, amt, bal):
    with open(TRANS_FILE, "a") as f:
        f.write(f"{acc} | {t} | ₹{amt} | Balance ₹{bal}\n")

# ---------------- THEME ----------------
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    bg = "#0f172a" if dark_mode else "#fef3c7"
    card = "#1e293b" if dark_mode else "#ffffff"
    fg = "white" if dark_mode else "#1e293b"

    root.config(bg=bg)
    title.config(bg=bg, fg=fg)
    card_frame.config(bg=card)

# ---------------- ACCOUNT ----------------
def create_account():
    click()
    acc, name, pin = acc_e.get(), name_e.get(), pin_e.get()

    if not acc or not name or not pin:
        messagebox.showwarning("⚠️", "Fill all fields")
        return

    if acc in accounts:
        messagebox.showerror("❌", "Account already exists")
        return

    accounts[acc] = {"name": name, "pin": pin, "balance": 0}
    save_data()
    messagebox.showinfo("✅", "Account Created!")

def login():
    click()
    acc, pin = acc_e.get(), pin_e.get()
    if acc in accounts and accounts[acc]["pin"] == pin:
        dashboard(acc)
    else:
        messagebox.showerror("❌", "Invalid Login")

# ---------------- DASHBOARD ----------------
def dashboard(acc):
    d = tk.Toplevel()
    d.title("Dashboard")
    d.geometry("380x420")
    d.config(bg="#020617")

    tk.Label(d, text=f"👋 Hi {accounts[acc]['name']}",
             font=("Segoe UI", 16, "bold"),
             bg="#020617", fg="#38bdf8").pack(pady=15)

    amt_e = tk.Entry(d, font=("Segoe UI", 12))
    amt_e.pack(pady=10)

    def deposit():
        click()
        amt = float(amt_e.get())
        accounts[acc]["balance"] += amt
        save_data()
        save_transaction(acc, "Deposit", amt, accounts[acc]["balance"])
        messagebox.showinfo("💰", "Amount Deposited")

    def withdraw():
        click()
        amt = float(amt_e.get())
        if amt <= accounts[acc]["balance"]:
            accounts[acc]["balance"] -= amt
            save_data()
            save_transaction(acc, "Withdraw", amt, accounts[acc]["balance"])
            messagebox.showinfo("💸", "Withdrawal Successful")
        else:
            messagebox.showerror("❌", "Insufficient Balance")

    def balance():
        click()
        messagebox.showinfo("📊", f"Balance: ₹{accounts[acc]['balance']}")

    def history():
        h = tk.Toplevel()
        h.title("Transactions")
        h.geometry("420x300")
        text = tk.Text(h)
        text.pack(fill="both", expand=True)

        if os.path.exists(TRANS_FILE):
            with open(TRANS_FILE) as f:
                for line in f:
                    if acc in line:
                        text.insert("end", line)

    btn = lambda t, c, cmd: tk.Button(
        d, text=t, bg=c, fg="white",
        font=("Segoe UI", 11, "bold"),
        width=22, command=cmd).pack(pady=5)

    btn("💰 Deposit", "#22c55e", deposit)
    btn("💸 Withdraw", "#ef4444", withdraw)
    btn("📊 Check Balance", "#f59e0b", balance)
    btn("📜 Transaction History", "#6366f1", history)

# ---------------- ADMIN ----------------
def admin_login():
    click()
    if admin_u.get() == "admin" and admin_p.get() == "admin123":
        admin_panel()
    else:
        messagebox.showerror("❌", "Invalid Admin")

def admin_panel():
    a = tk.Toplevel()
    a.title("Admin Panel")
    a.geometry("420x350")
    text = tk.Text(a)
    text.pack(fill="both", expand=True)

    for acc, d in accounts.items():
        text.insert("end",
            f"Account: {acc}\nName: {d['name']}\nBalance: ₹{d['balance']}\n{'-'*30}\n")

# ---------------- MAIN UI ----------------
root = tk.Tk()
root.title("Smart Banking App")
root.geometry("480x720")
root.config(bg="#0f172a")

load_data()

title = tk.Label(root, text="🏦 SMART BANK",
                 font=("Segoe UI", 26, "bold"),
                 bg="#0f172a", fg="#38bdf8")
title.pack(pady=20)

card_frame = tk.Frame(root, bg="#1e293b", padx=25, pady=25)
card_frame.pack(pady=10)

lbl = lambda t: tk.Label(card_frame, text=t,
                         bg="#1e293b", fg="white",
                         font=("Segoe UI", 11)).pack(anchor="w")

lbl("Account Number")
acc_e = tk.Entry(card_frame, font=("Segoe UI", 12))
acc_e.pack(fill="x", pady=5)

lbl("Name")
name_e = tk.Entry(card_frame, font=("Segoe UI", 12))
name_e.pack(fill="x", pady=5)

lbl("PIN")
pin_e = tk.Entry(card_frame, show="*", font=("Segoe UI", 12))
pin_e.pack(fill="x", pady=5)

def main_btn(text, color, cmd):
    tk.Button(root, text=text, bg=color, fg="white",
              font=("Segoe UI", 12, "bold"),
              width=24, command=cmd).pack(pady=6)

main_btn("➕ Create Account", "#22c55e", create_account)
main_btn("🔐 Login", "#3b82f6", login)
main_btn("🌗 Toggle Theme", "#a855f7", toggle_theme)

tk.Label(root, text="👑 Admin Login",
         bg="#0f172a", fg="#facc15",
         font=("Segoe UI", 14, "bold")).pack(pady=10)

admin_u = tk.Entry(root)
admin_u.pack(pady=3)

admin_p = tk.Entry(root, show="*")
admin_p.pack(pady=3)

main_btn("⚙️ Admin Panel", "#ec4899", admin_login)
main_btn("❌ Exit", "#64748b", root.destroy)

root.mainloop()
