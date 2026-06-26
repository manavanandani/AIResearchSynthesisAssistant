"""Command-line interface for AIResearchSynthesisAssistant."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Dict

from .models.feedback import FeedbackItem
from .pipeline.embedding_extractor import SemanticEmbeddingExtractor
from .pipeline.semantic_clusterer import SemanticClusterer
from .pipeline.prompt_orchestrator import PromptOrchestrator
from .benchmark.overlap_evaluator import OverlapEvaluator
from .benchmark.runtime_profiler import RuntimeProfiler
from .reporting.terminal_view import TerminalView
from .reporting.prd_generator import PRDGenerator


def load_corpus(file_path: str) -> List[FeedbackItem]:
    """Loads raw user feedback corpus from JSON."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Feedback corpus file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [FeedbackItem(**item) for item in data]


def load_baseline(file_path: str) -> Dict[str, str]:
    """Loads human ground-truth taxonomy mapping."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Baseline taxonomy file not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_pipeline(corpus: List[FeedbackItem], target_k: int = 5):
    """Executes embeddings, clustering, and prompt synthesis."""
    texts = [item.text for item in corpus]
    extractor = SemanticEmbeddingExtractor()
    embeddings = extractor.fit_transform(texts)

    clusterer = SemanticClusterer(min_clusters=4, max_clusters=6)
    labels = clusterer.fit_predict(embeddings, target_k=target_k)

    clustered = defaultdict(list)
    assignment_map = {}
    for idx, (label, item) in enumerate(zip(labels, corpus)):
        clustered[int(label)].append(item)

    orchestrator = PromptOrchestrator()
    synthesis = orchestrator.synthesize_all(clustered)

    cluster_to_title = {t.cluster_id: t.theme_title for t in synthesis.themes}
    for idx, (label, item) in enumerate(zip(labels, corpus)):
        assignment_map[item.feedback_id] = cluster_to_title.get(int(label), "General Usability")

    return synthesis, assignment_map


def cmd_synthesize(args):
    """Synthesizes qualitative feedback into theme clusters and PRD requirements."""
    corpus = load_corpus(args.corpus)
    synthesis, _ = run_pipeline(corpus, target_k=args.clusters)
    view = TerminalView()
    view.print_synthesis_summary(synthesis)


def cmd_benchmark(args):
    """Benchmarks AI cluster accuracy against manually-coded ground truth."""
    corpus = load_corpus(args.corpus)
    baseline = load_baseline(args.baseline)
    synthesis, assignments = run_pipeline(corpus, target_k=args.clusters)
    metrics = OverlapEvaluator.evaluate(synthesis, baseline, assignments)
    view = TerminalView()
    view.print_benchmark_table(metrics)


def cmd_profile(args):
    """Profiles pipeline execution time vs. manual synthesis."""
    corpus = load_corpus(args.corpus)
    synthesis, profile = RuntimeProfiler.profile(
        sample_count=len(corpus),
        execution_fn=lambda: run_pipeline(corpus, target_k=args.clusters)[0],
    )
    view = TerminalView()
    view.print_profiler_summary(profile)


def cmd_export_prd(args):
    """Exports full Product Requirements Document in markdown."""
    corpus = load_corpus(args.corpus)
    synthesis, assignments = run_pipeline(corpus, target_k=args.clusters)

    metrics = None
    if Path(args.baseline).exists():
        baseline = load_baseline(args.baseline)
        metrics = OverlapEvaluator.evaluate(synthesis, baseline, assignments)

    _, profile = RuntimeProfiler.profile(
        sample_count=len(corpus),
        execution_fn=lambda: synthesis,
    )

    markdown = PRDGenerator.generate_prd_markdown(synthesis, metrics, profile)
    out_path = Path(args.output)
    out_path.write_text(markdown, encoding="utf-8")
    print(f"✅ Successfully exported Synthesis PRD to {out_path}")


def main():
    parser = argparse.ArgumentParser(
        prog="synthesize",
        description="AIResearchSynthesisAssistant - LLM qualitative research pipeline",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Synthesize
    p_syn = subparsers.add_parser("synthesize", help="Synthesize feedback corpus into themes")
    p_syn.add_argument("--corpus", default="data/user_feedback_corpus.json", help="Path to corpus JSON")
    p_syn.add_argument("--clusters", type=int, default=5, help="Target cluster count")
    p_syn.set_defaults(func=cmd_synthesize)

    # Benchmark
    p_ben = subparsers.add_parser("benchmark", help="Benchmark against manually-coded baseline")
    p_ben.add_argument("--corpus", default="data/user_feedback_corpus.json", help="Path to corpus JSON")
    p_ben.add_argument("--baseline", default="data/ground_truth_taxonomy.json", help="Path to baseline JSON")
    p_ben.add_argument("--clusters", type=int, default=5, help="Target cluster count")
    p_ben.set_defaults(func=cmd_benchmark)

    # Profile
    p_pro = subparsers.add_parser("profile", help="Profile synthesis duration and efficiency gains")
    p_pro.add_argument("--corpus", default="data/user_feedback_corpus.json", help="Path to corpus JSON")
    p_pro.add_argument("--clusters", type=int, default=5, help="Target cluster count")
    p_pro.set_defaults(func=cmd_profile)

    # Export PRD
    p_prd = subparsers.add_parser("export-prd", help="Export PRD specification document")
    p_prd.add_argument("--corpus", default="data/user_feedback_corpus.json", help="Path to corpus JSON")
    p_prd.add_argument("--baseline", default="data/ground_truth_taxonomy.json", help="Path to baseline JSON")
    p_prd.add_argument("--clusters", type=int, default=5, help="Target cluster count")
    p_prd.add_argument("--output", default="SYNTHESIS_PRD.md", help="Output PRD path")
    p_prd.set_defaults(func=cmd_export_prd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
