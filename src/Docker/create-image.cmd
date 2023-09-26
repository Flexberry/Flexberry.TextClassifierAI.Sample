docker build --no-cache -f SQL\Dockerfile.PostgreSql -t reportstextclassifierai/postgre-sql ../SQL

docker build --no-cache -f Dockerfile -t reportstextclassifierai/app ../..

docker build --no-cache -f Dockerfile.ScikitLearnClassifier -t reportstextclassifierai/classifier ../..

docker build --no-cache -f Dockerfile.ScikitLearnSignatureClassifier -t reportstextclassifierai/signature-classifier ../..