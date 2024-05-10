import random
import argparse

def split_by_speaker(input_file, output_train_file, output_test_file):
  """
  Splits a dataset by speaker, maintaining a 90/10 train/test split for each speaker.

  Args:
    input_file (str): Path to the input file containing speaker data.
    output_train_file (str): Path to the output file for the training data.
    output_test_file (str): Path to the output file for the testing data.
  """

  # Initialize empty dictionaries to store data by speaker
  speaker_data = {}
  train_data = {}
  test_data = {}

  # Read data from the input file
  with open(input_file, 'r', encoding="utf-8") as f:
    for line in f:
      path, speaker, transcription = line.strip().split('|')
      if speaker not in speaker_data:
        speaker_data[speaker] = []
      speaker_data[speaker].append((path, transcription))

  # Split data for each speaker
  for speaker, data in speaker_data.items():
    random.shuffle(data)  # Shuffle data to ensure randomness
    split_point = int(0.9 * len(data))  # Calculate 90% split point

    train_data[speaker] = data[:split_point]
    test_data[speaker] = data[split_point:]

  # Write train and test data to separate files
  with open(output_train_file, 'w', encoding="utf-8") as train_f, open(output_test_file, 'w', encoding="utf-8") as test_f:
    for speaker, speaker_data in train_data.items():
      for path, transcription in speaker_data:
        train_f.write(f"{path}|{speaker}|{transcription}\n")

    for speaker, speaker_data in test_data.items():
      for path, transcription in speaker_data:
        test_f.write(f"{path}|{speaker}|{transcription}\n")

if __name__ == "__main__":
  # Parse arguments from command line
  parser = argparse.ArgumentParser(description="Split dataset by speaker")
  parser.add_argument("input_file", help="Path to the input file")
  parser.add_argument("output_train_file", help="Path to the output training file")
  parser.add_argument("output_test_file", help="Path to the output testing file")
  args = parser.parse_args()

  # Call the split function with parsed arguments
  split_by_speaker(args.input_file, args.output_train_file, args.output_test_file)
  print("Splitting complete! Train and test data files created.")
