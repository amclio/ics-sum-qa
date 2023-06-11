from collections import Counter
import string
import re
from kolm.normalize import normalize


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    # def remove_articles(text):
    #     return re.sub(r'\b(a|an|the)\b', ' ', text)

    # def white_space_fix(text):
    #     return ' '.join(text.split())

    # def remove_punc(text):
    #     exclude = set(string.punctuation)
    #     return ''.join(ch for ch in text if ch not in exclude)

    # def lower(text):
    #     return text.lower()

    # return white_space_fix(remove_articles(remove_punc(lower(s))))

    lines = normalize([s])

    if len(lines) == 0:
        return ""

    return lines[0]


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()

    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1
