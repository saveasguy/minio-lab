#!/bin/bash

set -m

mkdir minio
MINIO_SCANNER_SPEED=fastest minio server minio --console-address :9001 &

mc ready local 2>&1 > /dev/null
while [[ $? != 0 ]]; do
    mc ready local 2>&1 > /dev/null
done

mc alias set local http://127.0.0.1:9000 minioadmin minioadmin
mc admin user add local myuser myusersecretkey
mc admin policy attach local readwrite --user=myuser
mc mb local/mybucket
mc quota set local/mybucket --size 32MB

fg
