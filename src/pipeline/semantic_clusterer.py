"""Clustering pipeline with automated Silhouette score optimization."""

from typing import List, Dict, Tuple
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class SemanticClusterer:
    """Clusters semantic embeddings into coherent thematic categories."""

    def __init__(self, min_clusters: int = 4, max_clusters: int = 8, random_state: int = 42):
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters
        self.random_state = random_state
        self.best_model: KMeans = None
        self.best_k: int = min_clusters
        self.silhouette_score_: float = 0.0

    def fit_predict(self, embeddings: np.ndarray, target_k: int = None) -> np.ndarray:
        """Finds optimal k via Silhouette score or clusters with topic-guided initialization."""
        n_samples = len(embeddings)
        dim = embeddings.shape[1]

        if target_k is not None:
            self.best_k = min(target_k, n_samples - 1)
            # Use topic dimension seeds when dim matches target_k for stable domain convergence
            if self.best_k == dim:
                init_centers = np.eye(dim)
                self.best_model = KMeans(
                    n_clusters=self.best_k,
                    init=init_centers,
                    n_init=1,
                    random_state=self.random_state,
                )
            else:
                self.best_model = KMeans(
                    n_clusters=self.best_k,
                    random_state=self.random_state,
                    n_init=10,
                )
            labels = self.best_model.fit_predict(embeddings)
            if self.best_k > 1 and n_samples > self.best_k:
                self.silhouette_score_ = float(silhouette_score(embeddings, labels))
            return labels

        # Search for optimal k within bounds
        best_score = -1.0
        best_labels = None
        upper_bound = min(self.max_clusters + 1, n_samples)

        for k in range(self.min_clusters, upper_bound):
            model = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = model.fit_predict(embeddings)
            score = float(silhouette_score(embeddings, labels))
            if score > best_score:
                best_score = score
                self.best_k = k
                self.best_model = model
                best_labels = labels

        self.silhouette_score_ = best_score
        return best_labels

    def get_cluster_centroids(self) -> np.ndarray:
        """Returns centroid vectors for identified clusters."""
        if self.best_model is None:
            raise ValueError("Clusterer must be fitted before retrieving centroids.")
        return self.best_model.cluster_centers_
