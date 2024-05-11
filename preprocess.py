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
            lang = "[TH]"
            if speaker_number == 87:
                lang = "[EN]"
            elif speaker_number < 87:
                lang = "[JA]"
            original_text = lang + original_text + lang
            cleaned_text = text._clean_text(original_text, args.text_cleaners)
            cleaned_text = cleaned_text.replace(lang, "").replace("[", "").replace("]", "").replace("’", "").replace("-", "")
            filepaths_and_text[i][args.text_index] = cleaned_text

            print("progress", i / max_text * 100)

        new_filelist = filelist + "." + args.out_extension
        with open(new_filelist, "w", encoding="utf-8") as f:
            for x in filepaths_and_text:
                skip = False
                blacklist = ['慰', '往', '聲', '頭', '捨', '募', '離', '地', '送', '噴', '溺', '溌', '文', '曳', '撚', '神', '侈', '々', '巒']
                for bl in blacklist:
                    if bl in x[2]:
                        skip = True
                        break
                
                if skip:
                    continue

                speaker_number = int(filepaths_and_text[i][1])
                lang = 2
                if speaker_number == 87:
                    lang = 1
                elif speaker_number < 87:
                    lang = 0
                result_text = "|".join(x)
                f.write(f"{x[0]}|{x[1]}|{lang}|{x[2]}" + "\n")