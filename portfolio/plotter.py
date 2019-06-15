import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, figure_size=(18, 6), dpi=100, marker='o'):
        self._figure_size = figure_size
        self._dpi = dpi
        self._marker = marker


    def plot_time_series_data(self, data, fig_filepath):
        plt.figure(dpi=self._dpi)
        data.plot(grid=True, marker=self._marker, figsize=self._figure_size)
        plt.savefig(fig_filepath, bbox_inches='tight')
