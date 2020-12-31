import argparse
from sklearn.metrics import f1_score

def evaluation(path_to_ground_truth_bio, path_to_pred_bio):
    '''
    Computing F1-score for each of the major-claim, claim, premises, and non-argumentative classes
    '''

    gt_bio   = [x.split('\t') for x in open(path_to_ground_truth_bio).read().split('\n')[0:-1]]
    pred_bio = [x.split('\t') for x in open(path_to_pred_bio).read().split('\n')[0:-1]]


    #filter out tokens that doesn't need labels
    gt_bio   = [x for x in gt_bio if len(x) > 0]
    pred_bio = [x for x in pred_bio if len(x) > 0]

    gt_bio   = [x for x in gt_bio if  x[0] not in ['__END_PARAGRAPH__',  '__END_ESSAY__']]
    pred_bio = [x for x in pred_bio if x[0] not in ['__END_PARAGRAPH__',  '__END_ESSAY__']]

    assert len(gt_bio) == len(pred_bio), 'Number of tokens in the prediction file is different than the ground truth.'

    #F1-score overall tokens..
    _, gt_y   = zip(*gt_bio)
    _, pred_y = zip(*pred_bio)

    macro_f1_score = f1_score(gt_y, pred_y, average='macro')
    weighted_f1_score = f1_score(gt_y, pred_y, average='weighted')


    print('Macro F1-Score: ', round(macro_f1_score, 3))
    print('Weighted F1-Score: ', round(weighted_f1_score, 3))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate your approach')
    parser.add_argument('--gt_bio_path')
    parser.add_argument('--pred_bio_path')

    args = parser.parse_args()

    evaluation(args.gt_bio_path, args.pred_bio_path)
