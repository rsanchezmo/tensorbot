import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import Dict, Any, List
from tbparse import SummaryReader
import numpy as np


def plot_tensorboard_experiment(exp_path: str, plot_config: List[Dict[str, Any]]) -> (List[str], Dict[str, Any]):
    """ Plot a Tensorboard experiment

    :param exp_path: path to the Tensorboard experiment (it assumes that the route is confirmed to exist)
    :type exp_path: str

    :param plot_config: configuration for the plots
    :type plot_config: List[Dict[str, Any]]

    :return tmp_paths: list of paths to the temporary images
    :rtype tmp_paths: List[str]

    :return train_history: dictionary with the training history
    :rtype train_history: Dict[str, Any]
    """

    reader = SummaryReader(exp_path, pivot=True, extra_columns={'dir_name', 'wall_time'})
    tb_candidates = [child for child in reader.children.keys() if 'events.out.tfevents' in child]
    tb_candidates.sort()

    # get the last event file, if there are many
    data = reader.children[tb_candidates[-1]].scalars

    tmp_paths = []
    for figure_idx, figure in enumerate(plot_config):
        fig = plt.figure(figsize=figure.get('fig_size', (12, 6)))

        subplots: List | None = figure.get('subplots', None)
        if subplots is None:
            continue

        num_subplots = len(subplots)
        num_cols = figure.get('max_cols', 2)
        num_rows = num_subplots // num_cols + 1 if num_subplots % num_cols else num_subplots // num_cols
        odd = num_subplots % num_cols

        num_tags = sum([len(subplot['tags']) for subplot in subplots])
        colors = plt.cm.get_cmap('tab10', num_tags)

        gs = gridspec.GridSpec(num_rows, num_cols)

        total_tag_idx = 0
        for subplot_idx, subplot in enumerate(subplots):
            if subplot_idx == num_subplots - 1 and odd:
                ax = fig.add_subplot(gs[subplot_idx // num_cols, subplot_idx % num_cols:])
            else:
                ax = fig.add_subplot(gs[subplot_idx // num_cols, subplot_idx % num_cols])

            style = subplot.get('style', ['-'] * len(subplot['tags']))
            marker = subplot.get('marker', [''] * len(subplot['tags']))
            for tag_idx, tag in enumerate(subplot['tags']):
                if tag not in data.columns:
                    print(f"Tag {tag} not found in the experiment")
                    continue

                if isinstance(data[tag][0], list):
                    y = np.array(data[tag].values.tolist())
                    y = y[:, 0]
                else:
                    y = data[tag].values

                nan_mask = ~np.isnan(y)
                y = y[nan_mask]

                x = data['step']
                x = x.values[nan_mask]
                ax.plot(x, y, label=tag, color=colors(total_tag_idx), linestyle=style[tag_idx], marker=marker[tag_idx])
                total_tag_idx += 1

            ax.set_title(subplot.get('title', ''))
            ax.set_yscale(subplot.get('scale', 'linear'))
            ax.legend().set_visible(subplot.get('legend', False))
            ax.grid(axis='both', color='0.92')

        fig.suptitle(figure.get('figure_name', ''), fontweight='bold')
        fig.tight_layout()
        tmp_path = f'tmp_{figure_idx}.png'
        plt.savefig(tmp_path, dpi=300)
        plt.close(fig)
        tmp_paths.append(tmp_path)

    times = data["wall_time"].values
    begin = times[0][0]
    end = times[-1][0]
    elapsed_time = end - begin

    train_history = {
        'training_time': elapsed_time,
        'training_steps': data['step'].values[-1],
    }

    return tmp_paths, train_history
