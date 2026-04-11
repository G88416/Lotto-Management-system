import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
import pyperclip  # pip install pyperclip (optional, for easy copy)

MAX_GENERATION_ATTEMPTS = 15000

class LottoGapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LottoGap • Custom Gap Filter + Historical Canvas")
        self.root.geometry("1100x780")
        self.root.configure(bg="#0f172a")
        
        self.historical_max_gap = None
        self.all_generated_tickets = []
        
        # ====================== LEFT PANEL ======================
        left_frame = tk.Frame(root, bg="#1e2937", width=420, height=700)
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        tk.Label(left_frame, text="🎛️ Custom Gap Filter", font=("Inter", 18, "bold"), bg="#1e2937", fg="white").pack(anchor="w", padx=20, pady=(20,10))
        
        # Settings
        settings = tk.LabelFrame(left_frame, text="LOTTO SETTINGS", font=("Inter", 10, "bold"), bg="#1e2937", fg="#64748b", labelanchor="nw", padx=15, pady=10)
        settings.pack(fill="x", padx=15, pady=10)
        
        tk.Label(settings, text="Pool (1 to N):", bg="#1e2937", fg="#cbd5e1", font=("Inter", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.pool_var = tk.IntVar(value=52)
        tk.Entry(settings, textvariable=self.pool_var, width=10, font=("Inter", 14), justify="center", bg="#334155", fg="white", relief="flat").grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(settings, text="Numbers to pick:", bg="#1e2937", fg="#cbd5e1", font=("Inter", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.pick_var = tk.IntVar(value=6)
        tk.Entry(settings, textvariable=self.pick_var, width=10, font=("Inter", 14), justify="center", bg="#334155", fg="white", relief="flat").grid(row=1, column=1, padx=10, pady=5)
        
        # Max Gap
        gap_frame = tk.LabelFrame(left_frame, text="MAXIMUM GAP (difference)", font=("Inter", 10, "bold"), bg="#1e2937", fg="#64748b", labelanchor="nw", padx=15, pady=10)
        gap_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(gap_frame, text="Tight clusters", bg="#1e2937", fg="#64748b", font=("Inter", 9)).pack(anchor="w")
        self.max_gap_var = tk.IntVar(value=4)
        self.slider = tk.Scale(gap_frame, from_=2, to=15, orient="horizontal", variable=self.max_gap_var,
                               bg="#1e2937", fg="#00d4ff", highlightthickness=0, length=340, font=("Inter", 10))
        self.slider.pack(pady=5)
        tk.Label(gap_frame, text="More spread", bg="#1e2937", fg="#64748b", font=("Inter", 9)).pack(anchor="e")
        
        tk.Label(gap_frame, text="Example: 1,3,4,6,8,9,11,14,15,17 (max gap = 3)", bg="#1e2937", fg="#00d4ff", font=("Inter", 9, "italic")).pack(pady=5)
        
        # Historical Canvas
        tk.Label(left_frame, text="📋 Paste Draw Results Canvas", font=("Inter", 14, "bold"), bg="#1e2937", fg="white").pack(anchor="w", padx=20, pady=(15,5))
        
        self.draws_text = scrolledtext.ScrolledText(left_frame, height=8, font=("Consolas", 11), bg="#111827", fg="#e2e8f0", insertbackground="#00d4ff")
        self.draws_text.pack(fill="x", padx=15, pady=5)
        self.draws_text.insert("1.0", "Paste your past lotto draws here (one draw per line):\n1, 3, 4, 6, 8, 9\n5, 7, 12, 15, 18, 20\n2, 4, 9, 11, 14, 17")
        
        btn_frame = tk.Frame(left_frame, bg="#1e2937")
        btn_frame.pack(fill="x", padx=15, pady=8)
        
        tk.Button(btn_frame, text="🔍 ANALYZE & LEARN GAP PATTERN", command=self.analyze_historical, bg="#00d4ff", fg="#0f172a", font=("Inter", 11, "bold"), relief="flat", height=2).pack(side="left", expand=True, fill="x", padx=(0,5))
        tk.Button(btn_frame, text="CLEAR", command=self.clear_historical, bg="#334155", fg="white", font=("Inter", 11), relief="flat", width=12).pack(side="left")
        
        self.historical_label = tk.Label(left_frame, text="", bg="#1e2937", fg="#00ffaa", font=("Inter", 10, "bold"))
        self.historical_label.pack(pady=5)
        
        # Generate button
        tk.Button(left_frame, text="GENERATE PATTERN TICKETS", command=self.generate_tickets, bg="#00d4ff", fg="#0f172a", font=("Inter", 16, "bold"), relief="flat", height=3).pack(fill="x", padx=15, pady=15)
        
        # ====================== RIGHT PANEL ======================
        right_frame = tk.Frame(root, bg="#0f172a")
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        header = tk.Frame(right_frame, bg="#0f172a")
        header.pack(fill="x")
        tk.Label(header, text="🎟️ Your Filtered Tickets", font=("Inter", 18, "bold"), bg="#0f172a", fg="white").pack(side="left")
        
        tk.Button(header, text="📋 Copy ALL as text", command=self.copy_all_tickets, bg="#334155", fg="white", font=("Inter", 10, "bold")).pack(side="right", padx=5)
        tk.Button(header, text="CLEAR RESULTS", command=self.clear_results, bg="#334155", fg="#f87171", font=("Inter", 10, "bold")).pack(side="right")
        
        self.results_area = tk.Frame(right_frame, bg="#0f172a")
        self.results_area.pack(fill="both", expand=True, pady=10)
        
        # Empty state
        self.empty_label = tk.Label(self.results_area, text="No tickets yet\n\nPaste past draws → Analyze → Generate tickets\nEvery ticket respects your custom gap rule", 
                                    font=("Inter", 14), bg="#1e2937", fg="#64748b", height=12, width=60, relief="solid", bd=1)
        self.empty_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Status bar
        self.status = tk.Label(root, text="Ready to generate", bg="#0f172a", fg="#00d4ff", font=("Inter", 10))
        self.status.pack(side="bottom", fill="x", pady=8)
    
    def parse_historical(self, text):
        draws = []
        for line in text.splitlines():
            nums = []
            for x in line.replace(",", " ").split():
                try:
                    nums.append(int(x))
                except ValueError:
                    pass
            if len(nums) >= 2:
                unique = sorted(set(nums))
                draws.append(unique)
        return draws
    
    def analyze_historical(self):
        text = self.draws_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "Please paste some past draws first!")
            return
        
        draws = self.parse_historical(text)
        if not draws:
            messagebox.showwarning("No draws", "Could not detect any valid draws.")
            return
        
        max_gaps = []
        for draw in draws:
            max_g = 1
            for i in range(len(draw)-1):
                diff = draw[i+1] - draw[i]
                if diff > max_g:
                    max_g = diff
            max_gaps.append(max_g)
        
        overall_max = max(max_gaps)
        self.historical_max_gap = overall_max
        
        self.historical_label.config(text=f"✅ {len(draws)} draws analyzed • Historical Max Gap = {overall_max}")
        self.slider.set(overall_max)
        self.status.config(text=f"Historical pattern applied (max gap = {overall_max})")
        
        if messagebox.askyesno("Apply & Generate?", "Apply this historical gap and generate new tickets now?"):
            self.generate_tickets()
    
    def clear_historical(self):
        self.draws_text.delete("1.0", tk.END)
        self.historical_label.config(text="")
        self.historical_max_gap = None
        self.status.config(text="Ready to generate")
    
    def generate_valid_combo(self, N, k, max_gap):
        if max_gap <= 0:
            return None
        attempts = 0
        while attempts < MAX_GENERATION_ATTEMPTS:
            nums = set()
            while len(nums) < k:
                nums.add(random.randint(1, N))
            sorted_nums = sorted(nums)
            valid = True
            for i in range(len(sorted_nums)-1):
                if sorted_nums[i+1] - sorted_nums[i] > max_gap:
                    valid = False
                    break
            if valid:
                return sorted_nums
            attempts += 1
        return None
    
    def remove_ticket(self, frame, numbers):
        frame.destroy()
        if numbers in self.all_generated_tickets:
            self.all_generated_tickets.remove(numbers)

    def create_ticket_widget(self, numbers, max_gap, is_historical=False):
        frame = tk.Frame(self.results_area, bg="#1e2937", relief="solid", bd=2, padx=15, pady=15)
        frame.pack(fill="x", pady=8, padx=10)
        
        # Header
        header = tk.Frame(frame, bg="#1e2937")
        header.pack(fill="x")
        tk.Label(header, text="HISTORICAL STYLE TICKET" if is_historical else "VALID PATTERN TICKET", 
                 bg="#1e2937", fg="#00ffaa" if is_historical else "#00d4ff", font=("Inter", 10, "bold")).pack(side="left")
        tk.Label(header, text=f"Gap ≤ {max_gap}", bg="#334155", fg="white", font=("Inter", 9), padx=8, pady=2).pack(side="left", padx=8)
        tk.Button(header, text="×", command=lambda f=frame, n=numbers: self.remove_ticket(f, n),
                  bg="#1e2937", fg="#f87171", font=("Inter", 14, "bold"), relief="flat", width=2).pack(side="right")
        
        # Balls
        ball_frame = tk.Frame(frame, bg="#1e2937")
        ball_frame.pack(pady=12)
        for n in numbers:
            ball = tk.Label(ball_frame, text=f"{n:02d}", font=("Inter", 22, "bold"), width=4, height=2,
                            bg="#f43f5e", fg="white", relief="raised", bd=4, highlightbackground="#fff")
            ball.pack(side="left", padx=6)
        
        # Gaps
        gap_frame = tk.Frame(frame, bg="#1e2937")
        gap_frame.pack(fill="x")
        tk.Label(gap_frame, text="GAPS BETWEEN NUMBERS", bg="#1e2937", fg="#64748b", font=("Inter", 9)).pack(anchor="w")
        inner = tk.Frame(gap_frame, bg="#1e2937")
        inner.pack(fill="x", pady=4)
        for i in range(len(numbers)-1):
            diff = numbers[i+1] - numbers[i]
            percent = min((diff / max_gap) * 100, 100) if max_gap > 0 else 0
            bar = tk.Frame(inner, bg="#334155", height=12, width=80)
            bar.pack(side="left", padx=3, fill="x", expand=True)
            fill = tk.Frame(bar, bg="#00d4ff", height=12, width=int(80 * percent / 100))
            fill.place(x=0, y=0)
            tk.Label(inner, text=str(diff), bg="#1e2937", fg="#cbd5e1", font=("Inter", 8)).pack(side="left", padx=2)
        
        # AI-readable text
        tk.Label(frame, text=f"Machine-readable for any AI → {', '.join(map(str, numbers))}", 
                 bg="#111827", fg="#e2e8f0", font=("Consolas", 11), anchor="w", padx=12, pady=8).pack(fill="x", pady=(12,0))
        
        self.all_generated_tickets.append(numbers)
        return frame
    
    def generate_tickets(self):
        for widget in self.results_area.winfo_children():
            if widget != self.empty_label:
                widget.destroy()
        
        self.all_generated_tickets.clear()
        self.empty_label.pack_forget()
        
        N = max(10, self.pool_var.get())
        k = max(2, min(self.pick_var.get(), N-1))
        max_gap = self.max_gap_var.get()
        
        generated = 0
        for _ in range(5):
            combo = self.generate_valid_combo(N, k, max_gap)
            if combo:
                self.create_ticket_widget(combo, max_gap, is_historical=(self.historical_max_gap is not None))
                generated += 1
        
        if generated == 0:
            tk.Label(self.results_area, text="Could not generate valid tickets.\nTry increasing Max Gap.", 
                     font=("Inter", 14), bg="#1e2937", fg="#f87171").pack(expand=True, fill="both", pady=50)
            return
        
        self.status.config(text=f"✅ {generated} pattern tickets generated (AI-readable)")
    
    def copy_all_tickets(self):
        if not self.all_generated_tickets:
            messagebox.showinfo("Nothing to copy", "No tickets yet!")
            return
        text = "\n\n".join([f"Ticket {i+1}: {', '.join(map(str, t))}" for i, t in enumerate(self.all_generated_tickets)])
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Copied!", "All tickets copied to clipboard as plain text!\nAny other AI can read them perfectly.")
        except Exception:
            # Fallback
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied!", "All tickets copied (fallback clipboard).")
    
    def clear_results(self):
        for widget in self.results_area.winfo_children():
            widget.destroy()
        self.empty_label.pack(expand=True, fill="both", padx=20, pady=20)
        self.all_generated_tickets.clear()
        self.status.config(text="Ready to generate")

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("⚠️  Optional: pip install pyperclip  (makes copy button faster)")
    root = tk.Tk()
    app = LottoGapApp(root)
    root.mainloop()
