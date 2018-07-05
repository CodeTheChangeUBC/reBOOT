# ORIGINAL AUTHOR: @bobheadxi
# This script handles local database creation easier.
# Run with `sh scripts/start_db.sh`

postgres -V
if [ "$?" -gt "0" ]; then
  echo "Postgres not installed! Would you like to install it? (y/n)"
  echo "Note that you must have Homebrew installed for this to work."
  read choice
  if [ "$choice" == "y" ]; then
    echo "Installing postgres..."
    brew install postgresql
    initdb /usr/local/var/postgres
    echo "Process complete - please run 'make db' again."
    exit
  else
    echo "Alright, bye!"
    exit
  fi
fi

echo "Killing existing postgres processes..."
pg_ctl -D /usr/local/var/postgres stop -s -m fast
pg_ctl -D /usr/local/var/postgres start
while true; do
  pg_ctl -D /usr/local/var/postgres status
  if [ "$?" -gt "0" ]; then
    echo "Waiting for postgres to start..."
    sleep 3
  else
    break
  fi
done
exit