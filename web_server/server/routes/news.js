var express = require('express');
var rpc_client = require('../rpc_client/rpc_client')
var router = express.Router();


router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
    console.log('Load news from Node.js server')
 
    user_id = req.params['userId'];
    page_num = req.params['pageNum'];

    rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {
        // console.log('in response')
        // console.log(response)
        res.json(response)
    });
}); 

/* Log news click */
router.get('/userId/:userId/newsId/:newsId', function(req, res, next) {
    console.log('Load one news from Noed.js server');
    user_id = req.params['userId'];
    news_id = req.params['newsId'];


    rpc_client.logNewsClickForUser(user_id, news_id);
    res.status(200);
});

module.exports = router;