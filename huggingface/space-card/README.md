---
title: PhishURL Detection Demo
emoji: 🔎
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 5.0.0
python_version: "3.10"
app_file: app.py
pinned: false
license: mit
tags:
- cybersecurity
- phishing
- url-classification
---

# PhishURL Detection Demo

Interactive demo for classifying URLs as legitimate or phishing/malicious.

The demo should:

- accept a single URL input,
- extract URL-based features,
- run the selected model,
- show the predicted label and confidence when available,
- show a short warning that the result is experimental and not a final security verdict.
