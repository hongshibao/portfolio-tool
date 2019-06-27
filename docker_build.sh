: "${DOCKER_TAG:=test}"

docker build -f docker/Dockerfile.base -t thinkpoet/portfolio-tool-base:latest .
docker build -f docker/Dockerfile -t thinkpoet/portfolio-tool:${DOCKER_TAG} --build-arg BASE_IMAGE="thinkpoet/portfolio-tool-base:latest" .
