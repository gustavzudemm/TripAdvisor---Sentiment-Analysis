# TripAdvisor---Sentiment-Analysis
Sentiment Analysis of german reviews on TripAdvisor

## Description
- Dataset contains ~1000 german reviews from TripAdvisor about Lufthansa
- Converted ratings (1.0 - 5.0, 1 being the worst and 5 being the best rating) to categorical values
  - 1.0 - 2.0: negative
  - 3.0: neutral
  - 4.0 - 5.0: positive
- Basic Preprocessing (stopword-removal, non-alphanumeric-char removal, lemmatization)
- ML-Model: *Logistic Regression*
  - Tfidf-Vectorization (max_feat=50)
  - max_iter=500
## Results
- Training Accuracy: 86.7%
- Test Accuracy: 81.5%

- AUC-ROC Train: 85%
- AUC-ROC Test: 74%
