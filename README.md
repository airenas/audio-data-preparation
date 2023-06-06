# audio-data-preparation
Data preparation scripts for audio corpus

## Prepare python env

```bash
conda create --name corpus python=3.10
conda activate corpus
make install/req
```

## Corpus preparation

```bash
cd egs/<corpus>
make build
```
