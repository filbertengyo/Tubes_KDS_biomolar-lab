"""
BioMolar Lab — GUI Simulator Osmosis Sel Darah Merah
Jalankan: python -m src.gui
"""
import tkinter as tk
from tkinter import ttk, font as tkfont
import math
import sys

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyArrowPatch, Ellipse
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ── konstanta ────────────────────────────────────────────────────────────────
CELL_OSM   = 300.0   # mOsm/L osmolaritas normal sel darah merah
R          = 0.08206 # L·atm / (mol·K)
T          = 310.0   # Kelvin (37°C)

PRESETS = {
    "Normal saline (0.9%)":   dict(nacl=154, gluc=90,  urea=14),
    "Half saline (0.45%)":    dict(nacl=77,  gluc=90,  urea=14),
    "Hipertonik (3% NaCl)":   dict(nacl=513, gluc=90,  urea=14),
    "Dextrose 5% in water":   dict(nacl=0,   gluc=278, urea=14),
    "Air murni (distilasi)":  dict(nacl=0,   gluc=0,   urea=0),
    "Gagal ginjal (uremia)":  dict(nacl=140, gluc=95,  urea=68),
    "Hiperglikemia (DM)":     dict(nacl=138, gluc=480, urea=14),
}

PALETTE = {
    "bg":        "#F8F7F4",
    "panel":     "#FFFFFF",
    "border":    "#E0DED8",
    "accent":    "#378ADD",
    "text":      "#2C2C2A",
    "muted":     "#888780",
    "success":   "#1D9E75",
    "warning":   "#BA7517",
    "danger":    "#E24B4A",
    "info_bg":   "#E6F1FB",
    "info_text": "#185FA5",
    "ok_bg":     "#EAF3DE",
    "ok_text":   "#27500A",
    "warn_bg":   "#FAEEDA",
    "warn_text": "#633806",
    "err_bg":    "#FCEBEB",
    "err_text":  "#791F1F",
}

def calc_osm(nacl, gluc, urea):
    return 2 * nacl + gluc / 18.0 + urea / 2.8

def osmotic_pressure(delta_osm):
    """π = ΔC · R · T  (atm)"""
    return abs(delta_osm) * R * T / 1000.0

def cell_scale(osm_sol):
    diff = osm_sol - CELL_OSM
    if osm_sol < 100:  return 1.80
    if osm_sol > 500:  return 0.55
    return max(0.65, min(1.55, 1.0 - diff * 0.0015))

def classify(osm_sol):
    if osm_sol < 150:  return "lisis"
    if osm_sol < 275:  return "hipotonik"
    if osm_sol <= 325: return "isotonik"
    if osm_sol <= 500: return "hipertonik"
    return "krenasi"


# ── canvas sel ───────────────────────────────────────────────────────────────
def draw_cell_axes(ax, osm_sol):
    ax.clear()
    ax.set_aspect("equal")
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axis("off")

    status = classify(osm_sol)
    scale  = cell_scale(osm_sol)

    # ── latar ekstrasel ──
    extra_color = {
        "lisis":     "#EDF4FB",
        "hipotonik": "#EDF4FB",
        "isotonik":  "#EBF7F3",
        "hipertonik":"#FFF8F0",
        "krenasi":   "#FFF8F0",
    }[status]
    ax.set_facecolor(extra_color)

    rng = np.random.default_rng(42)

    # titik air ekstrasel
    n_extra = {"lisis":50,"hipotonik":38,"isotonik":20,"hipertonik":10,"krenasi":5}[status]
    ec = PALETTE["accent"] if status in ("lisis","hipotonik") else PALETTE["success"]
    pts = rng.uniform(-3.2, 3.2, (n_extra * 3, 2))
    for p in pts[:n_extra]:
        dx, dy = p[0], p[1]
        if math.sqrt(dx**2 + (dy/0.65)**2) > scale * 1.15:
            ax.plot(dx, dy, "o", ms=3, color=ec, alpha=0.55, zorder=1)

    # ── sel ──
    rx, ry = 1.5 * scale, 0.97 * scale

    if status == "lisis":
        # burst rays
        for ang in np.linspace(0, 2*math.pi, 14, endpoint=False):
            ln = rng.uniform(0.6, 1.2)
            x0 = math.cos(ang)*rx*0.4; y0 = math.sin(ang)*ry*0.4
            x1 = math.cos(ang)*(rx+ln); y1 = math.sin(ang)*(ry+ln*0.65)
            ax.plot([x0,x1],[y0,y1], color=PALETTE["danger"], lw=1.4, alpha=0.7, zorder=3)
        ax.add_patch(Ellipse((0,0), rx*0.9, ry*0.9,
                              facecolor=PALETTE["danger"]+"33",
                              edgecolor=PALETTE["danger"], lw=2, zorder=4))
        ax.text(0, 0, "LISIS", ha="center", va="center",
                fontsize=11, fontweight="bold", color=PALETTE["danger"], zorder=5)

    elif status == "krenasi":
        # spiky
        thetas = np.linspace(0, 2*math.pi, 200)
        spikes = 16
        r_vals = [rx*(1.0 if int(t/(2*math.pi/spikes))%2==0 else 0.82) for t in thetas]
        xs = [r*math.cos(t) for r,t in zip(r_vals, thetas)]
        ys = [(r/rx)*ry*math.cos(t)*0 + (r/rx)*ry*math.sin(t) for r,t in zip(r_vals, thetas)]
        ys = [rv*math.sin(t)*ry/rx for rv,t in zip(r_vals, thetas)]
        ax.fill(xs, ys, facecolor=PALETTE["accent"]+"44",
                edgecolor=PALETTE["warning"], lw=2, zorder=3)
        ax.text(0, -ry - 0.25, "krenasi", ha="center", va="top",
                fontsize=9, color=PALETTE["warning"], zorder=5)

    else:
        # normal / swollen biconcave
        cell_fc = PALETTE["accent"] + "44"
        ax.add_patch(Ellipse((0,0), rx*2, ry*2,
                              facecolor=cell_fc,
                              edgecolor="#D4537E", lw=2.5, zorder=3))
        # dimple jika isotonik / hipertonik
        if scale <= 1.05:
            ax.add_patch(Ellipse((0,0), rx*0.75, ry*0.9,
                                  facecolor=extra_color+"BB",
                                  edgecolor="none", zorder=4))

        # titik air intrasel
        n_in = int(22 * scale)
        for _ in range(n_in):
            angle = rng.uniform(0, 2*math.pi)
            r2    = rng.uniform(0, 0.55)
            px = math.cos(angle)*rx*r2
            py = math.sin(angle)*ry*r2
            ax.plot(px, py, "o", ms=2.5, color=PALETTE["accent"], alpha=0.6, zorder=5)

    # ── panah aliran air ──
    if status == "hipotonik":
        for dx in [-0.45, 0.45]:
            ax.annotate("", xy=(dx*rx, 0), xytext=(dx*(rx+1.1), 0),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["accent"],
                                        lw=1.8, mutation_scale=14))
        ax.text(0, -ry-0.32, "air masuk ↓ osmolaritas ekstrasel rendah",
                ha="center", fontsize=8.5, color=PALETTE["info_text"], zorder=6)

    elif status == "hipertonik":
        for dx in [-0.45, 0.45]:
            ax.annotate("", xy=(dx*(rx+1.1), 0), xytext=(dx*rx, 0),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE["warning"],
                                        lw=1.8, mutation_scale=14))
        ax.text(0, -ry-0.32, "air keluar ↑ osmolaritas ekstrasel tinggi",
                ha="center", fontsize=8.5, color=PALETTE["warn_text"], zorder=6)

    elif status == "isotonik":
        ax.text(0, -ry-0.32, "⇆  keseimbangan osmotik",
                ha="center", fontsize=8.5, color=PALETTE["ok_text"], zorder=6)


# ── kelas utama GUI ──────────────────────────────────────────────────────────
class BioMolarGUI:
    def __init__(self, root):
        self.root = root
        root.title("BioMolar Lab — Osmosis Cell Simulator")
        root.configure(bg=PALETTE["bg"])
        root.resizable(True, True)
        root.minsize(860, 600)

        self._build_ui()
        self._update()

    # ── layout ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        root = self.root

        # ── header ──
        hdr = tk.Frame(root, bg=PALETTE["panel"],
                       highlightbackground=PALETTE["border"],
                       highlightthickness=1)
        hdr.pack(fill="x", padx=0, pady=0)
        tk.Label(hdr, text="BioMolar Lab",
                 font=("Helvetica", 17, "bold"),
                 bg=PALETTE["panel"], fg=PALETTE["text"],
                 pady=10, padx=18).pack(side="left")
        tk.Label(hdr, text="Osmosis Cell Simulator",
                 font=("Helvetica", 11),
                 bg=PALETTE["panel"], fg=PALETTE["muted"],
                 pady=10).pack(side="left")

        # ── body ──
        body = tk.Frame(root, bg=PALETTE["bg"])
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(0, weight=0, minsize=280)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

    def _panel(self, parent, title=None, **kw):
        f = tk.Frame(parent, bg=PALETTE["panel"],
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1,
                     **kw)
        if title:
            tk.Label(f, text=title.upper(),
                     font=("Helvetica", 9),
                     bg=PALETTE["panel"], fg=PALETTE["muted"],
                     padx=14, pady=8).pack(anchor="w")
            ttk.Separator(f, orient="horizontal").pack(fill="x", padx=14)
        return f

    # ── panel kiri: kontrol ──────────────────────────────────────────────────
    def _build_left(self, parent):
        outer = tk.Frame(parent, bg=PALETTE["bg"])
        outer.grid(row=0, column=0, sticky="nsew", padx=(0,10))

        # preset
        pf = self._panel(outer, "Preset larutan")
        pf.pack(fill="x", pady=(0,8))
        tk.Label(pf, text="Pilih preset:", font=("Helvetica",10),
                 bg=PALETTE["panel"], fg=PALETTE["muted"],
                 padx=14).pack(anchor="w", pady=(6,2))
        self.preset_var = tk.StringVar(value="Normal saline (0.9%)")
        cb = ttk.Combobox(pf, textvariable=self.preset_var,
                          values=list(PRESETS.keys()),
                          state="readonly", width=30)
        cb.pack(padx=14, pady=(0,10), fill="x")
        cb.bind("<<ComboboxSelected>>", self._on_preset)

        # sliders
        sf = self._panel(outer, "Parameter larutan")
        sf.pack(fill="x", pady=(0,8))

        self.nacl_var = tk.IntVar(value=154)
        self.gluc_var = tk.IntVar(value=90)
        self.urea_var = tk.IntVar(value=14)

        self._slider(sf, "NaCl", "mEq/L",  self.nacl_var, 0, 600)
        self._slider(sf, "Glukosa", "mg/dL", self.gluc_var, 0, 600)
        self._slider(sf, "Urea/BUN","mg/dL", self.urea_var, 0, 100)

        # stat cards
        cf = self._panel(outer, "Hasil perhitungan")
        cf.pack(fill="x", pady=(0,8))

        grid = tk.Frame(cf, bg=PALETTE["panel"])
        grid.pack(fill="x", padx=14, pady=10)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        self.lbl_osm_sol  = self._stat_card(grid, "Osm larutan",  "—", "mOsm/L", 0, 0)
        self.lbl_osm_diff = self._stat_card(grid, "Δ Osmolaritas","—", "mOsm/L", 0, 1)
        self.lbl_pi       = self._stat_card(grid, "Tek. osmotik", "—", "atm",    1, 0)
        self.lbl_vol      = self._stat_card(grid, "Vol. sel rel.", "—", "%",      1, 1)

        # status
        stf = self._panel(outer, "Status")
        stf.pack(fill="x", pady=(0,8))
        self.status_lbl = tk.Label(stf, text="—",
                                   font=("Helvetica", 12, "bold"),
                                   bg=PALETTE["panel"], fg=PALETTE["text"],
                                   padx=14, pady=8, anchor="w", justify="left",
                                   wraplength=240)
        self.status_lbl.pack(fill="x")

    def _slider(self, parent, label, unit, var, lo, hi):
        f = tk.Frame(parent, bg=PALETTE["panel"])
        f.pack(fill="x", padx=14, pady=4)
        top = tk.Frame(f, bg=PALETTE["panel"])
        top.pack(fill="x")
        tk.Label(top, text=label, font=("Helvetica",10),
                 bg=PALETTE["panel"], fg=PALETTE["text"]).pack(side="left")
        val_lbl = tk.Label(top, text=f"{var.get()} {unit}",
                           font=("Helvetica",10,"bold"),
                           bg=PALETTE["panel"], fg=PALETTE["accent"])
        val_lbl.pack(side="right")

        def on_change(_=None):
            val_lbl.config(text=f"{var.get()} {unit}")
            self._update()

        s = ttk.Scale(f, from_=lo, to=hi, variable=var,
                      orient="horizontal", command=on_change)
        s.pack(fill="x", pady=(2,0))

    def _stat_card(self, parent, label, val, unit, row, col):
        f = tk.Frame(parent, bg=PALETTE["bg"],
                     padx=10, pady=8)
        f.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        tk.Label(f, text=label, font=("Helvetica",8),
                 bg=PALETTE["bg"], fg=PALETTE["muted"]).pack(anchor="w")
        lbl = tk.Label(f, text=val, font=("Helvetica",16,"bold"),
                       bg=PALETTE["bg"], fg=PALETTE["text"])
        lbl.pack(anchor="w")
        tk.Label(f, text=unit, font=("Helvetica",8),
                 bg=PALETTE["bg"], fg=PALETTE["muted"]).pack(anchor="w")
        return lbl

    # ── panel kanan: visualisasi ─────────────────────────────────────────────
    def _build_right(self, parent):
        outer = tk.Frame(parent, bg=PALETTE["bg"])
        outer.grid(row=0, column=1, sticky="nsew")
        outer.rowconfigure(0, weight=1)
        outer.rowconfigure(1, weight=0)
        outer.columnconfigure(0, weight=1)

        # cell canvas
        cf = self._panel(outer, "Visualisasi sel darah merah")
        cf.grid(row=0, column=0, sticky="nsew", pady=(0,8))

        if HAS_MPL:
            self.fig, self.ax = plt.subplots(figsize=(5.2, 3.4),
                                              facecolor=PALETTE["bg"])
            self.fig.subplots_adjust(left=0.02, right=0.98,
                                      top=0.96, bottom=0.06)
            self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=cf)
            self.canvas_mpl.get_tk_widget().pack(fill="both",
                                                  expand=True, padx=12, pady=8)
        else:
            tk.Label(cf, text="Install matplotlib untuk visualisasi sel",
                     bg=PALETTE["panel"], fg=PALETTE["muted"],
                     font=("Helvetica",11)).pack(expand=True)

        # info biologis
        inf = self._panel(outer, "Penjelasan biologis")
        inf.grid(row=1, column=0, sticky="ew")
        self.info_txt = tk.Label(inf, text="—",
                                  font=("Helvetica", 10),
                                  bg=PALETTE["panel"], fg=PALETTE["text"],
                                  padx=14, pady=10, anchor="w",
                                  justify="left", wraplength=540)
        self.info_txt.pack(fill="x")

    # ── logika update ─────────────────────────────────────────────────────────
    def _on_preset(self, _=None):
        p = PRESETS[self.preset_var.get()]
        self.nacl_var.set(p["nacl"])
        self.gluc_var.set(p["gluc"])
        self.urea_var.set(p["urea"])
        self._update()

    def _update(self):
        nacl = self.nacl_var.get()
        gluc = self.gluc_var.get()
        urea = self.urea_var.get()

        osm_sol = calc_osm(nacl, gluc, urea)
        diff    = osm_sol - CELL_OSM
        pi      = osmotic_pressure(diff)
        status  = classify(osm_sol)
        sc      = cell_scale(osm_sol)
        vol_rel = round(min(180, max(50, sc * sc * 100)))

        # stat cards
        self.lbl_osm_sol.config(text=f"{osm_sol:.0f}")
        sign = "+" if diff >= 0 else ""
        self.lbl_osm_diff.config(text=f"{sign}{diff:.0f}")
        self.lbl_pi.config(text=f"{pi:.3f}")
        self.lbl_vol.config(text=f"{vol_rel}")

        # status badge color
        sc_colors = {
            "lisis":     (PALETTE["err_bg"],  PALETTE["err_text"],  "LISIS — membran pecah"),
            "hipotonik": (PALETTE["info_bg"], PALETTE["info_text"], "HIPOTONIK — sel membengkak"),
            "isotonik":  (PALETTE["ok_bg"],   PALETTE["ok_text"],  "ISOTONIK — sel normal"),
            "hipertonik":(PALETTE["warn_bg"], PALETTE["warn_text"],"HIPERTONIK — sel menyusut"),
            "krenasi":   (PALETTE["err_bg"],  PALETTE["warn_text"],"KRENASI — sel berduri"),
        }
        bg, fg, txt = sc_colors[status]
        self.status_lbl.config(bg=bg, fg=fg, text=txt)

        # penjelasan
        infos = {
            "lisis":     "Larutan sangat hipotonik (< 150 mOsm/L). Air masuk terus-menerus melebihi kapasitas membran plasma. Tekanan turgor menyebabkan membran pecah dan hemoglobin terlepas ke larutan — peristiwa ini disebut hemolisis.",
            "hipotonik": f"Larutan hipotonik ({osm_sol:.0f} mOsm/L < 275). Konsentrasi zat terlarut di luar sel lebih rendah dari dalam sel (300 mOsm/L). Air berpindah masuk melalui aquaporin mengikuti gradien osmotik. Sel membengkak ≈ {vol_rel}% volume normal.",
            "isotonik":  f"Larutan isotonik ({osm_sol:.0f} mOsm/L). Tekanan osmotik seimbang antara intrasel dan ekstrasel. Tidak ada perpindahan air neto. Sel mempertahankan bentuk bikonkaf normalnya (100% volume).",
            "hipertonik":f"Larutan hipertonik ({osm_sol:.0f} mOsm/L > 325). Konsentrasi ekstrasel lebih tinggi dari intrasel. Air keluar dari sel mengikuti gradien osmotik. Sel menyusut ≈ {vol_rel}% volume normal. Kondisi ini terjadi pada dehidrasi atau infus NaCl hipertonik.",
            "krenasi":   f"Larutan sangat hipertonik (> 500 mOsm/L). Air keluar masif dari sel, menyebabkan membran mengkerut dan membentuk tonjolan-tonjolan kecil (spicules). Sel menyusut hingga ≈ {vol_rel}% volume normal — disebut echinocytosis atau krenasi.",
        }
        self.info_txt.config(text=infos[status])

        # redraw matplotlib
        if HAS_MPL:
            draw_cell_axes(self.ax, osm_sol)
            self.canvas_mpl.draw()


# ── entry point ───────────────────────────────────────────────────────────────
def main():
    if not HAS_MPL:
        print("WARNING: matplotlib tidak terinstall. Visualisasi sel tidak akan tampil.")
        print("Jalankan: pip install matplotlib numpy")

    root = tk.Tk()

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("TScale", background=PALETTE["bg"], troughcolor=PALETTE["border"],
                    sliderlength=18, sliderthickness=14)
    style.configure("TCombobox", fieldbackground=PALETTE["panel"],
                    background=PALETTE["panel"])
    style.configure("TSeparator", background=PALETTE["border"])

    app = BioMolarGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
