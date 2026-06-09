---
license: other
language:
- en
- tr
task_categories:
- tabular-classification
task_ids:
- binary-classification
pretty_name: PhishURL Dataset
tags:
- cybersecurity
- phishing
- url-classification
- malicious-url-detection
- tabular
size_categories:
- 1M<n<10M
---

# PhishURL Dataset

This dataset is intended for binary phishing URL detection using extracted URL features.

Label convention:

- `0`: legitimate / safe
- `1`: phishing / malicious

## Data Fields

The feature dataset is expected to contain:

- `text`: original URL, if redistribution is allowed
- feature columns extracted from the URL
- `label`: binary target label

If original URLs cannot be redistributed because of source licensing, publish only the extracted feature table or keep the dataset gated/private.

## Recommended Splits

Recommended files for Hugging Face Dataset Viewer:

```text
train.parquet
validation.parquet
test.parquet
```

Use stratified splits so the legitimate/phishing ratio is preserved across splits.

## Licensing

The dataset license is currently marked as `other` until every original data source is documented and redistribution rights are verified.

Do not switch this to an open license such as CC BY 4.0, CC0, or MIT unless the source datasets allow redistribution under that license.

## Citation

```bibtex
@dataset{ozyurt_phishurl_dataset_2026,
  author = {Ozyurt, Alper},
  title = {PhishURL Dataset},
  year = {2026},
  url = {https://huggingface.co/datasets/alperozyyurt/phishurl-dataset}
}
```
