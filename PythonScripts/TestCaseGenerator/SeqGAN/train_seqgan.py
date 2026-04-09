import torch
import torch.optim as optim
import json

from Utils.tokenizer import tokenize_test_case, detokenize_test_case, encode_token_str
from SeqGAN.seqgan_orig.helpers import prepare_generator_batch
from SeqGAN.rollout import Rollout

class SeqGANTrainer:
    def __init__(self, config, vocab, gpu=False):
        self.config = config
        self.vocab = vocab
        self.token_to_idx = {tok: i for i, tok in enumerate(vocab)}
        self.idx_to_token = {i: tok for i, tok in enumerate(vocab)}
        self.gpu = gpu

        from SeqGAN.seqgan_orig.generator import Generator
        from SeqGAN.seqgan_orig.discriminator import Discriminator

        self.generator = Generator(
            config["gen_emb_dim"],
            config["gen_hidden_dim"],
            len(vocab),
            config["seq_len"],
            gpu=gpu
        )

        self.discriminator = Discriminator(
            config["dis_emb_dim"],
            config["dis_hidden_dim"],
            len(vocab),
            config["seq_len"],
            gpu=gpu
        )

        self.gen_optimizer = optim.Adam(self.generator.parameters(), lr=config["gen_lr"])
        self.dis_optimizer = optim.Adagrad(self.discriminator.parameters(), lr=config["dis_lr"])

        if gpu:
            self.generator = self.generator.cuda()
            self.discriminator = self.discriminator.cuda()

    def load_dataset(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        sequences = []
        for obj in data:
            token_str = tokenize_test_case(obj)
            token_ids = encode_token_str(token_str, self.token_to_idx, self.config["seq_len"])
            sequences.append(torch.tensor(token_ids, dtype=torch.long))

        return torch.stack(sequences)

    def train_generator_mle(self, dataset):
        print("\n Pretraining Generator with MLE...")
        for epoch in range(self.config["pretrain_epochs"]):
            total_loss = 0
            for i in range(0, len(dataset), self.config["batch_size"]):
                batch = dataset[i:i + self.config["batch_size"]]
                inp, target = prepare_generator_batch(batch, start_letter=self.token_to_idx["<start>"], gpu=self.gpu)

                self.gen_optimizer.zero_grad()
                loss = self.generator.batchNLLLoss(inp, target)
                loss.backward()
                self.gen_optimizer.step()
                total_loss += loss.item()

            print(f"  Epoch {epoch+1}: Avg NLL Loss = {total_loss / len(dataset):.4f}")

    def train_generator_adv_with_rollout(self, dataset, num_batches=1, rollout_num=16):
        print("\n Adversarial Training with Rollout")
        rollout = Rollout(self.generator)

        for epoch in range(self.config["adv_epochs"]):
            print(f"  Adversarial Epoch {epoch + 1}/{self.config['adv_epochs']}")
            for _ in range(num_batches):
                samples = self.generator.sample(self.config["batch_size"], start_letter=self.token_to_idx["<start>"])
                inp, target = prepare_generator_batch(samples, start_letter=self.token_to_idx["<start>"], gpu=self.gpu)

                rewards = rollout.get_reward(
                    inp,
                    rollout_num=rollout_num,
                    discriminator=self.discriminator,
                    start_letter=self.token_to_idx["<start>"],
                    max_seq_len=self.config["seq_len"]
                )

                pg_loss = self.generator.batchPGLoss(inp, target, rewards)
                self.gen_optimizer.zero_grad()
                pg_loss.mean().backward()
                self.gen_optimizer.step()

            rollout.update_params()

    def train_discriminator(self, dataset):
        print("\n Pretraining Discriminator...")
        for epoch in range(self.config["disc_epochs"]):
            neg_samples = self.generator.sample(len(dataset), start_letter=self.token_to_idx["<start>"])

            pos = dataset  # already a tensor
            neg = neg_samples  # already a tensor

            data = torch.cat([pos, neg], dim=0)
            target = torch.cat([
                torch.ones(len(pos), 1),
                torch.zeros(len(neg), 1)
            ], dim=0)

            if self.gpu:
                data = data.cuda()
                target = target.cuda()

            perm = torch.randperm(data.size(0))
            data = data[perm]
            target = target[perm]

            self.dis_optimizer.zero_grad()
            out = self.discriminator.batchClassify(data)
            loss_fn = torch.nn.BCELoss()
            loss = loss_fn(out, target.view(-1))
            loss.backward()
            self.dis_optimizer.step()

            acc = torch.sum((out > 0.5) == (target > 0.5)).item() / len(target)
            print(f"  Epoch {epoch + 1}: Loss = {loss.item():.4f}, Accuracy = {acc:.4f}")

    """def train_discriminator(self, dataset):
        print("\n Pretraining Discriminator...")
        for epoch in range(self.config["disc_epochs"]):
            neg_samples = self.generator.sample(len(dataset), start_letter=self.token_to_idx["<start>"])
            pos = torch.stack(dataset)
            neg = neg_samples
            data = torch.cat([pos, neg], dim=0)
            target = torch.cat([
                torch.ones(len(pos), 1),
                torch.zeros(len(neg), 1)
            ], dim=0)

            if self.gpu:
                data = data.cuda()
                target = target.cuda()

            perm = torch.randperm(data.size(0))
            data = data[perm]
            target = target[perm]

            self.dis_optimizer.zero_grad()
            out = self.discriminator.batchClassify(data)
            loss_fn = torch.nn.BCELoss()
            loss = loss_fn(out, target)
            loss.backward()
            self.dis_optimizer.step()

            acc = torch.sum((out > 0.5) == (target > 0.5)).item() / len(target)
            print(f"  Epoch {epoch+1}: Loss = {loss.item():.4f}, Accuracy = {acc:.4f}")"""

    def generate_text(self, num_samples, output_file=None):
        samples = self.generator.sample(num_samples, start_letter=self.token_to_idx["<start>"])
        decoded = [
            detokenize_test_case(" ".join([self.idx_to_token[i.item()] for i in seq]))
            for seq in samples
        ]
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(decoded, f, indent=2)
        return decoded

    def run_pipeline(self, json_path):
        dataset = self.load_dataset(json_path)
        self.train_generator_mle(dataset)
        self.train_discriminator(dataset)
        self.train_generator_adv_with_rollout(dataset)
        self.generate_text(self.config["num_samples"], output_file=self.config["output_path"])
