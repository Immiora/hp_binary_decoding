'''
manually adjusted empty words later

python src/get_word_timestamps.py \
    -i /Fridge/users/julia/project_hp_reading/data/4pascal/sub-002/sub-002_ses-iemu_acq-ECOG_run-02_audio.TextGrid \
    -t words

'''
import textgrids
import os
import pandas as pd
import argparse
import sys
sys.path.insert(0, '.')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


def main(args):
    output_dir = args.output_dir
    if output_dir == '':
        output_dir = os.path.dirname(args.input_file)
    if not os.path.isdir(output_dir): os.makedirs(output_dir)


    #
    words = {'text':[], 'xmin':[], 'xmax':[]}
    fname = args.input_file
    print(fname)
    grid = textgrids.TextGrid(fname)

    for index, itext in enumerate(grid[args.tier]):
        print('text annotation ' + str(index))
        print(itext.text)

        if itext.text == '':
            continue
        else:
            words['text'].append(itext.text.lower())
            words['xmin'].append(itext.xmin)
            words['xmax'].append(itext.xmax)


    # save
    df = pd.DataFrame(words)
    df['duration'] = df['xmax'] - df['xmin']
    df.to_csv(os.path.join(output_dir, os.path.basename(fname).replace('.TextGrid', '.csv')))


##
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TextGrid to csv with time stamps for each word')
    parser.add_argument('--input_file', '-i', type=str, help='Input textgrid file')
    parser.add_argument('--tier', '-t', type=str, help='Tier name with words')
    parser.add_argument('--output_dir', '-o', type=str, help='Path to save the output', default='')
    args = parser.parse_args()

    main(args)