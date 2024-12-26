# Local development: Run `python src/main.py`
# HOST='localhost:5000'

# Remote development: Run container in Google Cloud Run
# HOST='https://wind-farms-81983497920.australia-southeast1.run.app'

# Should qualify
curl -X POST $HOST/address/qualify -d '{"address": "5 Fahey St, Wonthaggi VIC 3995"}'

# Shoud not qualify
curl -X POST $HOST/address/qualify -d '{"address": "3 McGarvey Rd, Inverloch VIC 3996"}'