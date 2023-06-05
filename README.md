# audio-data-preparation
Data preparation scripts for audio corpus

## Preparation

```bash
conda create --name corpus python=3.10
cobda activate corpus
make install/req
```

## Corpus preparation

```bash
cd egs/<corpus>
make build
```
