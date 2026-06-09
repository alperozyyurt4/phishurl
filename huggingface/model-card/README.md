---
license: mit
language:
- en
- tr
tags:
- cybersecurity
- phishing
- url-classification
- malicious-url-detection
- tabular-classification
- scikit-learn
- tensorflow
pipeline_tag: tabular-classification
library_name: scikit-learn
datasets:
- alperozyyurt/phishurl-dataset
metrics:
- accuracy
- f1
- roc_auc
---

# PhishURL Detection

PhishURL Detection classifies URLs as legitimate or phishing/malicious using handcrafted URL features and multiple machine learning and deep learning models.

Label convention:

- `0`: legitimate / safe
- `1`: phishing / malicious

## Model Summary

The project includes classical ML and neural models trained on URL-derived features:

| Model | Test Accuracy | F1 Score | AUC |
|---|---:|---:|---:|
| Random Forest | 0.9640 | 0.9640 | 0.9931 |
| XGBoost | 0.9587 | 0.9587 | 0.9935 |
| CNN | 0.9587 | 0.9587 | 0.9935 |
| Decision Tree | 0.9560 | 0.9560 | 0.9857 |
| ANN | 0.9547 | 0.9546 | 0.9920 |
| LightGBM | 0.9541 | 0.9541 | 0.9921 |
| DNN | 0.9219 | 0.9215 | 0.9175 |

The best reported model is Random Forest by test accuracy. XGBoost and CNN have the highest reported AUC among the included models.

## Features

The feature extractor creates URL-based signals including:

- URL, hostname, path, and query lengths
- Special character counts
- Digit and letter ratios
- IP address and punycode checks
- TLD checks
- Suspicious security and account keywords
- Entropy
- Typosquatting and brand-similarity indicators

## Intended Use

This model is intended for:

- Academic phishing URL detection experiments
- Security education demos
- Baseline malicious URL classification research
- Prototype triage tools

It should not be used as the only production security control. Real systems should combine model predictions with browser reputation, DNS intelligence, domain age, certificate metadata, sandboxing, and human review.

## Limitations

- The model uses handcrafted URL features and may miss attacks that require page content, hosting behavior, DNS history, or live threat intelligence.
- New phishing campaigns and domain-generation strategies can reduce accuracy over time.
- Reported metrics depend on the dataset split and labeling quality.
- Pickle model files should only be loaded in trusted environments.

## Citation

If this project helps your work, cite the repository:

```bibtex
@software{ozyurt_phishurl_detection_2026,
  author = {Ozyurt, Alper},
  title = {PhishURL Detection},
  year = {2026},
  url = {https://github.com/alperozyyurt4/phishurl}
}
```

## License

Code and model packaging are released under the MIT License. Dataset redistribution rights must be verified separately before publishing the full dataset.
