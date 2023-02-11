#!/usr/bin/env bash

set -e;

IMAGE_TAG="gcr.io/shallweswim/shallweswim"

gcloud builds submit --tag ${IMAGE_TAG}
gcloud run deploy --image ${IMAGE_TAG} shallweswim
