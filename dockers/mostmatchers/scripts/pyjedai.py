import argparse
import csv

def main():
    # parser = argparse.ArgumentParser(description="Algorithm script's arguments")
    # parser.add_argument("--score", required=True, help="Algorithm Name")
    # environment_arguments, _ = parser.parse_known_args()

    with open('/app/target.csv', 'r') as csv_file:
        with open('/app/output.txt', 'w') as txt_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                txt_file.write(','.join(row) + '\n')

    # # print(pipi)
    # # # Write arguments to the output file
    # output_file_path = '/app/source.csv'
    # with open(output_file_path, 'w') as output_file:
    #     output_file.write(str(environment_arguments.score))

    # # # Print a message
    # # print(f"Arguments written to {output_file_path}")
    print("Script inside Docker has finished.")

    print("Hello")
if __name__ == "__main__":
    main()