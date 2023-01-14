ip=`hostname -I | cut -d" " -f1`
echo "Starting server on port ${ip}:5000"
gunicorn --bind 0.0.0.0:5000 --workers=4 --log-file=all.log --log-level=info --access-logfile=access.log app:app