'''

'''
#
# import numpy as np
# import argparse
# import os
# import json
#
# def main(args):
#     output_dir = args.output_dir
#     if output_dir == '':
#         output_dir = os.path.dirname(args.input_file)
#     if not os.path.isdir(output_dir): os.makedirs(output_dir)
#
#     for ifile in args.input_file:
#         np.load(ifile)
#
#
#
#
#
#
# ##
# if __name__ == '__main__':
#
#     parser = argparse.ArgumentParser(description='Normalize runs individually')
#     parser.add_argument('--input_file', '-i', type=str, help='Input file', nargs="+")
#     parser.add_argument('--output_dir', '-o', type=str, help='Path to save the output', default='')
#     args = parser.parse_args()
#
#     main(args)