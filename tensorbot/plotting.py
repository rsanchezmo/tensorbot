import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import Dict, Any, List
from tbparse import SummaryReader


def plot_tensorboard_experiment(exp_path: str, plot_config: List[Dict[str, Any]], tmp_path: str):
    """ Plot a Tensorboard experiment

    :param exp_path: path to the Tensorboard experiment (it assumes that the route is confirmed to exist)
    :type exp_path: str

    :param plot_config: configuration for the plots
    :type plot_config: List[Dict[str, Any]]

    :param tmp_path: path to save the temporary plot
    :type tmp_path: str

    """

    reader = SummaryReader(exp_path, pivot=True, extra_columns={'dir_name', 'wall_time'})
    data = reader.scalars

    for figure in plot_config:
        fig = plt.figure(figsize=figure.get('fig_size', (12, 6)))

        subplots: List | None = figure.get('subplots', None)
        if subplots is None:
            continue

        num_subplots = len(subplots)
        num_cols = figure.get('max_cols', 2)
        num_rows = num_subplots // num_cols + 1 if num_subplots % num_cols else num_subplots // num_cols

        gs = gridspec.GridSpec(num_rows, num_cols)



