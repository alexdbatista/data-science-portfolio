"""
Portfolio Visual Identity System
=================================
Consistent color schemes, fonts, and styling across all data science projects.

Author: Alex Domingues Batista, PhD
Theme: Professional Analytical Chemistry → Data Science
"""

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# ═══════════════════════════════════════════════════════════════════
# COLOR PALETTE: "Analytical Precision"
# ═══════════════════════════════════════════════════════════════════

# Primary Colors (for main data visualization)
PRIMARY = {
    'deep_blue': '#1f77b4',      # Trust, precision, analytical
    'vibrant_orange': '#ff7f0e',  # Energy, highlights
    'forest_green': '#2ca02c',    # Success, validation
    'crimson_red': '#d62728',     # Alerts, degradation
    'royal_purple': '#9467bd',    # Innovation, advanced methods
    'warm_brown': '#8c564b',      # Stability, baseline
}

# Gradient Palettes (for sequential data)
SEQUENTIAL = {
    'blues': ['#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594'],
    'greens': ['#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32'],
    'reds': ['#fee5d9', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#99000d'],
    'purples': ['#f2f0f7', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486'],
}

# Diverging Palette (for comparisons, before/after)
DIVERGING = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']

# Qualitative Palette (for categories - up to 8 classes)
CATEGORICAL = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

# Gas/Chemical Specific (for gas sensor project)
GAS_COLORS = {
    'Ethanol': '#ff6b6b',        # Red tint
    'Ethylene': '#4ecdc4',       # Cyan/turquoise
    'Ammonia': '#ffe66d',        # Yellow
    'Acetaldehyde': '#a8dadc',   # Light blue
    'Acetone': '#f1c40f',        # Golden
    'Toluene': '#9b59b6',        # Purple
}

# Status Colors (for quality indicators)
STATUS = {
    'excellent': '#27ae60',      # Green
    'good': '#2ecc71',           # Light green
    'warning': '#f39c12',        # Orange
    'critical': '#e74c3c',       # Red
    'neutral': '#95a5a6',        # Gray
}

# ═══════════════════════════════════════════════════════════════════
# TYPOGRAPHY & LAYOUT
# ═══════════════════════════════════════════════════════════════════

FONTS = {
    'title': {'family': 'sans-serif', 'size': 16, 'weight': 'bold'},
    'subtitle': {'family': 'sans-serif', 'size': 14, 'weight': 'semibold'},
    'label': {'family': 'sans-serif', 'size': 12},
    'legend': {'family': 'sans-serif', 'size': 11},
    'annotation': {'family': 'sans-serif', 'size': 10},
}

# Figure sizes (width, height in inches)
FIGSIZE = {
    'small': (10, 6),
    'medium': (14, 7),
    'large': (16, 8),
    'wide': (18, 6),
    'square': (10, 10),
    'tall': (10, 14),
}

# ═══════════════════════════════════════════════════════════════════
# MATPLOTLIB/SEABORN CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

def apply_portfolio_style():
    """
    Apply the portfolio visual identity to all matplotlib/seaborn plots.
    Call this at the beginning of each notebook.
    """
    
    # Seaborn style base
    sns.set_style("whitegrid", {
        'axes.edgecolor': '#333333',
        'axes.linewidth': 1.5,
        'grid.color': '#e0e0e0',
        'grid.linestyle': '--',
        'grid.linewidth': 0.8,
    })
    
    # Matplotlib rcParams
    rcParams.update({
        # Figure
        'figure.figsize': (14, 7),
        'figure.dpi': 100,
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',
        
        # Axes
        'axes.labelsize': 12,
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'normal',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.prop_cycle': plt.cycler('color', CATEGORICAL),
        'axes.facecolor': 'white',
        
        # Ticks
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 6,
        'ytick.major.size': 6,
        'xtick.major.width': 1.2,
        'ytick.major.width': 1.2,
        
        # Legend
        'legend.fontsize': 11,
        'legend.frameon': True,
        'legend.framealpha': 0.95,
        'legend.edgecolor': '#cccccc',
        'legend.fancybox': True,
        'legend.shadow': False,
        
        # Lines
        'lines.linewidth': 2.5,
        'lines.markersize': 8,
        
        # Grid
        'grid.alpha': 0.6,
        
        # Font
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Helvetica'],
    })
    
    # Set default color palette
    sns.set_palette(CATEGORICAL)


def get_project_colors(project='general'):
    """
    Get project-specific color schemes.
    
    Parameters:
    -----------
    project : str
        One of: 'nasa', 'gas_sensor', 'metabolomics', 'general'
    
    Returns:
    --------
    dict : Color scheme for the specified project
    """
    schemes = {
        'nasa': {
            'primary': PRIMARY['deep_blue'],
            'secondary': PRIMARY['vibrant_orange'],
            'success': PRIMARY['forest_green'],
            'danger': PRIMARY['crimson_red'],
            'palette': [PRIMARY['deep_blue'], PRIMARY['vibrant_orange'], 
                       PRIMARY['forest_green'], PRIMARY['warm_brown']],
        },
        'gas_sensor': {
            'primary': PRIMARY['forest_green'],
            'secondary': PRIMARY['crimson_red'],
            'drift': PRIMARY['vibrant_orange'],
            'baseline': PRIMARY['deep_blue'],
            'palette': list(GAS_COLORS.values()),
        },
        'metabolomics': {
            'primary': PRIMARY['royal_purple'],
            'secondary': PRIMARY['vibrant_orange'],
            'healthy': PRIMARY['deep_blue'],
            'disease': PRIMARY['crimson_red'],
            'palette': [PRIMARY['royal_purple'], PRIMARY['vibrant_orange'], 
                       PRIMARY['deep_blue'], PRIMARY['crimson_red']],
        },
        'general': {
            'palette': CATEGORICAL,
        }
    }
    
    return schemes.get(project, schemes['general'])


# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def add_watermark(ax, text="A. Domingues Batista, PhD", position='bottom_right', alpha=0.3):
    """Add professional watermark to plots."""
    if position == 'bottom_right':
        ax.text(0.98, 0.02, text, transform=ax.transAxes,
                fontsize=9, color='gray', alpha=alpha,
                ha='right', va='bottom', style='italic')
    elif position == 'top_right':
        ax.text(0.98, 0.98, text, transform=ax.transAxes,
                fontsize=9, color='gray', alpha=alpha,
                ha='right', va='top', style='italic')


def create_gradient_colormap(colors, name='custom'):
    """Create custom gradient colormap from list of colors."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(name, colors)


def style_comparison_plot(ax, title, ylabel, highlight_color=PRIMARY['forest_green']):
    """Apply consistent styling to comparison plots."""
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel(ylabel, fontsize=12, fontweight='semibold')
    ax.set_xlabel('', fontsize=12, fontweight='semibold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.tick_params(labelsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    return ax


# ═══════════════════════════════════════════════════════════════════
# USAGE EXAMPLE
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Apply in notebooks with:
    # from visual_config import apply_portfolio_style, get_project_colors
    # apply_portfolio_style()
    # colors = get_project_colors('nasa')
    print("✅ Portfolio visual identity system loaded!")
    print(f"   Primary colors: {len(PRIMARY)}")
    print(f"   Sequential palettes: {len(SEQUENTIAL)}")
    print(f"   Gas-specific colors: {len(GAS_COLORS)}")
