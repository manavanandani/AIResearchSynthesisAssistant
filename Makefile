.PHONY: test synthesize benchmark profile prd clean

test:
	python3 -m pytest tests/ -v

synthesize:
	python3 -m src.cli synthesize --corpus data/user_feedback_corpus.json

benchmark:
	python3 -m src.cli benchmark --corpus data/user_feedback_corpus.json --baseline data/ground_truth_taxonomy.json

profile:
	python3 -m src.cli profile --corpus data/user_feedback_corpus.json

prd:
	python3 -m src.cli export-prd --corpus data/user_feedback_corpus.json --output SYNTHESIS_PRD.md

clean:
	rm -rf __pycache__ src/__pycache__ src/*/__pycache__ tests/__pycache__ .pytest_cache
