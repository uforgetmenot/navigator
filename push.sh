#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME=${1:-navigator-app}
IMAGE_TAG=${2:-latest}
LOCAL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
REMOTE_REGISTRY=${3:-registry.seadee.com.cn:5000}
REMOTE_IMAGE="${REMOTE_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "Running docker compose build"
docker compose build

if ! docker image inspect "${LOCAL_IMAGE}" >/dev/null 2>&1; then
	echo "Local image ${LOCAL_IMAGE} not found" >&2
	exit 1
fi

echo "Tagging ${LOCAL_IMAGE} -> ${REMOTE_IMAGE}"
if ! docker tag "${LOCAL_IMAGE}" "${REMOTE_IMAGE}"; then
	echo "Failed to tag image" >&2
	exit 1
fi

echo "Pushing ${REMOTE_IMAGE}"
if ! docker push "${REMOTE_IMAGE}"; then
	echo "Failed to push image" >&2
	exit 1
fi