# Idol Calendar

たくさんのライブを抱える方々に向けて、複数のアイドルの
ライブの予定を1つのカレンダーにまとめて表示することができるサービスです。

## URL

[Idol Calendar](https://idol-calendar.info)

## 使用技術

- React
- TypeScript
- Python
- Serverless Framework
- AWS
  - Lambda
  - API Gateway
  - DynamoDB
  - S3


## インフラ構成図

![アーキテクチャ図](documents/images/アーキテクチャ図.drawio.svg)


## 使い方

### Serverless Framework

#### Serverless Frameworkのプラグインのインストール方法

以下のコマンドを実行することで、Pythonの外部ライブラリを利用することができる

```bash
serverless plugin install -n serverless-python-requirements
```

#### Serverless Frameworkのサービスの作成方法

以下のコマンドを実行する

```bash
sls create --template aws-python3 --path ディレクトリ名
```

Pythonの外部ライブラリを利用する場合は、以下のコマンドを実行する

```bash
serverless plugin install -n serverless-python-requirements
```

### Serverless Frameworkを用いたデプロイ方法

0. 外部モジュールを利用する場合は、requirements.txtを作成する

    ```bash
    pip freeze > requirements.txt
    ```

1. dev環境へとデプロイする

    ```bash
    sls deploy --stage dev/prod 
    ```

2. デプロイしたLambdaを実行する

    ```bash
    sls invoke -f hello
    ```

3. 問題なれば、dev環境を削除する

    ```bash
    sls remove --stage dev
    ```

4. prod環境へとデプロイする

    ```bash
    sls deploy --stage prod
    ```

## Note

### デプロイ時にエラーが発生した場合

`--verbose`オプションをつけることで、詳細なエラーが表示される

```bash
sls deploy --stage dev --verbose
```

## 管理しているLambda

### イベント情報の取得 (S3への保存)
| Lambda Function Name | 概要                                    |
|----------------------|----------------------------------------|
| get-event-kolkol     | Kolokolのホームページからイベント情報を取得する  |
| get-event-yosugala   | yosugalaのホームページからイベント情報を取得する |

### イベント情報の登録 (Dynamoへの登録)

### APIの作成 (API Gateway)