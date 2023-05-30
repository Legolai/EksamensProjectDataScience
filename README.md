# Exams Project - DataScience

Group members: 
@Legolai
@michaelxuw
@MuneebAshraf

## Pigeon Detector

The idea of this project was to create a model that could take a video feed and detect in each frame where there is pigeons and scare them away in some way. Here it was important for us the the model had mixed balance of both speed and accuracy, so that the pigeon could be detect and dealt with. To do this we settled on the SSD (single shot detection) method, because it seem faster than Faster RCNN but less accuracte, YOLO was also an option which seems to be faster than SSD but less accuracte. So SSD feelt like a good balance. The whole idea was in the end to setup a raspberry pi with camera and the model connect to water hose or microfon to scare pigeons away from the area of which the camera points to. 

### Technologies used

- Pytorch
- OpenCV
- XML
- JSON
- Pillow
- Selenium

### Installation guide

Install Pytorch with CUDA

```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Install OpenCV

```
pip3 install opencv-python
```

Install Pillow

```
pip3 install Pillow
```

Install Selenium

```
pip3 install selenium
```

Install tqdm

```
pip3 install tqdm
```

Make sure that the python installation you have includes ```tkinter```.

### User guide

#### Setup from scratch

1. Edit ```googleImageScrapper.py``` for what kind of images you want and the amount then run the script to fetch images from google images. (The scrapper is currently only for Firefox)

2. Use a program like [LabelImg](https://github.com/heartexlabs/labelImg) or [MakeSense](https://www.makesense.ai) label images for what object that is need to be detected.

*Make sure you are in the SSD300 folder now.*

3. The edit ```create_data_lists.py``` so that it points to the correct folders. Now run the script. (Do some changes so that so also get a test dataset used for validation of the model)

4. Add a new custom dataset class to the ```datasets.py``` file, if none of the existing ones matches your usecase. Find and replace the dataset class use in ```train.py``` and ```eval.py```

**Train**

5. Edit ```train.py``` so it points to the correct folder and if need change the name for the checkpoint file. Now run the script. 

6. When you find the training has stagnated and see no noticeable improvement you may stop the train or let it continue. If *nothing* really has happen for the last 30 epochs and the loss value continues to be high, stop the train and start over, try change the decay value and such, maybe even the optimizer to get better result.

**Eval**

7. Now that you have a trained model, modifier the ```eval.py``` script and run it to see how good the model is compared to you.

**App**

8. Modifier the detect file ```detect.py```, change the checkpoint variable to the trained model you wish to use. [*Get pre-trained model*](https://drive.google.com/file/d/1Z8nXowDxZUV9Fm4JA09eDTbivA0Oaerl/view?usp=share_link). Then run the program ```python3 app.py```

### Status

Getting data
 - Webscrabing using the google_Image_Scraper.py. [done]
 
Preparing data
 - Labelling the images with: https://github.com/heartexlabs/labelImg, using the create_data_lists.py to prepare images and annotations for transformation. [done]


Transformation
 - The Transform function in utils.py is used to transform the pictures to the correct resolution (also annotations) as well as fully prepare the dataset for modeling. [done]


Modeling and computation
 - Modelled and trained with model.py, train.py and optimizer.py. [done]


Presentation
 - The detect.py is then used to connect to the webcam and the app.py for the program to run. [done]

The last step of the raspberry pi pigeon turret was not completed.

### List of Challenges

- Creating a webscraber
- To experience/do annotations
- To prepare a dataset (clean up and w/e needed)
- Finding a model that works for us and our hardware.
- Getting enough compute power to train the model and restart when things *failed*.
- To make a program that can run the webcam and detect pigeons.


### Sources 
 
- [SSD pytorch tutorial](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection)
- [Optimizer implementation](https://github.com/JRC1995/DemonRangerOptimizer) 
- [What optimizer to choose](https://johnchenresearch.github.io/demon/)
- [Base Google image scraper](https://github.com/ohyicong/Google-Image-Scraper)
