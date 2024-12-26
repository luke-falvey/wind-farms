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

Specify `--platform` to build the image for the target platform (Google Cloud runs x86_64 VMs)

```bash
docker buildx build --platform linux/amd64 -t wind-farms .
```

### Running docker image


```bash
docker run -p 5000:5000 -e GOOGLE_MAPS_API_KEY='<YOUR_GOOGLE_MAPS_API_KEY>' wind-farms
```

### Pushing image to registry

Google Artifact Registry requires:
- ARTIFACT_REGISTRY: `australia-southeast1-docker.pkg.dev`
- GCP_PROJECT_ID: `<YOUR_GCP_PROJECT_ID>`
- IMAGE_PATH: `YOUR_IMAGE_PATH`

```bash
ARTIFACT_REGISTRY='<YOUR_ARTIFACT_REGISTRY>'
GCP_PROJECT_ID='<YOUR_GCP_PROJECT_ID>'
IMAGE_PATH='<YOUR_IMAGE_PATH>'
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin $ARTIFACT_REGISTRY
docker tag wind-farms $ARTIFACT_REGISTRY/$GCP_PROJECT_ID/$IMAGE_PATH
docker push $ARTIFACT_REGISTRY/$GCP_PROJECT_ID/$IMAGE_PATH
```