import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from support_handler import stock_handler

class StockAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analyzer - TSX Companies")
        self.root.geometry("1200x800")
        self.stock_handler = stock_handler()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TSX Stock Analyzer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Search section
        search_frame = ttk.LabelFrame(main_frame, text="Stock Search", padding="10")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 5))
        
        ttk.Label(search_frame, text="Enter Stock Symbol:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.symbol_var = tk.StringVar(value="CEU.TO")
        symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol_var, width=15)
        symbol_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.analyze_btn = ttk.Button(search_frame, text="Analyze Stock", command=self.analyze_stock)
        self.analyze_btn.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # Quick access buttons
        ttk.Label(search_frame, text="Quick Access:").grid(row=3, column=0, sticky=tk.W, pady=(15, 5))
        
        quick_stocks = ["CEU.TO", "CCO.TO", "TSAT.TO"]
        for i, stock in enumerate(quick_stocks):
            btn = ttk.Button(search_frame, text=stock, 
                           command=lambda s=stock: self.quick_analyze(s))
            btn.grid(row=4+i, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Export button
        export_btn = ttk.Button(search_frame, text="Export All TSX Symbols", 
                               command=self.export_symbols)
        export_btn.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        search_frame.columnconfigure(0, weight=1)
        
        # Results section with notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.create_result_tabs()
        
    def create_result_tabs(self):
        # Company Info Tab
        self.company_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.company_frame, text="Company Info")
        
        # Market & Valuation Tab
        self.market_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.market_frame, text="Market & Valuation")
        
        # Financial Performance Tab
        self.financial_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.financial_frame, text="Financial Performance")
        
        # Analysis Tab
        self.analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analysis_frame, text="Analysis & Recommendations")
        
        # Create content areas for each tab
        self.setup_company_tab()
        self.setup_market_tab()
        self.setup_financial_tab()
        self.setup_analysis_tab()
        
    def setup_company_tab(self):
        # Company information display
        self.company_text = scrolledtext.ScrolledText(self.company_frame, wrap=tk.WORD, 
                                                     height=20, width=70)
        self.company_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_market_tab(self):
        # Market data in a structured layout
        market_container = ttk.Frame(self.market_frame)
        market_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Market Cap section
        market_cap_frame = ttk.LabelFrame(market_container, text="Market Capitalization", padding="10")
        market_cap_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.market_cap_label = ttk.Label(market_cap_frame, text="Market Cap: -", font=("Arial", 12))
        self.market_cap_label.pack(anchor=tk.W)
        
        # Ratios section
        ratios_frame = ttk.LabelFrame(market_container, text="Valuation Ratios", padding="10")
        ratios_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pe_label = ttk.Label(ratios_frame, text="P/E Ratio (TTM): -")
        self.pe_label.pack(anchor=tk.W, pady=2)
        
        self.peg_label = ttk.Label(ratios_frame, text="PEG Ratio: -")
        self.peg_label.pack(anchor=tk.W, pady=2)
        
        self.pb_label = ttk.Label(ratios_frame, text="Price to Book: -")
        self.pb_label.pack(anchor=tk.W, pady=2)
        
        self.forward_pe_label = ttk.Label(ratios_frame, text="Forward P/E: -")
        self.forward_pe_label.pack(anchor=tk.W, pady=2)
        
        # Price section
        price_frame = ttk.LabelFrame(market_container, text="Price Information", padding="10")
        price_frame.pack(fill=tk.X)
        
        self.current_price_label = ttk.Label(price_frame, text="Current Price: -", font=("Arial", 12, "bold"))
        self.current_price_label.pack(anchor=tk.W, pady=2)
        
        self.week_high_label = ttk.Label(price_frame, text="52-Week High: -")
        self.week_high_label.pack(anchor=tk.W, pady=2)
        
        self.week_low_label = ttk.Label(price_frame, text="52-Week Low: -")
        self.week_low_label.pack(anchor=tk.W, pady=2)
        
    def setup_financial_tab(self):
        financial_container = ttk.Frame(self.financial_frame)
        financial_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Profitability section
        profit_frame = ttk.LabelFrame(financial_container, text="Profitability Metrics", padding="10")
        profit_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.roe_label = ttk.Label(profit_frame, text="Return on Equity (ROE): -")
        self.roe_label.pack(anchor=tk.W, pady=2)
        
        self.roa_label = ttk.Label(profit_frame, text="Return on Assets (ROA): -")
        self.roa_label.pack(anchor=tk.W, pady=2)
        
        self.profit_margin_label = ttk.Label(profit_frame, text="Profit Margin: -")
        self.profit_margin_label.pack(anchor=tk.W, pady=2)
        
        # Revenue & Earnings section
        revenue_frame = ttk.LabelFrame(financial_container, text="Revenue & Earnings", padding="10")
        revenue_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.revenue_label = ttk.Label(revenue_frame, text="Revenue (TTM): -")
        self.revenue_label.pack(anchor=tk.W, pady=2)
        
        self.gross_profit_label = ttk.Label(revenue_frame, text="Gross Profit: -")
        self.gross_profit_label.pack(anchor=tk.W, pady=2)
        
        self.net_income_label = ttk.Label(revenue_frame, text="Net Income: -")
        self.net_income_label.pack(anchor=tk.W, pady=2)
        
        # Balance Sheet section
        balance_frame = ttk.LabelFrame(financial_container, text="Balance Sheet", padding="10")
        balance_frame.pack(fill=tk.X)
        
        self.total_debt_label = ttk.Label(balance_frame, text="Total Debt: -")
        self.total_debt_label.pack(anchor=tk.W, pady=2)
        
        self.current_ratio_label = ttk.Label(balance_frame, text="Current Ratio: -")
        self.current_ratio_label.pack(anchor=tk.W, pady=2)
        
        self.debt_equity_label = ttk.Label(balance_frame, text="Debt to Equity: -")
        self.debt_equity_label.pack(anchor=tk.W, pady=2)
        
    def setup_analysis_tab(self):
        analysis_container = ttk.Frame(self.analysis_frame)
        analysis_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analyst Recommendations
        analyst_frame = ttk.LabelFrame(analysis_container, text="Analyst Recommendations", padding="10")
        analyst_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.recommendation_label = ttk.Label(analyst_frame, text="Recommendation: -", font=("Arial", 12, "bold"))
        self.recommendation_label.pack(anchor=tk.W, pady=2)
        
        self.target_mean_label = ttk.Label(analyst_frame, text="Target Mean Price: -")
        self.target_mean_label.pack(anchor=tk.W, pady=2)
        
        self.target_high_label = ttk.Label(analyst_frame, text="Target High Price: -")
        self.target_high_label.pack(anchor=tk.W, pady=2)
        
        self.target_low_label = ttk.Label(analyst_frame, text="Target Low Price: -")
        self.target_low_label.pack(anchor=tk.W, pady=2)
        
        # Dividends section
        dividend_frame = ttk.LabelFrame(analysis_container, text="Dividend Information", padding="10")
        dividend_frame.pack(fill=tk.X)
        
        self.dividend_yield_label = ttk.Label(dividend_frame, text="Dividend Yield: -")
        self.dividend_yield_label.pack(anchor=tk.W, pady=2)
        
        self.dividend_rate_label = ttk.Label(dividend_frame, text="Dividend Rate: -")
        self.dividend_rate_label.pack(anchor=tk.W, pady=2)
        
        self.payout_ratio_label = ttk.Label(dividend_frame, text="Payout Ratio: -")
        self.payout_ratio_label.pack(anchor=tk.W, pady=2)
        
    def quick_analyze(self, symbol):
        self.symbol_var.set(symbol)
        self.analyze_stock()
        
    def analyze_stock(self):
        symbol = self.symbol_var.get().strip()
        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol")
            return
            
        # Disable button during analysis
        self.analyze_btn.config(state="disabled", text="Analyzing...")
        
        # Run analysis in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._analyze_stock_thread, args=(symbol,))
        thread.daemon = True
        thread.start()
        
    def _analyze_stock_thread(self, symbol):
        try:
            info = self.stock_handler.get_company_info(symbol)
            # Update GUI in main thread
            self.root.after(0, self._update_display, info, symbol)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
            
    def _update_display(self, info, symbol):
        try:
            # Update Company Info tab
            company_info = f"""Company: {info.get('longName', 'N/A')} ({symbol})

Sector: {info.get('sector', 'N/A')}
Industry: {info.get('industry', 'N/A')}
Exchange: {info.get('exchange', 'N/A')}
Website: {info.get('website', 'N/A')}

Business Summary:
{info.get('longBusinessSummary', 'No description available')[:500]}..."""
            
            self.company_text.delete(1.0, tk.END)
            self.company_text.insert(tk.END, company_info)
            
            # Update Market & Valuation tab
            self.market_cap_label.config(text=f"Market Cap: {self._format_number(info.get('marketCap'))}")
            self.pe_label.config(text=f"P/E Ratio (TTM): {self._format_ratio(info.get('trailingPE'))}")
            self.peg_label.config(text=f"PEG Ratio: {self._format_ratio(info.get('pegRatio'))}")
            self.pb_label.config(text=f"Price to Book: {self._format_ratio(info.get('priceToBook'))}")
            self.forward_pe_label.config(text=f"Forward P/E: {self._format_ratio(info.get('forwardPE'))}")
            self.current_price_label.config(text=f"Current Price: ${self._format_price(info.get('currentPrice'))}")
            self.week_high_label.config(text=f"52-Week High: ${self._format_price(info.get('fiftyTwoWeekHigh'))}")
            self.week_low_label.config(text=f"52-Week Low: ${self._format_price(info.get('fiftyTwoWeekLow'))}")
            
            # Update Financial Performance tab
            self.roe_label.config(text=f"Return on Equity (ROE): {self._format_percent(info.get('returnOnEquity'))}")
            self.roa_label.config(text=f"Return on Assets (ROA): {self._format_percent(info.get('returnOnAssets'))}")
            self.profit_margin_label.config(text=f"Profit Margin: {self._format_percent(info.get('profitMargins'))}")
            self.revenue_label.config(text=f"Revenue (TTM): {self._format_number(info.get('totalRevenue'))}")
            self.gross_profit_label.config(text=f"Gross Profit: {self._format_number(info.get('grossProfits'))}")
            self.net_income_label.config(text=f"Net Income: {self._format_number(info.get('netIncomeToCommon'))}")
            self.total_debt_label.config(text=f"Total Debt: {self._format_number(info.get('totalDebt'))}")
            self.current_ratio_label.config(text=f"Current Ratio: {self._format_ratio(info.get('currentRatio'))}")
            self.debt_equity_label.config(text=f"Debt to Equity: {self._format_ratio(info.get('debtToEquity'))}")
            
            # Update Analysis tab
            self.recommendation_label.config(text=f"Recommendation: {info.get('recommendationKey', 'N/A').upper()}")
            self.target_mean_label.config(text=f"Target Mean Price: ${self._format_price(info.get('targetMeanPrice'))}")
            self.target_high_label.config(text=f"Target High Price: ${self._format_price(info.get('targetHighPrice'))}")
            self.target_low_label.config(text=f"Target Low Price: ${self._format_price(info.get('targetLowPrice'))}")
            self.dividend_yield_label.config(text=f"Dividend Yield: {self._format_percent(info.get('dividendYield'))}")
            self.dividend_rate_label.config(text=f"Dividend Rate: ${self._format_price(info.get('dividendRate'))}")
            self.payout_ratio_label.config(text=f"Payout Ratio: {self._format_percent(info.get('payoutRatio'))}")
            
        except Exception as e:
            self._show_error(f"Error updating display: {str(e)}")
        finally:
            # Re-enable button
            self.analyze_btn.config(state="normal", text="Analyze Stock")
            
    def _format_number(self, value):
        if value is None:
            return "N/A"
        try:
            if value >= 1_000_000_000:
                return f"${value/1_000_000_000:.2f}B"
            elif value >= 1_000_000:
                return f"${value/1_000_000:.2f}M"
            elif value >= 1_000:
                return f"${value/1_000:.2f}K"
            else:
                return f"${value:,.2f}"
        except:
            return "N/A"
            
    def _format_price(self, value):
        if value is None:
            return "N/A"
        try:
            return f"{value:.2f}"
        except:
            return "N/A"
            
    def _format_ratio(self, value):
        if value is None:
            return "N/A"
        try:
            return f"{value:.2f}"
        except:
            return "N/A"
            
    def _format_percent(self, value):
        if value is None:
            return "N/A"
        try:
            return f"{value*100:.2f}%"
        except:
            return "N/A"
            
    def _show_error(self, error_msg):
        messagebox.showerror("Error", f"Failed to analyze stock: {error_msg}")
        self.analyze_btn.config(state="normal", text="Analyze Stock")
        
    def export_symbols(self):
        try:
            filename = self.stock_handler.get_all_stock()
            messagebox.showinfo("Success", f"TSX symbols exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export symbols: {str(e)}")

def main():
    root = tk.Tk()
    app = StockAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()