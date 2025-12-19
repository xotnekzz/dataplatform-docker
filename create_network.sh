# 컨테이너간 통신을 위한 네트워크 생성
docker network create \
  --driver bridge \
  --subnet=10.100.0.0/24 \
  --gateway=10.100.0.1 \
  dataplatform-net
