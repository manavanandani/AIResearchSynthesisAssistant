"""Tests for clustering and silhouette score."""

import numpy as np
from src.pipeline.semantic_clusterer import SemanticClusterer


def test_clustering_partition():
    # 3 distinct 2D point groups
    group1 = np.random.normal(loc=[10, 0], scale=0.2, size=(10, 2))
    group2 = np.random.normal(loc=[0, 10], scale=0.2, size=(10, 2))
    group3 = np.random.normal(loc=[-10, -10], scale=0.2, size=(10, 2))
    data = np.vstack([group1, group2, group3])

    clusterer = SemanticClusterer(min_clusters=2, max_clusters=4)
    labels = clusterer.fit_predict(data, target_k=3)

    assert len(labels) == 30
    assert len(set(labels)) == 3
    assert clusterer.silhouette_score_ > 0.6
