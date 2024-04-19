# TensorBot
`Tensorboard` connection to `telegram` to monitor your training process. You can monitor whatever training you want. Just need
to provide the path of the tensorboard log, some configuration for the plots of the desired metrics to monitor and a telegram
token and chat id to send messages to.

![TensorBot](./docs/tensorbot.png)


## Installation
```bash
pip install .
```

## Usage
First you should create your bot on telegram using the `BotFather` and get the token. Then you should open a chat with your bot
and write some message to it. Then you can get the chat id by calling the following url:
```python
import requests

url = f'https://api.telegram.org/bot{YOUR_TELEGRAM_TOKEN}/getUpdates'
response = requests.get(url)
print(response.json())
```
You should see the chat `id` in the response. If you receive nothing, remember to send a message to your bot first.

There is an `example.py` file that you can run to see how it works. Just instantiate the `TensorBot` class with your token and chat id, 
then create your plot config as depicted below and run the bot with the `run` method.

```python
from tensorbot import TensorBot

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
                'legend': True
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

bot.run(experiment_name='my_exp', update_interval=5, plot_config=plot_config,
        tensorboard_path='YOUR_TENSORBOARD_PATH')
```

To finish the process, just press `Ctrl+C` in the terminal where you are running the script. I thought about 
stopping when there is now new data for a while. May include this functionality in the future.

You should receive messages like this:
```
- TensorBot started to monitor experiment: my_exp 🚀 
- Checking for updates every 1 minutes

- Experiment: my_exp updated! 🚀
- Training time: 5.44 hours
- Training steps: 13
```

![jaxer_stats](./docs/jaxer_stats.jpeg)
![jaxer_timing](./docs/jaxer_timing.jpeg)
 

> [!NOTE]
> You can customize the plots as you want! If you think some feature is missing, please let me know!