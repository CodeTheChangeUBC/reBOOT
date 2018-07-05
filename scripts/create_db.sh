# ORIGINAL AUTHOR: @bobheadxi
# This script handles local database creation easier.
# Run with `sh scripts/create_db.sh`

createuser -s root
createdb reboot
echo "Local database ready to go!"
exit