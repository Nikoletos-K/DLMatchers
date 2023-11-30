import argparse
import csv
import io
import contextlib
import pandas as pd

from pyjedai.datamodel import Data
from pyjedai.block_building import (
    StandardBlocking,
    QGramsBlocking,
    ExtendedQGramsBlocking,
    SuffixArraysBlocking,
    ExtendedSuffixArraysBlocking,
)

constructors = {"standard":StandardBlocking,
                "qgrams":QGramsBlocking,
                "extended-qgrams":ExtendedQGramsBlocking,
                "suffix-arrays":SuffixArraysBlocking,
                "extended-suffix":ExtendedSuffixArraysBlocking 
            }

def main():
    parser = argparse.ArgumentParser(description="Algorithm script's arguments")
    parser.add_argument("--blocking", type=str, required=True, help="Blocking Type")
    arguments = parser.parse_args()

    # with open('/app/target.csv', 'r') as csv_file:
    #     with open('/app/output.txt', 'w') as txt_file:
    #         csv_reader = csv.reader(csv_file)
    #         for row in csv_reader:
    #             txt_file.write(','.join(row) + '\n')

    # # print(pipi)
    # # # Write arguments to the output file
    # output_file_path = '/app/source.csv'
    # with open(output_file_path, 'w') as output_file:
    #     output_file.write(str(environment_arguments.score))

    # # # Print a message
    # # print(f"Arguments written to {output_file_path}")
    d1 = pd.read_csv("app/source.csv", sep='|', engine='python', na_filter=False)
    d2 = pd.read_csv("app/target.csv", sep='|', engine='python', na_filter=False)
    gt = pd.read_csv("app/gt.csv", sep='|', engine='python')

    data = Data(dataset_1=d1,
                id_column_name_1='id',
                dataset_2=d2,
                id_column_name_2='id',
                ground_truth=gt)
    
    bb = constructors[arguments.blocking]()
    blocks = bb.build_blocks(data)
    
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        _ = bb.evaluate(blocks, with_classification_report=True)
    blocking_output = buffer.getvalue()
    
    with open('app/output.txt', 'w') as file:
        file.write(blocking_output)

if __name__ == "__main__":
    main()