"""Tests for semantic embedding extraction."""

import numpy as np
from src.pipeline.embedding_extractor import SemanticEmbeddingExtractor


def test_fit_transform_embeddings():
    texts = [
        "The onboarding flow is hard to use and confusing",
        "Search is painfully slow when looking up tickets",
        "Billing was charged twice for deactivated seats",
        "Real-time multiplayer cursors lag and desync",
        "Slack webhook notifications fail to trigger",
    ]
    extractor = SemanticEmbeddingExtractor()
    embeddings = extractor.fit_transform(texts)

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape[0] == 5
    assert embeddings.shape[1] == 5
    # Embeddings should be unit normalized
    norms = np.linalg.norm(embeddings, axis=1)
    np.testing.assert_allclose(norms, np.ones(5), atol=1e-5)
