import json
import re
from collections import Counter
from typing import List, Dict

from PythonScripts import settings

RESERVED_TOKENS = ["<pad>", "<start>", "<unk>"]

if settings.AUTOMATED:
    def tokenize_test_case(test_case: Dict) -> str:
        tokens = [
            f"type:{test_case.get('type', 'unknown').lower().strip().replace(' ', '_')}",
            f"desc:{test_case.get('description', '').lower().strip().replace(' ', '_')}"
        ]
        for step in test_case.get("steps", []):
            if isinstance(step, dict):
                tokens.append(f"action:{(step.get('action') or '').lower().strip().replace(' ', '_')}")
                tokens.append(f"by:{(step.get('by') or '').lower().strip().replace(' ', '_')}")
                tokens.append(f"value:{(step.get('value') or '').lower().strip().replace(' ', '_')}")
                tokens.append(f"use_data_key:{(step.get('use_data_key') or '').lower().strip().replace(' ', '_')}")
            else:
                tokens.append(f"step:{str(step).lower().strip().replace(' ', '_')}")
        tokens.append(f"result:{test_case.get('expected_result', '').lower().strip().replace(' ', '_')}")
        return ' '.join(tokens)

else:
    def tokenize_test_case(test_case: Dict) -> str:
        tokens = [
            f"type:{test_case.get('type', 'unknown').lower().strip().replace(' ', '_')}",
            f"desc:{test_case.get('description', '').lower().strip().replace(' ', '_')}"
        ]
        for step in test_case.get("steps", []):
            tokens.append(f"step:{step.lower().strip().replace(' ', '_')}")
        tokens.append(f"result:{test_case.get('expected_result', '').lower().strip().replace(' ', '_')}")
        return ' '.join(tokens)

def detokenize_test_case(token_str: str, id_prefix="GEN") -> Dict:
    fields = {
        "id": f"{id_prefix}_{abs(hash(token_str)) % 100000}",
        "type": "",
        "description": "",
        "steps": [],
        "expected_result": ""
    }
    for token in token_str.strip().split():
        if token.startswith("type:"):
            fields["type"] = token[5:].replace('_', ' ')
        elif token.startswith("desc:"):
            fields["description"] = token[5:].replace('_', ' ')
        elif token.startswith("step:"):
            fields["steps"].append(token[5:].replace('_', ' '))
        elif token.startswith("result:"):
            fields["expected_result"] = token[7:].replace('_', ' ')
    return fields

def build_vocab_from_json(json_paths, vocab_path="vocab.txt", max_vocab_size=5000):
    counter = Counter()
    for path in json_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            tokens = tokenize_test_case(item).split()
            counter.update(tokens)

    vocab = RESERVED_TOKENS + [tok for tok, _ in counter.most_common(max_vocab_size - len(RESERVED_TOKENS))]
    with open(vocab_path, "w", encoding="utf-8") as f:
        for tok in vocab:
            f.write(tok + "\n")
    print(f" Vocab saved to {vocab_path} with {len(vocab)} tokens.")

def build_vocab_from_sjson(path, vocab_path="vocab.txt", max_vocab_size=5000):
    counter = Counter()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        tokens = tokenize_test_case(item).split()
        counter.update(tokens)

    vocab = RESERVED_TOKENS + [tok for tok, _ in counter.most_common(max_vocab_size - len(RESERVED_TOKENS))]
    with open(vocab_path, "w", encoding="utf-8") as f:
        for tok in vocab:
            f.write(tok + "\n")
    print(f" Vocab saved to {vocab_path} with {len(vocab)} tokens.")

def load_vocab(vocab_path="vocab.txt"):
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = [line.strip() for line in f]
    token_to_idx = {tok: i for i, tok in enumerate(vocab)}
    idx_to_token = {i: tok for tok, i in token_to_idx.items()}
    return vocab, token_to_idx, idx_to_token

def encode_token_str(token_str, token_to_idx, seq_len):
    ids = [token_to_idx["<start>"]] + [token_to_idx.get(tok, token_to_idx["<unk>"]) for tok in token_str.split()]
    return ids[:seq_len] + [token_to_idx["<pad>"]] * (seq_len - len(ids))

def decode_token_ids(token_ids, idx_to_token):
    token_str = " ".join([idx_to_token.get(i, "<unk>") for i in token_ids])
    return token_str
