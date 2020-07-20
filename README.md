# Teams Notifier

O Projeto é escrito em Python3.7 com a biblioteca pymsteams e tem como proposito se conectar ao Teams atravez de um Webhook e enviar uma Menssagem segmentada em 3 sessões.

- Cabecario com informacões da Release
- Conteudo do ChangeSet
- Autorizadores

## Enviroments Variables

Para uso o projeto faz leitura das seguinte variaveis.

|Variavel|Descricão|
|--|--|
|VSTS_USER| Conta de E-mail usada para criacão do Token |
|VSTS_PAT| Personal Autentication Token gerado no console do Azure DevOps |
|WEBHOOK| URL do WebHook criado no console do Teams |
|ORG_NAME|Nome da Organizacão|
|PROJECT_VERSION| Versão do Projeto M.N ("Major"."Minor") |
|BUILD_NUMBER| Numero da Build AAAAMMDD.nB (AnoMesDia.numeroBuild) |
|RELEASE_ID| ID da Release |
|RELEASE_STAGE_URL| URL do Frontend do Projeto |
|RELEASE_STAGE| Estagio de entrega da Release |
|PROJECT_NAME| Nome do Projeto |
|CHANGESET| Texto a ser enviado com as mudancas entregues na release (pode ser usado MD) |
|BUILDERS| Quem gerou o Build e é o solicitante da Release |

## Utilizando Container

Para execucão da build do container:


Compilar o python
```
python3 -m compileall .

for i in $(find . -name '*.pyc'); do j=$(echo $i | sed -e 's|__pycache__/||g' -e 's|cpython-37.||'); mv $i $j; done

```

Criacão da Imagem

```
cd deploy
mkdir app
cp ../source/send_Release.pyc ./app
docker build -t teamsnotifier .
```

Executando a Imagem

```
docker run --rm \
-e VSTS_USER="fulano.detal@devbeerops.club" \
-e VSTS_PAT="1t2o3k4e5n6" \
-e WEBHOOK="https://outlook.office.com/webhook/uuid/IncomingWebhook/uuid/uuid" \
-e PROJECT_VERSION="1.1" \
-e BUILD_NUMBER="20200613.1" \
-e RELEASE_ID="01" \
-e RELEASE_STAGE_URL="https://aplicacao.devbeerops.club" \
-e RELEASE_STAGE="STAGING" \
-e ORG_NAME="devbeerops" \
-e PROJECT_NAME="aplicacao" \
-e CHANGESET="$(cat docs/change_set.md)" \
-e BUILDERS="$(echo Fulano Detal)" \
teamsnotifier:latest
```