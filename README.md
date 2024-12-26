# Wind Farms

## Getting Started (Mac)

### Python Virtual Environment Setup

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Running the project

```bash
export GOOGLE_MAPS_API_KEY="<YOUR_GOOGLE_MAPS_API_KEY>"
python src/main.py
```


### Building docker image


```bash
docker build -t wind-farms .
```

### Running docker image


```bash
docker run -p 5000:5000 -e GOOGLE_MAPS_API_KEY='<YOUR_GOOGLE_MAPS_API_KEY>' wind-farms
```