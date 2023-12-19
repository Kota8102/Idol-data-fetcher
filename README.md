# Serverless Frameworkを使ってみる

## 外部ライブラリの利用方法[Title](https://developer.kaizenplatform.com/entry/2021/03/30/150000)

```bash
serverless plugin install -n serverless-python-requirements
```

```bash
pip freeze > requirements.txt
```

## 使い方

サービスの作成方法
```bash
sls create --template aws-python3 --path ディレクトリ名
```

Pythonの外部ライブラリを利用する場合は、以下のコマンドを実行する
```bash
serverless plugin install -n serverless-python-requirements
```


### デプロイ方法

外部モジュールを利用する場合は、requirements.txtを作成する
```bash
pip freeze > requirements.txt
```

```bash
sls deploy --stage dev/prod --verbose(デバックあり)
```

```bash
sls invoke -f hello
```

削除方法
```bash
sls remove
```

## 管理しているLambda

| Lambda Function Name | Execution Time |
|----------------------|----------------|
| get-event-kolkol     |           |