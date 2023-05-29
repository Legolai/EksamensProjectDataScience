# Exams Project - DataScience

@Legolai
@michaelxuw
@MuneebAshraf

## Pigeon Detector

The idea of this project was to create a model that could take a video feed and detect in each frame where there is pigeons.

### Technologies used

- Pytorch
- OpenCV
- XML
- JSON
- Pillow
- Selenium

### Installation guide

Install Pytorch with CUDA

```pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```

Install OpenCV

```pip3 install opencv-python```

Install Pillow

```pip3 install Pillow```

Install Selenium
```pip3 install selenium```

### User guide

Make sure you are in the SSD300 folder to use the model.

Train

```python3 train.py```

Eval

```python3 eval.py```

Modifier the detect file detect.py, change the checkpoint variable to the trained model you wish to use. Then run the program ```python3 app.py```

### Status

TBD

### List of Challenges

TBD

Project name
Short description
List of used 
Installation guide (if any libraries need to be installed)
User guide (how to run the program)
Status (What has been done (and if anything: what was not done))
List of Challenges you have set up for your self (The things in your project you want to highlight)
