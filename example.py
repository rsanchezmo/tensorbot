from tensorbot import TensorBot

if __name__ == '__main__':
    bot = TensorBot(token='YOUR_TOKEN_ID', chat_id='YOUR_CHAT_ID',
                    tensorboard_path='YOUR_TENSORBOARD_PATH')

    plot_config = [
        {
            'figure_name': 'train',
            'fig_size': (12, 6),
            'max_cols': 2,  
            'subplots': [
                {
                    'tags': ['train/loss', 'val/loss'],
                    'title': 'Loss',
                    'scale': 'log'
                },
                {
                    'tags': ['train/accuracy', 'val/accuracy'],
                    'title': 'Accuracy',
                    'scale': 'linear'
                }
            ]
        }
    ]

    bot.run(update_interval=5, plot_config=plot_config)
