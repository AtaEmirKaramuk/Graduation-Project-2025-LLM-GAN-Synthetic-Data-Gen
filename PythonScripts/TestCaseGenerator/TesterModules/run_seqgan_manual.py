from Utils.tokenizer import build_vocab_from_json, load_vocab
from SeqGAN.train_seqgan import SeqGANTrainer
from PythonScripts.settings import (
    SEQGAN_CONFIG
)

# Step 1: Build vocab from real + Zephyr (or just real) test cases
build_vocab_from_json(["test_cases.json"], vocab_path="vocab.txt")

# Step 2: Load vocab into memory
vocab, _, _ = load_vocab("vocab.txt")

# Step 3: Define training configuration
config = SEQGAN_CONFIG

# Step 4: Train and generate using SeqGAN
trainer = SeqGANTrainer(config=config, vocab=vocab, gpu=False)
trainer.run_pipeline("test_cases.json")
