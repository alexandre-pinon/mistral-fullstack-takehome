#!/bin/bash

./scripts/setup_integration_test.sh &&
./scripts/run_integration_test_no_pre_post.sh &&
./scripts/cleanup_integration_test.sh
