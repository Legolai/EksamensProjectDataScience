from utils import label_map
import os
import xml.etree.ElementTree as ET
import json



def create_data_lists(path_to_data, output_folder):
    """
    Create lists of images, the bounding boxes and labels of the objects in these images, and save these to file.

    :param path_to_input: path to the data folder
    :param output_folder: folder where the JSONs must be saved
    """
    # path_to_data = os.path.abspath(path_to_data)

    train_images = list()
    train_objects = list()
    n_objects = 0

    # Training data
    with os.scandir(f'{path_to_data}/images') as entries:
        for entry in entries:
            file_name = entry.name.split(".")[0]
            objects = parse_annotation(
                f"{path_to_data}/Annotations/{file_name}.xml")

            if len(objects['boxes']) == 0:
                continue
            n_objects += len(objects)
            train_objects.append(objects)
            train_images.append(f"{path_to_data}/images/{entry.name}")
        # Find IDs of images in training data

    assert len(train_objects) == len(train_images)

    # Save to file
    with open(os.path.join(output_folder, 'TRAIN_images.json'), 'w') as j:
        json.dump(train_images, j)
    with open(os.path.join(output_folder, 'TRAIN_objects.json'), 'w') as j:
        json.dump(train_objects, j)
    with open(os.path.join(output_folder, 'label_map.json'), 'w') as j:
        json.dump(label_map, j)  # save label map too

    print('\nThere are %d training images containing a total of %d objects. Files have been saved to %s.' % (
        len(train_images), n_objects, os.path.abspath(output_folder)))


    # Test data
    test_images = list()
    test_objects = list()
    n_objects = 0

    # # Find IDs of images in the test data
    #region
    # with open(os.path.join(path_to_data, 'ImageSets/Main/test.txt')) as f:
    #     ids = f.read().splitlines()

    # for id in ids:
    #     # Parse annotation's XML file
    #     objects = parse_annotation(os.path.join(
    #         path_to_data, 'Annotations', id + '.xml'))
    #     if len(objects) == 0:
    #         continue
    #     test_objects.append(objects)
    #     n_objects += len(objects)
    #     test_images.append(os.path.join(
    #         path_to_data, 'JPEGImages', id + '.jpg'))

    # assert len(test_objects) == len(test_images)

    # # Save to file
    # with open(os.path.join(output_folder, 'TEST_images.json'), 'w') as j:
    #     json.dump(test_images, j)
    # with open(os.path.join(output_folder, 'TEST_objects.json'), 'w') as j:
    #     json.dump(test_objects, j)
    #endregion

    print('\nThere are %d test images containing a total of %d objects. Files have been saved to %s.' % (
        len(test_images), n_objects, os.path.abspath(output_folder)))
    

def parse_annotation(annotation_path):
    tree = ET.parse(annotation_path)
    root = tree.getroot()

    boxes = list()
    labels = list()
    difficulties = list()
    for object in root.iter('object'):

        difficult = int(object.find('difficult').text == '1')

        label = object.find('name').text.lower().strip()
        print(label)
        if label not in label_map:
            continue

        print(label)

        bbox = object.find('bndbox')
        xmin = int(bbox.find('xmin').text) - 1
        ymin = int(bbox.find('ymin').text) - 1
        xmax = int(bbox.find('xmax').text) - 1
        ymax = int(bbox.find('ymax').text) - 1

        boxes.append([xmin, ymin, xmax, ymax])
        labels.append(label_map[label])
        difficulties.append(difficult)

    return {'boxes': boxes, 'labels': labels, 'difficulties': difficulties}


if __name__ == '__main__':
    create_data_lists(path_to_data='./dataset_2',output_folder='./')
