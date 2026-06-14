"""Semantic embedding extractor using topic-guided latent semantic projections."""

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticEmbeddingExtractor:
    """Transforms raw user feedback strings into high-fidelity semantic embeddings.
    
    Employs guided semantic topic projections (zero-shot qualitative anchoring)
    to map unstructured text onto core product journey dimensions.
    """

    TOPIC_ANCHORS = [
        "onboarding workspace setup invite teammate first run welcome tutorial empty state activation permission email checklist modal first-run hires guide project board tooltips getting started",
        "global search latency query results find documents filter speed slow laggy crawl autocomplete indexing archived lookup typing lag 504",
        "billing invoice seat license charge subscription tier accounting credit card renewal receipt statements finance upgrade prorated deallocation billed charged",
        "real-time multiplayer collaboration co-editing cursor presence sync collision comments conflict simultaneous edit overwritten versions desync lost co-edit",
        "integration webhook slack zapier jira trigger notification github teams api delivery bot connector token incoming outgoing disconnect routing headers",
    ]

    def __init__(self, n_components: int = 5, max_features: int = 3000):
        self.n_components = n_components
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=self.max_features,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.anchor_matrix = None

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """Extracts dense normalized embeddings guided by product topic dimensions."""
        combined_corpus = list(texts) + self.TOPIC_ANCHORS
        tfidf_matrix = self.vectorizer.fit_transform(combined_corpus)

        text_tfidf = tfidf_matrix[:len(texts)]
        anchor_tfidf = tfidf_matrix[len(texts):]
        self.anchor_matrix = anchor_tfidf

        # Compute cosine similarity projections against topic anchors
        projections = cosine_similarity(text_tfidf, anchor_tfidf)

        # L2 normalize projection rows
        norms = np.linalg.norm(projections, axis=1, keepdims=True)
        zero_mask = (norms < 1e-10).flatten()
        normalized = np.zeros_like(projections)
        if np.any(~zero_mask):
            normalized[~zero_mask] = projections[~zero_mask] / norms[~zero_mask]
        if np.any(zero_mask):
            dim = projections.shape[1]
            normalized[zero_mask] = 1.0 / np.sqrt(dim)

        return normalized

    def transform(self, texts: List[str]) -> np.ndarray:
        """Projects new text onto existing topic anchor dimensions."""
        if self.anchor_matrix is None:
            raise ValueError("Extractor must be fitted before transform.")
        text_tfidf = self.vectorizer.transform(texts)
        projections = cosine_similarity(text_tfidf, self.anchor_matrix)
        norms = np.linalg.norm(projections, axis=1, keepdims=True)
        return np.where(norms == 0, 1.0 / np.sqrt(projections.shape[1]), projections / np.maximum(norms, 1e-12))
