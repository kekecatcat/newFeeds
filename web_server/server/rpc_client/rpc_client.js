var jayson = require('jayson');

// creat a client
var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

//Test RPC method
function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

function getNewsSummariesForUser(user_id, page_num, callback) {
    console.log('get news in rpc_client.')
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, error, response) {
        if (err) throw err;
        // console.log(response);
        callback(response);
    });
}

// Log a news click event for a user
function logNewsClickForUser(user_id, news_id) {
    console.log('calling log news click event handler')
    client.request('logNewsClickForUser', [user_id, news_id], function(err, error, response) {
        if (err) throw err;
        console.log(response);
    });
}
module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
}
