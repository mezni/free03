#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}

echo "Deploying to $ENVIRONMENT..."

case $ENVIRONMENT in
    development)
        docker-compose -f deployments/docker/docker-compose.yml up -d
        ;;
    staging|production)
        kubectl apply -k deployments/kubernetes/overlays/$ENVIRONMENT
        kubectl rollout status deployment/$service_name
        ;;
    *)
        echo "Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "Deployment completed! 🚀"
