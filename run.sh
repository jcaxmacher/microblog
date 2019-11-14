#!/bin/bash -xe
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

yum update -y
yum install -y shadow-utils util-linux git python3 mariadb-devel gcc python3-devel
adduser web

cat <<EOF >/tmp/run.sh
git clone https://github.com/jcaxmacher/microblog.git;
python3 -m venv venv;
source venv/bin/activate;
cd microblog;
pip install -e .;

export FLASK_APP=microblog
export APP_NAME=example-a;
export ENV_NAME=prod;
export AWS_DEFAULT_REGION=us-east-1;
sleep 120
flask init-db

gunicorn -w 4 microblog.wsgi:app -b 0.0.0.0:5000
EOF

# pyagent run -c /path/to/appdynamics.cfg -- gunicorn -w 8 -b '0.0.0.0:9000' appdynamics.scripts.wsgi:application

sudo -i -H -u web bash -c "$(cat /tmp/run.sh)"