import torch
from torch.utils.data import Dataset
import json
import csv
import os
from PIL import Image
from utils import transform, label_map


class PascalVOCDataset(Dataset):
    """
    A PyTorch Dataset class to be used in a PyTorch DataLoader to create batches.
    """

    def __init__(self, data_folder, split, keep_difficult=False):
        """
        :param data_folder: folder where data files are stored
        :param split: split, one of 'TRAIN' or 'TEST'
        :param keep_difficult: keep or discard objects that are considered difficult to detect?
        """
        self.split = split.upper()

        assert self.split in {'TRAIN', 'TEST'}

        self.data_folder = data_folder
        self.keep_difficult = keep_difficult

        # Read data files
        with open(os.path.join(data_folder, self.split + '_images.json'), 'r') as j:
            self.images = json.load(j)
        with open(os.path.join(data_folder, self.split + '_objects.json'), 'r') as j:
            self.objects = json.load(j)

        assert len(self.images) == len(self.objects)

    def __getitem__(self, i):
        # Read image
        image = Image.open(self.images[i], mode='r')
        image = image.convert('RGB')

        # Read objects in this image (bounding boxes, labels, difficulties)
        objects = self.objects[i]
        boxes = torch.FloatTensor(objects['boxes'])  # (n_objects, 4)
        labels = torch.LongTensor(objects['labels'])  # (n_objects)
        difficulties = torch.ByteTensor(objects['difficulties'])  # (n_objects)

        # Discard difficult objects, if desired
        if not self.keep_difficult:
            boxes = boxes[1 - difficulties]
            labels = labels[1 - difficulties]
            difficulties = difficulties[1 - difficulties]

        # Apply transformations
        image, boxes, labels, difficulties = transform(
            image, boxes, labels, difficulties, split=self.split)

        return image, boxes, labels, difficulties

    def __len__(self):
        return len(self.images)

    def collate_fn(self, batch):
        """
        Since each image may have a different number of objects, we need a collate function (to be passed to the DataLoader).

        This describes how to combine these tensors of different sizes. We use lists.

        Note: this need not be defined in this Class, can be standalone.

        :param batch: an iterable of N sets from __getitem__()
        :return: a tensor of images, lists of varying-size tensors of bounding boxes, labels, and difficulties
        """

        images = list()
        boxes = list()
        labels = list()
        difficulties = list()

        for b in batch:
            images.append(b[0])
            boxes.append(b[1])
            labels.append(b[2])
            difficulties.append(b[3])

        images = torch.stack(images, dim=0)

        # tensor (N, 3, 300, 300), 3 lists of N tensors each
        return images, boxes, labels, difficulties


class CustomDatasetCSV(Dataset):
    split: str
    data_folder: str
    keep_difficult: bool
    dataset: list

    def __init__(self, data_folder: str, split: str, keep_difficult=False):
        """
        :param data_folder: folder where data files are stored
        :param split: split, one of 'TRAIN' or 'TEST'
        :param keep_difficult: keep or discard objects that are considered difficult to detect?
        """
        self.split = split.upper()

        assert self.split in {'TRAIN', 'TEST'}

        self.data_folder = data_folder
        self.keep_difficult = keep_difficult

        dataset = list()
        # Read data files
        with open(os.path.join(data_folder, self.split.lower() + ".csv"), 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            dataset = [dict(zip(header, row)) for row in reader]
        
        data_entries = dict()

        for data_row in dataset:
            file_name = data_row["filename"]
            x_min = float(data_row["xmin"])
            y_min = float(data_row["ymin"])
            x_max = float(data_row["xmax"])
            y_max = float(data_row["ymax"])
            class_name = data_row["class"]
            difficult = int(data_row.get("difficult", 0))

            if file_name not in data_entries:
                data_entries[file_name] = {
                    "filename": file_name,
                    "boxes": list(),
                    "labels": list(),
                    "difficulties": list()
                }
            
            data_entries[file_name]["boxes"].append([x_min, y_min, x_max, y_max])
            data_entries[file_name]["labels"].append(label_map[class_name])
            data_entries[file_name]["difficulties"].append(difficult)

        self.dataset = list(data_entries.values())
        


    def __getitem__(self, i):
        data_row = self.dataset[i]
        filename = data_row["filename"]

        # Read image
        image = Image.open(
            f"./images/{self.split.lower()}/{filename}", mode='r')
        image = image.convert('RGB')
       

        boxes = torch.FloatTensor(data_row["boxes"])  # (n_objects, 4)
        labels = torch.LongTensor(data_row["labels"])  # (n_objects)
        difficulties = torch.ByteTensor(data_row["difficulties"])  # (n_objects)

        # Apply transformations
        image, boxes, labels, difficulties = transform(
            image, boxes, labels, difficulties, split=self.split)

        return image, boxes, labels, difficulties

    def __len__(self):
        return len(self.dataset)

    def collate_fn(self, batch):
        """
        Since each image may have a different number of objects, we need a collate function (to be passed to the DataLoader).

        This describes how to combine these tensors of different sizes. We use lists.

        Note: this need not be defined in this Class, can be standalone.

        :param batch: an iterable of N sets from __getitem__()
        :return: a tensor of images, lists of varying-size tensors of bounding boxes, labels, and difficulties
        """
        images = list()
        boxes = list()
        labels = list()
        difficulties = list()

        for b in batch:
            images.append(b[0])
            boxes.append(b[1])
            labels.append(b[2])
            difficulties.append(b[3])

        images = torch.stack(images, dim=0)

        # tensor (N, 3, 300, 300), 3 lists of N tensors each
        return images, boxes, labels, difficulties


class CustomDataset2(Dataset):

    def __init__(self, data_folder: str, split: str, keep_difficult=False):
        """
        :param data_folder: folder where data files are stored
        :param split: split, one of 'TRAIN' or 'TEST'
        :param keep_difficult: keep or discard objects that are considered difficult to detect?
        """
        self.split = split.upper()

        assert self.split in {'TRAIN', 'TEST'}

        self.data_folder = data_folder
        self.keep_difficult = keep_difficult

        # Read data files
        with open(os.path.join(data_folder, self.split + '_images.json'), 'r') as j:
            self.images = json.load(j)
        with open(os.path.join(data_folder, self.split + '_objects.json'), 'r') as j:
            self.objects = json.load(j)

        assert len(self.images) == len(self.objects)

    def __getitem__(self, i):
        # Read image
        image = Image.open(self.images[i], mode='r')
        image = image.convert('RGB')

        objects = self.objects[i]
        boxes = torch.FloatTensor(objects['boxes'])  # (n_objects, 4)
        labels = torch.LongTensor(objects['labels'])  # (n_objects)
        difficulties = torch.ByteTensor(objects['difficulties'])  # (n_objects)

        # Apply transformations
        image, boxes, labels, difficulties = transform(
            image, boxes, labels, difficulties, split=self.split)

        return image, boxes, labels, difficulties

    def __len__(self):
        return len(self.images)

    def collate_fn(self, batch):
        """
        Since each image may have a different number of objects, we need a collate function (to be passed to the DataLoader).

        This describes how to combine these tensors of different sizes. We use lists.

        Note: this need not be defined in this Class, can be standalone.

        :param batch: an iterable of N sets from __getitem__()
        :return: a tensor of images, lists of varying-size tensors of bounding boxes, labels, and difficulties
        """
        images = list()
        boxes = list()
        labels = list()
        difficulties = list()

        for b in batch:
            images.append(b[0])
            boxes.append(b[1])
            labels.append(b[2])
            difficulties.append(b[3])

        images = torch.stack(images, dim=0)

        # tensor (N, 3, 300, 300), 3 lists of N tensors each
        return images, boxes, labels, difficulties
