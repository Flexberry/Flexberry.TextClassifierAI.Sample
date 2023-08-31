docker build --no-cache -f SQL\Dockerfile.PostgreSql -t reportstextclassifierai/postgre-sql ../SQL

docker build --no-cache -f Dockerfile -t reportstextclassifierai/app ../..
