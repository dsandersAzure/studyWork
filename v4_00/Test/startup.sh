#
# $portToUse is an environment variable required to set the nginx configuration
# (see below). We check the variable has been set - if it hasn't, then the
# default of 5000 is used.
#
if [ "${portToUse}x" == "x" ]; then portToUse='5000'; fi
if [ "${serverName}x" == "x" ]; then serverName='localhost'; fi
#
# Debug statements - access through 'docker logs <containername>'
# For this app, that is: docker logs notesfinal<portToUse>
#
echo ""
echo "** Starting Port ${portToUse} **"
echo ""
#
# Create the nginx configuration file dynamically, so that the correct
# port number is assigned. This ensures that the port is mapped and that
# the correct URL's are returned. In addition to this step, another step
# is used in notes/resources/Config.py - there, the port number is used
# to generate full URLs as Flask was dropping the port numbers. A final
# part of this sequence is runserver.py; this is the Python program that
# is called by the UWSGI call below. It stores the environment variable
# portToUse in Config.py
#
echo "server {" > Test_uwsgi.conf
echo "    listen      ${portToUse};" >> Test_uwsgi.conf
echo "    server_name ${serverName};" >> Test_uwsgi.conf
echo "    charset     utf-8;" >> Test_uwsgi.conf
echo "    client_max_body_size 75M;" >> Test_uwsgi.conf
echo "" >> Test_uwsgi.conf
echo "    location / { try_files \$uri @yourapplication; }" >> Test_uwsgi.conf
echo "    location @yourapplication {" >> Test_uwsgi.conf
echo "        include uwsgi_params;" >> Test_uwsgi.conf
echo "        uwsgi_pass 127.0.0.1:3031;" >> Test_uwsgi.conf
echo "    }" >> Test_uwsgi.conf
echo "}" >> Test_uwsgi.conf
#
# Build the notifications_uqsgi.ini file
#
echo "[uwsgi]" > Test_uwsgi.ini
echo "socket=127.0.0.1:3031" >> Test_uwsgi.ini
echo "chdir = /Test/" >> Test_uwsgi.ini
echo "wsgi-file=runserver.py" >> Test_uwsgi.ini
echo "callable=app" >> Test_uwsgi.ini
echo "workers=2" >> Test_uwsgi.ini
echo "processes=4" >> Test_uwsgi.ini
echo "threads=1" >> Test_uwsgi.ini
echo "stats=127.0.0.1:9191" >> Test_uwsgi.ini
echo "stats-http=127.0.0.1:9191" >> Test_uwsgi.ini
#
# Start nginx. Remove the default sites and symbolically link the configuration
# file to the nginx conifugration directory.
#
rm -r -f /etc/nginx/sites-enabled/default
ln -s /Test/Test_uwsgi.conf /etc/nginx/conf.d/Test_uwsgi.conf
service nginx start
#
# Start Redis
#
redis-server &
#
# Start UWSGI and pass the notes_final.ini file.
#
#runLocally=False; export runLocally
uwsgi Test_uwsgi.ini

