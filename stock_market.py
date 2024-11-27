import yfinance as yf
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class StockMarket:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.price = self.get_current_price()

    def get_current_price(self):
        stock = yf.Ticker(self.symbol)
        return stock.history(period="1d")['Close'].iloc[-1]

    def __repr__(self):
        return f"{self.name} ({self.symbol}): Preț={self.price:.2f}"

stock_data = [
    StockMarket("NVDA", "NVIDIA Corporation"),
    StockMarket("NFLX", "Netflix, Inc."),
    StockMarket("AAPL", "Apple Inc."),
    StockMarket("TSLA", "Tesla, Inc."),
    StockMarket("MSFT", "Microsoft Corporation"),
    StockMarket("META", "Meta Platforms, Inc."),
    StockMarket("AMZN", "Amazon.com, Inc."),
    StockMarket("AMD", "Advanced Micro Devices, Inc."),
    StockMarket("AVGO", "Broadcom Inc."),
    StockMarket("MSTR", "MicroStrategy Incorporated"),
    StockMarket("CVS", "CVS Health Corporation"),
    StockMarket("GOOG", "Alphabet Inc."),
    StockMarket("ISRG", "Intuitive Surgical, Inc."),
    StockMarket("AXP", "American Express Company"),
    StockMarket("UNH", "UnitedHealth Group Incorporated"),
    StockMarket("COIN", "Coinbase Global, Inc."),
    StockMarket("LLY", "Eli Lilly and Company"),
    StockMarket("MU", "Micron Technology, Inc."),
    StockMarket("PG", "Procter & Gamble Company"),
    StockMarket("JPM", "JP Morgan Chase")
]

class User:
    def __init__(self, username):
        self.username = username
        self.portfolio = {}

    def buy_stock(self, stock, quantity):
        if stock.symbol in self.portfolio:
            self.portfolio[stock.symbol] += quantity
        else:
            self.portfolio[stock.symbol] = quantity
        messagebox.showinfo("Achiziție", f"Ai cumpărat {quantity} acțiuni din {stock.name}.")

    def sell_stock(self, stock, quantity):
        if stock.symbol in self.portfolio and self.portfolio[stock.symbol] >= quantity:
            self.portfolio[stock.symbol] -= quantity
            if self.portfolio[stock.symbol] == 0:
                del self.portfolio[stock.symbol]
            messagebox.showinfo("Vânzare", f"Ai vândut {quantity} acțiuni din {stock.name}.")
        else:
            messagebox.showwarning("Eroare", f"Nu ai suficiente acțiuni din {stock.name} pentru a vinde.")

    def portfolio_value(self):
        total_value = 0
        for symbol, quantity in self.portfolio.items():
            stock = next((s for s in stock_data if s.symbol == symbol), None)
            if stock:
                total_value += stock.get_current_price() * quantity
        return total_value

class StockApp:
    def __init__(self, root):
        self.user = User("Meltis")
        self.root = root
        self.root.title("Simulare Piață de Acțiuni")
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("Symbol", "Name", "Price"), show="headings")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for stock in stock_data:
            self.tree.insert("", tk.END, values=(stock.symbol, stock.name, f"${stock.price:.2f}"))

        self.filter_entry = ttk.Entry(self.root)
        self.filter_entry.pack()
        self.filter_button = ttk.Button(self.root, text="Filtrează", command=self.filter_stocks)
        self.filter_button.pack()

        self.range_button = ttk.Button(self.root, text="Filtrează după interval de preț", command=self.filter_stocks_by_range)
        self.range_button.pack()

        self.buy_button = ttk.Button(self.root, text="Cumpără", command=self.buy_stock)
        self.buy_button.pack()

        self.sell_button = ttk.Button(self.root, text="Vinde", command=self.sell_stock)
        self.sell_button.pack()

        self.portfolio_button = ttk.Button(self.root, text="Portofoliu", command=self.show_portfolio)
        self.portfolio_button.pack()

    def filter_stocks(self):
        query = self.filter_entry.get().upper()
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtered_stocks = [stock for stock in stock_data if query in stock.symbol or query in stock.name.upper()]
        for stock in filtered_stocks:
            self.tree.insert("", tk.END, values=(stock.symbol, stock.name, f"${stock.price:.2f}"))

    def filter_stocks_by_range(self):
        min_price = simpledialog.askfloat("Interval minim", "Introdu valoarea minimă:")
        max_price = simpledialog.askfloat("Interval maxim", "Introdu valoarea maximă:")

        if min_price is not None and max_price is not None:
            for item in self.tree.get_children():
                self.tree.delete(item)

            filtered_stocks = [stock for stock in stock_data if min_price <= stock.price <= max_price]
            for stock in filtered_stocks:
                self.tree.insert("", tk.END, values=(stock.symbol, stock.name, f"${stock.price:.2f}"))

    def buy_stock(self):
        selected_item = self.tree.selection()
        if selected_item:
            stock_symbol = self.tree.item(selected_item, "values")[0]
            stock = next((s for s in stock_data if s.symbol == stock_symbol), None)
            if stock:
                quantity = self.get_quantity_input("Cumpără")
                if quantity:
                    self.user.buy_stock(stock, quantity)
        else:
            messagebox.showwarning("Atenție", "Te rog selectează un stoc pentru a cumpăra.")

    def sell_stock(self):
        selected_item = self.tree.selection()
        if selected_item:
            stock_symbol = self.tree.item(selected_item, "values")[0]
            stock = next((s for s in stock_data if s.symbol == stock_symbol), None)
            if stock:
                quantity = self.get_quantity_input("Vinde")
                if quantity:
                    self.user.sell_stock(stock, quantity)
        else:
            messagebox.showwarning("Atenție", "Te rog selectează un stoc pentru a vinde.")

    def get_quantity_input(self, action):
        quantity = simpledialog.askinteger(action, f"Câte acțiuni dorești să {action.lower()}?", minvalue=1)
        return quantity

    def show_portfolio(self):
        portfolio_str = f"Valoarea totală: ${self.user.portfolio_value():.2f}\n\nPortofoliu:\n"
        for symbol, quantity in self.user.portfolio.items():
            stock = next((s for s in stock_data if s.symbol == symbol), None)
            if stock:
                portfolio_str += f"{stock.name} ({symbol}): {quantity} acțiuni\n"
        messagebox.showinfo("Portofoliu", portfolio_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
