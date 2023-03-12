'''

python src/decode_words.py \
    -i /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-01_ieeg/hfb_hp_reading_ecog_car_70-170_avgfirst_100Hz_log_norm.npy \
    -sr 100 \
    -w /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-01_audio.csv \
    -t meneer mevrouw

python src/decode_words.py \
    -i /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-02_ieeg/hfb_hp_reading_ecog_car_70-170_avgfirst_100Hz_log_norm.npy \
    -sr 100 \
    -w /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-02_audio.csv \
    -t perkamentus anderling

'''

import numpy as np
import argparse
import os
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from random import shuffle
from utils.general import resample

def main(args):
    output_dir = args.output_dir
    if output_dir == '':
        output_dir = os.path.dirname(args.input_file)
    if not os.path.isdir(output_dir): os.makedirs(output_dir)

    # load data
    input = np.load(args.input_file)
    all_words = pd.read_csv(args.word_file, index_col=0)
    targets = args.targets

    # select input features
    input = resample(input, 25, int(args.sampling_rate))
    args.sampling_rate = 25

    selected_electrodes = np.concatenate([np.arange(8)+16*i for i in range(0,6)])
    input = input[:, selected_electrodes]

    # get onsets of targets
    onsets = {t: None for t in targets}
    durations = {t: None for t in targets}
    for t in targets:
        onsets[t] = all_words[all_words['text'] == t]['xmin'].values
        durations[t] = all_words[all_words['text'] == t]['duration'].values

    # select balanced number of trials
    min_n = np.min([len(onsets[t]) for t in targets])
    selected_onsets = onsets.copy()
    [shuffle(selected_onsets[t]) for t in targets]
    for t in targets:
        selected_onsets[t] = selected_onsets[t][:min_n]

    # construct input data
    sec2ind = lambda s: int(round(s*args.sampling_rate))
    selected_inputs = {t: [] for t in targets}
    max_duration = np.max([np.max(durations[t]) for t in targets])
    for t in targets:
        for o in selected_onsets[t]:
            selected_inputs[t].append(input[sec2ind(o):sec2ind(o) + sec2ind(max_duration)])
        selected_inputs[t] = np.array((selected_inputs[t])).reshape(min_n, -1)

    # set up classifier
    x = np.concatenate(list(selected_inputs.values()))
    y = np.concatenate([np.zeros(min_n)+i for i,t in enumerate(targets)])
    order = np.random.permutation(len(y))
    x = x[order]
    y = y[order]

    # decode
    loo = LeaveOneOut()
    loo.get_n_splits(x)
    accuracy = []
    for i, (train_index, test_index) in enumerate(loo.split(x)):
        print("TRAIN:", train_index, "TEST:", test_index)
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        #print(x_train, x_test, y_train, y_test)
        #clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
        clf = make_pipeline(SVC(C=1.5))
        clf.fit(x_train, y_train)
        accuracy.append(clf.score(x_test, y_test))
        print(accuracy[-1])

    print(f'LOO-CV accuracy is {np.mean(accuracy)}')







##
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Decode words')
    parser.add_argument('--input_file', '-i', type=str, help='Input file')
    parser.add_argument('--sampling_rate', '-sr', type=float)
    parser.add_argument('--word_file', '-w', type=str, help='Word onsets file')
    parser.add_argument('--targets', '-t', type=str, help='Words to decode', nargs="+")
    parser.add_argument('--output_dir', '-o', type=str, help='Path to save the output', default='')
    args = parser.parse_args()

    main(args)