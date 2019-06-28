: "${DOCKER_TAG:=test}"
: "${BASE_BUILD_IMAGE:=thinkport/portfolio-base:latest}"

docker build -f docker/Dockerfile.base -t "${BASE_BUILD_IMAGE}" .
docker build -f docker/Dockerfile -t thinkpoet/portfolio-tool:${DOCKER_TAG} --build-arg BASE_IMAGE="${BASE_BUILD_IMAGE}" .
