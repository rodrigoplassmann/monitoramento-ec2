#!/bin/bash
source /home/ubuntu/sistema-monitoramento/.env
mysql monitoramento <<EOF
DELETE FROM metrics WHERE created_at < NOW - INTERVAL 30 DAY;
EOF
