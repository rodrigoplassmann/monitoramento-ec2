#!/bin/bash

mysql monitoramento <<EOF
DELETE FROM metrics WHERE created_at < NOW() - INTERVAL 30 DAY;
EOF
