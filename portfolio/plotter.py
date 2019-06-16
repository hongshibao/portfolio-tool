from loguru import logger
import matplotlib.pyplot as plt
import os


# disable logging in modules
logger.disable("plotter")


class Plotter:
    def __init__(self, figure_size=(18, 6), dpi=100, marker='o'):
        self._figure_size = figure_size
        self._dpi = dpi
        self._marker = marker


    def plot_time_series_data(self, data, fig_filepath):
        # create folders if not exist
        folder_path = os.path.dirname(fig_filepath)
        if folder_path:
            os.makedirs(folder_path, exist_ok=True)
        abs_fig_filepath = os.path.abspath(fig_filepath)
        logger.debug("Saving figure to {}", abs_fig_filepath)
        data.plot(grid=True, marker=self._marker, figsize=self._figure_size)
        plt.savefig(fig_filepath, dpi=self._dpi, bbox_inches='tight')
        logger.debug("Saving figure to {} succeed", abs_fig_filepath)
