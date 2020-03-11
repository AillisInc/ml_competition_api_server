# ml_competition_api_server
- Web API server to calculate competition metrics for [this machine learning competition platform](https://github.com/AillisInc/ml_competition_platform)
- This code is written in Python and Flask web framework.

## Overall Architecture
- English version is still work in progress.

<img src="https://img.esa.io/uploads/production/attachments/9766/2020/03/15/40878/b172e725-c9e1-497d-9d20-d3184f2a94a2.jpg"  alt="imaeg" width="1000"/>

## How to setup development environment

### Setup environment variables.

```bash
cp .env.sample .env # Edit .env file according to your favorable environment
vim .env
```

Copy the following text to .env file.
```bash
API_KEY_TOKEN=secret_key
```

### Start server
start server with following command

```bash
python main.py
```

#### Endpoint to access API server
http://localhost:8000

## Default metrics
- [AUC for classification (/metrics/AUC)](https://github.com/AillisInc/ml_competition_api_server/blob/37ca11e75de50268f636c339ec1cc8f78c959b8d/main.py#L21)
- [mAP for detection (/metrics/mAP)](https://github.com/AillisInc/ml_competition_api_server/blob/37ca11e75de50268f636c339ec1cc8f78c959b8d/main.py#L34)


## How to define original metric
- Still work in progress

## License
MIT