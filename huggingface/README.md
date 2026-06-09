# Hugging Face Publishing Guide

This folder contains ready-to-copy cards and commands for publishing the project on Hugging Face.

Recommended public layout:

1. Model repo: `alperozyyurt/phishurl-detection`
2. Dataset repo: `alperozyyurt/phishurl-dataset`
3. Space repo: `alperozyyurt/phishurl-detection-demo`

Why separate repos:

- The model repo makes the trained weights discoverable under the correct ML task and license metadata.
- The dataset repo lets the Dataset Viewer, dataset metadata, and citation fields work properly.
- The Space gives visitors an interactive demo, which is the strongest way to make the project visible.

## License Decision

- Code in this repository: MIT license has been added at the project root.
- Model weights: you can publish them with MIT if you trained them yourself and the training data license allows redistribution of derived artifacts.
- Dataset: do not publish with `cc-by-4.0`, `mit`, or another open license until you verify the original data sources allow redistribution. If the dataset combines third-party URL lists, keep it `other` or private/gated until source licenses are documented.

## One-time Setup

```bash
pip install -U "huggingface_hub[cli]"
hf auth login
```

## Create Repositories

Replace `alperozyyurt` with your Hugging Face username if different.

```bash
hf repo create alperozyyurt/phishurl-detection --type model
hf repo create alperozyyurt/phishurl-dataset --type dataset
hf repo create alperozyyurt/phishurl-detection-demo --type space --space-sdk gradio
```

## Upload Model Repo

Create a temporary folder so only polished files are uploaded.

```bash
mkdir -p /tmp/phishurl-hf-model
cp huggingface/model-card/README.md /tmp/phishurl-hf-model/README.md
cp LICENSE /tmp/phishurl-hf-model/LICENSE
cp requirements-pip.txt /tmp/phishurl-hf-model/requirements.txt
cp -R models /tmp/phishurl-hf-model/models
cp -R gui/feature_extraction.py /tmp/phishurl-hf-model/feature_extraction.py
cp -R gui/tldlist.txt /tmp/phishurl-hf-model/tldlist.txt

hf upload alperozyyurt/phishurl-detection /tmp/phishurl-hf-model . --repo-type model
```

## Upload Dataset Repo

Use Parquet because it is faster and works well with the Dataset Viewer. Keep raw URL data out if you cannot redistribute it.

```bash
python huggingface/prepare_dataset.py \
  --input "4M Dataset Features.csv" \
  --output-dir hf_dataset \
  --label-column label

cp huggingface/dataset-card/README.md hf_dataset/README.md
hf upload alperozyyurt/phishurl-dataset hf_dataset . --repo-type dataset
```

## Upload Space

The current Flask GUI can be adapted, but a Gradio Space is usually simpler on Hugging Face. The Space app intentionally uses only the lightweight `.pkl` models to keep the public demo stable on CPU Basic.

```bash
mkdir -p /tmp/phishurl-hf-space
mkdir -p /tmp/phishurl-hf-space/models/{xgb,dt,lgbm}
cp huggingface/space-card/README.md /tmp/phishurl-hf-space/README.md
cp huggingface/space/app.py /tmp/phishurl-hf-space/app.py
cp huggingface/space/requirements.txt /tmp/phishurl-hf-space/requirements.txt
cp gui/feature_extraction.py /tmp/phishurl-hf-space/feature_extraction.py
cp gui/tldlist.txt /tmp/phishurl-hf-space/tldlist.txt
cp models/xgb/xgb-full-feature.pkl /tmp/phishurl-hf-space/models/xgb/
cp models/dt/dt-full-feature.pkl /tmp/phishurl-hf-space/models/dt/
cp models/lgbm/lgbm-full-feature.pkl /tmp/phishurl-hf-space/models/lgbm/

hf upload alperozyyurt/phishurl-detection-demo /tmp/phishurl-hf-space . --repo-type space
```
