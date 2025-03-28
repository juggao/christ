import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import pytz

class ChristelijkeFeestdagenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nederlandse Christelijke Feestdagen")
        self.root.geometry("650x550")
        self.root.configure(bg='#f0f0f0')
        
        # Header
        header = tk.Label(root, text="Belangrijke Christelijke Feestdagen in Nederland", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0')
        header.pack(pady=10)
        
        # Year selection
        year_frame = tk.Frame(root, bg='#f0f0f0')
        year_frame.pack(pady=5)
        tk.Label(year_frame, text="Selecteer jaar:", bg='#f0f0f0').pack(side=tk.LEFT)
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.year_spin = ttk.Spinbox(year_frame, from_=1900, to=2100, 
                                   textvariable=self.year_var, width=8)
        self.year_spin.pack(side=tk.LEFT, padx=5)
        ttk.Button(year_frame, text="Toon feestdagen", 
                  command=self.toon_feestdagen).pack(side=tk.LEFT, padx=5)
        
        # Results treeview
        self.tree = ttk.Treeview(root, columns=('Datum', 'Feestdag'), 
                               show='headings', height=18)
        self.tree.heading('Datum', text='Datum')
        self.tree.heading('Feestdag', text='Feestdag')
        self.tree.column('Datum', width=180, anchor='center')
        self.tree.column('Feestdag', width=430, anchor='w')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, 
                             anchor=tk.W, bg='#f0f0f0')
        self.status.pack(fill=tk.X, pady=(5,0))
        
        # Show current year's holidays by default
        self.toon_feestdagen()
    
    def bereken_pasen(self, jaar):
        """Bereken Paaszondag met Gauss-algoritme"""
        a = jaar % 19
        b = jaar // 100
        c = jaar % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        maand = (h + l - 7 * m + 114) // 31
        dag = ((h + l - 7 * m + 114) % 31) + 1
        return datetime(jaar, maand, dag)
    
    def get_feestdagen(self, jaar):
        """Bereken alle belangrijke christelijke feestdagen voor een bepaald jaar"""
        feestdagen = []
        
        # Vaste feestdagen
        vaste_feestdagen = [
            (datetime(jaar, 1, 6), "Driekoningen"),
            (datetime(jaar, 12, 5), "Sinterklaasavond"),
            (datetime(jaar, 12, 24), "Kerstavond"),
            (datetime(jaar, 12, 25), "Eerste Kerstdag"),
            (datetime(jaar, 12, 26), "Tweede Kerstdag"),
            (datetime(jaar, 12, 31), "Oudejaarsavond")
        ]
        
        # Bereken Pasen en aanverwante feestdagen
        pasen = self.bereken_pasen(jaar)
        
        beweeglijke_feestdagen = [
            (pasen - timedelta(days=46), "Aswoensdag"),
            (pasen - timedelta(days=7), "Palmzondag"),
            (pasen - timedelta(days=3), "Witte Donderdag"),
            (pasen - timedelta(days=2), "Goede Vrijdag"),
            (pasen, "Pasen (Eerste Paasdag)"),
            (pasen + timedelta(days=1), "Tweede Paasdag"),
            (pasen + timedelta(days=39), "Hemelvaartsdag"),
            (pasen + timedelta(days=49), "Pinksteren (Eerste Pinksterdag)"),
            (pasen + timedelta(days=50), "Tweede Pinksterdag"),
            (pasen + timedelta(days=56), "Drievuldigheidszondag"),
            (pasen + timedelta(days=60), "Sacramentsdag (RK)"),
        ]
        
        # Combineer en sorteer alle feestdagen
        alle_feestdagen = vaste_feestdagen + beweeglijke_feestdagen
        alle_feestdagen.sort(key=lambda x: x[0])
        
        # Formatteer datums en voeg toe aan lijst
        for datum, naam in alle_feestdagen:
            feestdagen.append((datum.strftime('%A %d %B %Y'), naam))
        
        return feestdagen
    
    def toon_feestdagen(self):
        """Toon feestdagen voor het geselecteerde jaar"""
        jaar = self.year_var.get()
        try:
            feestdagen = self.get_feestdagen(jaar)
            
            # Verwijder vorige resultaten
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Voeg nieuwe resultaten toe
            for datum, naam in feestdagen:
                self.tree.insert('', tk.END, values=(datum, naam))
                
            self.status.config(text=f"Toont christelijke feestdagen voor {jaar}")
        except Exception as e:
            self.status.config(text=f"Fout: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChristelijkeFeestdagenApp(root)
    root.mainloop()
