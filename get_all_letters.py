import argparse
from text.symbols import symbols

def find_diff_chars(str1, str2):
  set1 = set(str1)
  set2 = set(str2)

#   diff_chars = set1.symmetric_difference(set2)
  diff_chars = set1.difference(set2)
  return diff_chars

def print_transcription_characters(input_file):
  """
  Reads the transcription from each line in a dataset and prints all characters.

  Args:
    input_file (str): Path to the input file.
  """

  all_characters = set()
  with open(input_file, 'r', encoding="utf-8") as f:
    for line in f:
      # Extract the transcription (assuming it's the last field)
      _, _, transcription = line.strip().split('|')
      # Print all characters in the transcription
      all_characters.update(transcription)

  unique_characters_list = list(all_characters)
  dataset_chars = "".join(unique_characters_list)
  print(dataset_chars)
  print(find_diff_chars(dataset_chars, "".join(symbols)))

if __name__ == "__main__":
  # Parse arguments from command line
  parser = argparse.ArgumentParser(description="Print characters from transcription")
  parser.add_argument("input_file", help="Path to the input file")
  args = parser.parse_args()

  # Call the function with parsed argument
  print_transcription_characters(args.input_file)
