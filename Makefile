.PHONY: help build run test sbom

IMAGE := resilience-metrics

help:
	@echo "Targets: build, run, hub-run, test, sbom"

build:
	docker build -t $(IMAGE) .

run:
	@echo "Running $(IMAGE) on examples/synth.csv -> analysis.json"
	docker run --rm -u $$(id -u):$$(id -g) -v "$(PWD)/examples":/data $(IMAGE) analyze --csv /data/synth.csv --out /data/analysis.json

hub-run:
	@echo "Running eliotsystem/$(IMAGE):latest on examples/synth.csv -> analysis.json"
	docker run --rm -v "$(PWD)/examples":/data eliotsystem/$(IMAGE):latest analyze --csv /data/synth.csv --out /data/analysis.json

test:
	python -m unittest discover -s tests -p "test_*.py"

sbom:
	pip freeze > SBOM.txt
