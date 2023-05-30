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

Getting data
 - Webscrabing using the google_Image_Scraper.py
Preparing data
 - Labelling the images with: https://github.com/heartexlabs/labelImg, using the create_data_lists.py to prepare images and annotations for transformation
Transformation
 - The Transform function in utils.py is used to transform the pictures to the correct resolution (also annotations) as well as fully prepare the dataset for modeling
Modeling and computation
 - Modelled and trained with model.py, train.py and optimizer.py
Presentation
 - The detect.py is then used to connect to the webcam and the app.py for the program to run.

### List of Challenges

To create a webscraber
To experience/do annotations
To prepare a dataset (clean up and what ever needed)
To model and train on a dataset
To make a program that can run the webcam and detect pigeons.



Project name
Short description
List of used 
Installation guide (if any libraries need to be installed)
User guide (how to run the program)
Status (What has been done (and if anything: what was not done))
List of Challenges you have set up for your self (The things in your project you want to highlight)
