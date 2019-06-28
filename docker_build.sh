: "${DOCKER_IMAGE:=thinkpoet/portfolio-tool}"
: "${DOCKER_TAG:=test}"
: "${BASE_BUILD_IMAGE:=thinkport/portfolio-base:latest}"

pipenv lock -r | tail -n +2 > requirements.txt

docker build -f docker/Dockerfile.base -t "${BASE_BUILD_IMAGE}" .
docker build -f docker/Dockerfile -t ${DOCKER_IMAGE}:${DOCKER_TAG} --build-arg BASE_IMAGE="${BASE_BUILD_IMAGE}" .
