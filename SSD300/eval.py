from utils import *
from datasets import PascalVOCDataset, CustomDatasetCSV
from tqdm import tqdm
from pprint import PrettyPrinter
from torch.utils.data import DataLoader

# Good formatting when printing the APs for each class and mAP
pp = PrettyPrinter()

# Parameters
data_folder = './annotations'
# difficult ground truth objects must always be considered in mAP calculation, because these objects DO exist!
keep_difficult = True
batch_size = 64
workers = 4
device = get_device()
checkpoint = './checkpoint_ssd300_cuda_dataset_2.pth.tar'

# Load model checkpoint that is to be evaluated
checkpoint = torch.load(checkpoint, map_location=torch.device('cpu'))
model = checkpoint['model']
model = model.to(device)

# Switch to eval mode
model.eval()

# Load test data
# test_dataset = PascalVOCDataset(data_folder,
#                                 split='test',
#                                 keep_difficult=keep_difficult)
test_dataset = CustomDatasetCSV(data_folder, split='test')
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False,
                         collate_fn=test_dataset.collate_fn, num_workers=workers, pin_memory=True)


def evaluate(test_loader, model):
    """
    Evaluate.

    :param test_loader: DataLoader for test data
    :param model: model
    """

    # Make sure it's in eval mode
    model.eval()

    # Lists to store detected and true boxes, labels, scores
    det_boxes = list()
    det_labels = list()
    det_scores = list()
    true_boxes = list()
    true_labels = list()
    # it is necessary to know which objects are 'difficult', see 'calculate_mAP' in utils.py
    true_difficulties = list()

    with torch.no_grad():
        # Batches
        for (images, boxes, labels, difficulties) in tqdm(test_loader, desc='Evaluating'):
            images = images.to(device)  # (N, 3, 300, 300)

            # Forward prop.
            predicted_locs, predicted_scores = model(images)

            # Detect objects in SSD output
            det_boxes_batch, det_labels_batch, det_scores_batch = model.detect_objects(predicted_locs, predicted_scores,
                                                                                       min_score=0.01, max_overlap=0.45,
                                                                                       top_k=200)
            # Evaluation MUST be at min_score=0.01, max_overlap=0.45, top_k=200 for fair comparision with the paper's results and other repos

            # Store this batch's results for mAP calculation
            boxes = [b.to(device) for b in boxes]
            labels = [l.to(device) for l in labels]
            difficulties = [d.to(device) for d in difficulties]

            det_boxes.extend(det_boxes_batch)
            det_labels.extend(det_labels_batch)
            det_scores.extend(det_scores_batch)
            true_boxes.extend(boxes)
            true_labels.extend(labels)
            true_difficulties.extend(difficulties)

        # Calculate mAP
        APs, mAP = calculate_mAP(
            det_boxes, det_labels, det_scores, true_boxes, true_labels, true_difficulties)

    # Print AP for each class
    pp.pprint(APs)

    print('\nMean Average Precision (mAP): %.3f' % mAP)


if __name__ == '__main__':
    evaluate(test_loader, model)
