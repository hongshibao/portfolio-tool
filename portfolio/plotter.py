import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, figure_size=(18, 6), dpi=100, marker='o'):
        self._figure_size = figure_size
        self._dpi = dpi
        self._marker = marker


    def plot_time_series_data(self, data, fig_filepath):
        plt.figure(figsize=self._figure_size, dpi=self._dpi)
        data.plot(marker=self._marker)
        plt.grid()
        plt.savefig(fig_filepath, bbox_inches='tight')
