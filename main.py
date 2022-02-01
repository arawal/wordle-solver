from os.path import exists
import pandas as pd
from utils import preprocess, generate_word_scores_from_populace

WORD_SCORES = {}

def main():
    if exists("word_scores.csv"):
        word_scores = pd.read_csv("word_scores.csv", header=None, index_col=0, squeeze=True).to_dict()
        word_scores = {k:v for k, v in word_scores.items() if v != 0}
        return word_scores
    else:
        preprocess()
        return main()
      
def guess(tracker):
    global WORD_SCORES
    if tracker["counter"] != 0:
        words_list = []
        for k, _ in list(WORD_SCORES.items()):
            if len(list(set(k) & set(tracker["no"].values()))) == 0:
                words_list.append(k)
            else:
                del WORD_SCORES[k]
                
        special = {"pos": list(tracker["pos"].values()), "final": list(tracker["final"].values())}
        WORD_SCORES = generate_word_scores_from_populace(words_list, special)
    
    return list(WORD_SCORES.keys())[0]

def run(tracker = {"counter": 0, "final": {}, "pos": {}, "no": {}}):
    # suggest
    suggest = guess(tracker)
    print(suggest.upper())
        
    # input
    result = input(
        "Enter 'Y' for yellow, 'G' for green, 'N' for neither for each character. Eg. YGYNN. If word not in dict, say 'WRONG': ")
    
    result = result.lower()
    
    if result == "ggggg":
        return
    elif "counter" in tracker and tracker["counter"] == 6:
        return
    
    if result != "wrong":
        tracker["counter"] += 1
        
    for i in range(5):
        if result[i] == "g":
            tracker["final"][i] = suggest[i]
        elif result[i] == "y":
            tracker["pos"][i] = suggest[i]
        else:
            tracker["no"][i] = suggest[i]
            
    run(tracker)
    
    return

      
if __name__ == "__main__":
    # read preprocessed data
    WORD_SCORES = main()
    run()
