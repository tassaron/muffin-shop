# Run a development server (not in debug mode!)

if [ -z "$1" ]; then
    port=5000
else
    port="$1"
fi

#let stats_port=$port+50

uwsgi --socket 0.0.0.0:$port --protocol=http --disable-logging --log-4xx --log-5xx --auto-procname --module muffin_shop.run --need-app --py-autoreload=1 --master --processes 4 --single-interpreter --enable-threads
#--stats-http --stats 0.0.0.0:$stats_port
