# Serverless Frameworkを使ってみる

## 外部ライブラリの利用方法

```bash
serverless plugin install -n serverless-python-requirements
```

```bash
pip freeze > requirements.txt
```

## 使い方

デプロイ方法
```bash
sls deploy --stage dev/prod --verbose(デバックあり)
```

```bash
sls invoke -f hello
```

## 管理しているLambda

| Lambda Function Name | Execution Time |
|----------------------|----------------|
| get-event-kolkol     |           |