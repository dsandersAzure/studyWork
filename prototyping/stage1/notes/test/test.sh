#
# Test Script
#
echo ""
echo "Clear notifications"
echo "==================="
echo ""
curl -X PUT localhost:5000/clear
echo ""
echo "Test 1 - The device is running"
echo "------------------------------"
echo ""
curl localhost:5000/
echo ""
echo "Test 2 - List all routes"
echo "------------------------"
echo ""
curl localhost:5000/notifications
echo ""
echo "Test 3 - Post a notification"
echo "----------------------------"
echo ""
curl -X POST -H "Content-Type: application/json" -d '{"note":"**Remember** Safe Sex is Good Sex", "action":"msmapp geo(234.12,123.45)"}' localhost:5000/notification
echo ""
echo "Test 4 - Post a notification"
echo "----------------------------"
echo ""
curl -X POST -H "Content-Type: application/json" -d '{"note":"This is just a notification", "action":"Do an action"}' localhost:5000/notification
echo ""
echo "Test 5 - Get notification 0"
echo "---------------------------"
echo ""
curl localhost:5000/notification/0
echo ""
echo "Test 6 - Get notification 1"
echo "---------------------------"
echo ""
curl localhost:5000/notification/1
echo ""
echo "Test 7 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:5000/notifications
echo ""
echo "Test 8 - List all possible actions"
echo "----------------------------------"
echo ""
curl localhost:5000/
echo ""
echo ""
echo "Test 9 - Update notification 0"
echo "------------------------------"
echo ""
curl -X PUT -H "Content-Type: application/json" -d '{"note":"updated: This is just a notification"}' localhost:5000/notification/0
echo ""
echo "Test 10 - Get notification 0"
echo "----------------------------"
echo ""
curl localhost:5000/notification/0
echo ""
echo "Test 11 - Lock Device"
echo "---------------------"
echo ""
curl -X PUT localhost:5000/lock
echo ""
echo "Test 12 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:5000/notifications
echo ""
echo "Test 13 - Unlock Device"
echo "-----------------------"
echo ""
curl -X PUT localhost:5000/unlock/1234
echo ""
echo "Test 14 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:5000/notifications
echo ""