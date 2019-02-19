var client = require('./rpc_client');

//Invoke 'add'.
client.add(1, 3, function(response) {
    console.assert(response == 4);
});

client.getNewsSummariesForUser('test_user', 2, function(response) {
    console.assert(response != null);
});