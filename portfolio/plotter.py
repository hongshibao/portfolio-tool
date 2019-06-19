from loguru import logger
import matplotlib.pyplot as plt
from os import makedirs
from os.path import dirname, abspath


# disable logging in modules
logger.disable("portfolio.plotter")


class Plotter:
    def __init__(self, figure_size=(18, 6), dpi=100, marker='o'):
        self._figure_size = figure_size
        self._dpi = dpi
        self._marker = marker


    def plot_time_series_data(self, data, fig_filepath):
        # create folders if not exist
        folder_path = dirname(fig_filepath)
        if folder_path:
            makedirs(folder_path, exist_ok=True)
        abs_fig_filepath = abspath(fig_filepath)
        logger.debug("Saving figure to {}", abs_fig_filepath)
        data.plot(grid=True, marker=self._marker, figsize=self._figure_size)
        plt.savefig(fig_filepath, dpi=self._dpi, bbox_inches='tight')
        logger.debug("Saving figure to {} succeed", abs_fig_filepath)
