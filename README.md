# LLM-GAN Synthetic Data Generation Framework

## 🎯 Project Overview
This project, developed at **Doğuş University**, proposes a hybrid framework that integrates **Large Language Models (LLMs)** with **Generative Adversarial Networks (GANs)** to enhance synthetic data generation. The primary goal is to overcome the limitations of traditional GANs—such as lack of diversity and scenario-based control—by using LLMs to guide the generation of high-quality, contextually accurate test cases and datasets.

## 🛠 Methodology & Work Packages
The research follows a modular, data-driven methodology structured into three core phases:

* **WP1: Test Case Generation** – Combines LLM-driven data generation with sequence-based GANs (e.g., **SeqGAN**) to produce structured and syntactically valid software test cases.
* **WP2: Test Data Creation** – Generates synthetic user data (usernames, emails, passwords) using **CTGAN**, guided by LLM-generated context prompts to simulate realistic user interactions.
* **WP3: Automation & Packaging** – Integrates the generated outputs into an automated testing pipeline using **Selenium** for reproducible and continuous execution across multiple environments.

## 🧪 Technical Stack & Tools
* **LLM:** Falcon LLM.
* **GAN Architectures:** SeqGAN (for sequential test steps) and CTGAN (for tabular data).
* **Automation:** Selenium.
* **Analysis:** Evaluation via descriptive statistics and automation metrics such as time-to-execute and failure logs.

## 👥 Project Team
* **Berat Karadavut**
* **Günay Kırmızı**
* **Mert Güven**
* **Ata Emir Karamuk**
* **Berkay Öztürk**

**Supervisor:** Assoc. Prof. Dr. Aysun Güran
**Project Date:** May 2025
