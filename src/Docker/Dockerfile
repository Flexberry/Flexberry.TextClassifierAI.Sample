FROM node:10 as ember_app

COPY /src/ember-app /ember-app

WORKDIR /ember-app

RUN \
  set -x; \
  yarn global add ember-cli@3.1.4; \
  yarn global add bower;

RUN \
  set -x; \
  yarn install ; \
  bower install  --allow-root;

RUN \
  set -x; \
  ember build --environment=docker

FROM mcr.microsoft.com/dotnet/sdk:3.1 as backend

COPY /src/ReportsTextClassifierAi /ReportsTextClassifierAi

WORKDIR /ReportsTextClassifierAi

RUN \
 dotnet restore ReportsTextClassifierAi.sln;\
 dotnet build ReportsTextClassifierAi.sln -c Release;\
 dotnet publish ODataBackend/ReportsTextClassifierAi.ODataBackend.csproj -c Release -o out -f netcoreapp3.1

FROM mcr.microsoft.com/dotnet/aspnet:3.1

#Устанавливаем tesseract и imagemagic.
RUN apt-get update \
 && apt-get -y install tesseract-ocr \
 && apt-get -y install tesseract-ocr-all \
 && apt-get -y install imagemagick
 
COPY /src/Docker/ImageMagic/policy.xml /etc/ImageMagick-6/policy.xml

WORKDIR /app

COPY --from=backend /ReportsTextClassifierAi/out ./
COPY --from=ember_app /ember-app/dist ./wwwroot/

# Check webapi responses
HEALTHCHECK --interval=60s --timeout=15s --start-period=20s \
  CMD curl -f "http://0.0.0.0/health" || exit

ENTRYPOINT ["dotnet", "ReportsTextClassifierAi.ODataBackend.dll"]
