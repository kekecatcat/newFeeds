var auth = require('./routes/auth');
var bodyParser = require('body-parser');
var cors = require('cors');
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var index = require('./routes/index');
var news = require('./routes/news');
var config = require('./config/config.json');
var _ = require('./models/main.js').connect(config.mongoDbUri);
var authCheckMiddleware = require('./middleware/auth_checker');
var passport = require('passport');

var app = express();
app.use(bodyParser.json());

// Load passport strategies.
app.use(passport.initialize());
var localSignUpStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignUpStrategy);
passport.use('local-login', localLoginStrategy);



// view engine setup
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');

app.use(cors());

app.use('/static',
express.static(path.join(__dirname, '../client/build/static/')));

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});


app.use('/', index);
app.use('/auth',auth);
app.use('/news', authCheckMiddleware);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  res.status(404);
});


module.exports = app;
