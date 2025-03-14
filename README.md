# Auto captioner for Instagram reels

<video controls src="whispertimestamp.mp4" title="Example Video"></video>

The step by step tutorial & code walkthrough can be found in the [subtitler-tutorial.ipynb](subtitler-tutorial.ipynb) file


## Quick Set up

Go into the backend subfolder

`cd instagram-reels-subtitles/backend`

Make a virtual python environment

```python3 -m venv venv```

Use the venv

`source venv/bin/activate`

Install the necessary packages

`pip3 install groq moviepy pysrt`

## How to run it
Run this command in your terminal

`python3 captioner.py`