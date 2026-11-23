"""Shared matplotlib style for paper figures: Times New Roman text and STIX (Times-like) math, embedded TrueType fonts,
recessive axes, and panel titles placed on one baseline."""
import matplotlib.pyplot as plt

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE = "#2a78d6", "#eb6834"


def use_paper_style(size=8):
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix", "font.size": size, "axes.titlesize": size, "axes.labelsize": size,
        "xtick.labelsize": size - 1, "ytick.labelsize": size - 1, "legend.fontsize": size - 1,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    })


def inches(fig, x, y, w, h):
    """Axes rectangle in inches from the lower-left corner of the figure."""
    W, H = fig.get_size_inches()
    return [x / W, y / H, w / W, h / H]


def panel_titles(fig, axes, labels, y_in):
    """Titles centred over each axes, all on the same baseline y_in (inches from the bottom)."""
    W, H = fig.get_size_inches()
    for ax, lab in zip(axes, labels):
        p = ax.get_position()
        fig.text(p.x0 + p.width / 2, y_in / H, lab, ha="center", va="baseline", color=INK)
