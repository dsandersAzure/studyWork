#portToUse=$1
#if [ "$1x" == "x" ]; then portToUse='5000'; fi

echo ""
echo "** Starting Port ${portToUse} **"
echo "$1 = ${1}"
echo "$portToUse = ${portToUse}"
echo ""

echo "server {" > notes_final.conf
echo "    listen      ${portToUse};" >> notes_final.conf
echo "    server_name localhost;" >> notes_final.conf
echo "    charset     utf-8;" >> notes_final.conf
echo "    client_max_body_size 75M;" >> notes_final.conf
echo "" >> notes_final.conf
echo "    location / { try_files \$uri @yourapplication; }" >> notes_final.conf
echo "    location @yourapplication {" >> notes_final.conf
echo "        include uwsgi_params;" >> notes_final.conf
echo "        uwsgi_pass 127.0.0.1:3031;" >> notes_final.conf
echo "    }" >> notes_final.conf
echo "}" >> notes_final.conf

service nginx start
/flask/bin/uwsgi notes_final.ini
#/flask/bin/uwsgi --http :5000 --wsgi-file runserver.py --callable app --master --processes 4 --threads 2
#/flask/bin/python3 /notes/runserver.py