from tensorbot import TensorBot


if __name__ == '__main__':
    bot = TensorBot(token='YOUR_TOKEN_ID', chat_id='YOUR_CHAT_ID')

    plot_config = [
        {
            'figure_name': 'jaxer_stats',
            'fig_size': (12, 6),
            'max_cols': 2,
            'subplots': [
                {
                    'tags': ['train/loss'],
                    'title': 'Loss',
                    'scale': 'log',
                    'legend': True,
                },
                {
                    'tags': ['test/acc_dir', 'train/acc_dir'],
                    'title': 'acc_dir',
                    'scale': 'linear',
                    'legend': True,
                    'style': ['-', '--']
                },
                {
                    'tags': ['test/mape'],
                    'title': 'acc_ind',
                    'scale': 'linear',
                    'legend': True
                },
                {
                    'tags': ['test/mae'],
                    'title': 'mae',
                    'scale': 'linear',
                    'legend': True
                },
                {
                    'tags': ['train/lr'],
                    'title': 'lr',
                    'scale': 'log',
                    'legend': True
                }
            ]
        },
        {
            'figure_name': 'jaxer_timing',
            'fig_size': (12, 6),
            'max_cols': 2,
            'subplots': [
                {
                    'tags': ['train/epoch_time'],
                    'title': 'Epoch Time',
                    'scale': 'linear',
                    'legend': True,
                    'style': ['-']
                },
                {
                    'tags': ['test/epoch_time'],
                    'title': 'Step Time',
                    'scale': 'linear',
                    'legend': True
                }

            ]
        }
    ]

    bot.run(experiment_name='my_exp', update_interval=1, patience_time=30, plot_config=plot_config,
            tensorboard_path='YOUR_TENSORBOARD_PATH')
