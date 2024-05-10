import argparse
import text
from utils import load_filepaths_and_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_extension", default="cleaned")
    parser.add_argument("--text_index", default=1, type=int)
    parser.add_argument(
        "--filelists",
        nargs="+",
        default=[
            "filelists/ljs_audio_text_val_filelist.txt",
            "filelists/ljs_audio_text_test_filelist.txt",
        ],
    )
    parser.add_argument("--text_cleaners", nargs="+", default=["cjke_cleaners2"])

    args = parser.parse_args()

    for filelist in args.filelists:
        print("START:", filelist)
        filepaths_and_text = load_filepaths_and_text(filelist)
        max_text = len(filepaths_and_text)
        for i in range(len(filepaths_and_text)):
            speaker_number = int(filepaths_and_text[i][1])
            original_text = filepaths_and_text[i][args.text_index]
            lang = ""
            if speaker_number == 87:
                lang = "[EN]"
            elif speaker_number < 87:
                lang = "[JA]"
            original_text = lang + original_text + lang
            cleaned_text = text._clean_text(original_text, args.text_cleaners)
            cleaned_text = cleaned_text.replace(lang, "")
            filepaths_and_text[i][args.text_index] = cleaned_text

            print("progress", i / max_text * 100)

        new_filelist = filelist + "." + args.out_extension
        with open(new_filelist, "w", encoding="utf-8") as f:
            f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])
