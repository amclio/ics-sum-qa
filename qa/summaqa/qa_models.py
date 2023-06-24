import torch
from transformers import BertTokenizer, BertForQuestionAnswering


class QA_Bert:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = BertTokenizer.from_pretrained(
            "snunlp/KR-Medium", do_lower_case=False
        )
        self.model = BertForQuestionAnswering.from_pretrained(
            # "timpal0l/mdeberta-v3-base-squad2",
            "Kdogs/klue-finetuned-squad_kor_v1",
            # "ainize/klue-bert-base-mrc"
            # "bespin-global/klue-bert-base-aihub-mrc",
            # "bert-large-uncased-whole-word-masking-finetuned-squad",
        ).to(self.device)

        self.SEP_id = self.tokenizer.encode("[SEP]")[0]

    def predict(self, question, text):
        input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
        input_ids = self.tokenizer.encode(input_text)
        token_type_ids = [
            0 if i <= input_ids.index(self.SEP_id) else 1 for i in range(len(input_ids))
        ]

        start_scores, end_scores = self.model(
            torch.tensor([input_ids]).to(self.device), return_dict=False
        )

        start_scores = torch.nn.functional.softmax(start_scores, -1) * torch.Tensor(
            token_type_ids
        ).to(self.device)
        end_scores = torch.nn.functional.softmax(end_scores, -1) * torch.Tensor(
            token_type_ids
        ).to(self.device)

        start_values, start_indices = start_scores.topk(1)
        end_values, end_indices = end_scores.topk(1)

        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)

        answer = " ".join(all_tokens[start_indices[0][0] : end_indices[0][0] + 1])
        prob = start_values[0][0] * end_values[0][0]

        return answer, prob.item()
