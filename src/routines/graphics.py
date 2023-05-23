import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def add_zoom(fig, ax):
    axins = zoomed_inset_axes(ax, 3, loc=3)  # zoom = 6


    # sub region of the original image
    x1, x2, y1, y2 = 75., 100., 425., 500.
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    plt.xticks(visible=False)
    plt.yticks(visible=False)

    # draw a bbox of the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    plt.draw()
    plt.show()

