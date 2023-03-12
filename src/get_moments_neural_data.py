'''
get moments mean and std from a rest period (or silence not using in training/testing decoders)
trying to normalize using these rest values

python src/get_moments_neural_data.py \
    -i /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-01_ieeg/hfb_hp_reading_ecog_car_70-170_avgfirst_100Hz_log.csv \
    -sr 100 \
    --xmin 16.5 \
    --xmax 20.5

python src/get_moments_neural_data.py \
    -i /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-02_ieeg/hfb_hp_reading_ecog_car_70-170_avgfirst_100Hz_log.csv \
    -sr 100 \
    --xmin 50.5 \
    --xmax 54.5
'''

import numpy as np
import argparse
import json
import os

def get_moments(fname, xmin, xmax, sr, normalize):

    extension = os.path.splitext(fname)[1]
    if extension == '.npy':
        x = np.load(fname)
    elif extension == '.csv':
        from utils.general import load_csv_data
        x, labs = load_csv_data(fname)
        np.save(fname.replace(extension, '.npy'), x)
        np.save(fname.replace(extension, '_channels.npy'), labs)
    else:
        raise NotImplementedError

    temp = x[int(round(xmin*sr)):int(round(xmax*sr))]

    #meanfile = fname.replace('.npy', '_sec' + str(xmin) + 'to' + str(xmax) + '_mean.npy')
    #stdfile = fname.replace('.npy', '_sec' + str(xmin) + 'to' + str(xmax) + '_std.npy')
    moments = {}
    moments['rest_start'] = xmin
    moments['rest_stop'] = xmax
    moments['sr'] = sr
    moments['meanfile'] = fname.replace(extension, '_rest_precomputed_mean.npy')
    moments['stdfile'] = fname.replace(extension, '_rest_precomputed_std.npy')

    temp_mean = np.mean(temp, 0)
    temp_std = np.std(temp, 0, ddof=1)
    np.save(moments['meanfile'], temp_mean)
    np.save(moments['stdfile'], temp_std)

    json.dump(moments,
              open(fname.replace(extension, '_moments.json'), 'w'),
              indent=4,
              sort_keys=True)

    if normalize:
        x_norm = np.divide(np.subtract(x, temp_mean), temp_std)
        np.save(fname.replace(extension, '_norm.npy'), x_norm)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moments neural data for selected range')
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--sampling_rate', '-sr', type=float)
    parser.add_argument('--xmin', type=float, help='Start of rest in seconds')
    parser.add_argument('--xmax', type=float, help='End of rest in seconds')
    parser.add_argument('--normalize', dest='normalize', action='store_true')
    parser.add_argument('--no-normalize', dest='normalize', action='store_false')

    parser.set_defaults(normalize=True)

    args = parser.parse_args()

    get_moments(args.input, args.xmin, args.xmax, args.sampling_rate, args.normalize)