'use strict';
var listenOnPort = 8084,
    combinations = require('./combinations.json'),
    debug = require('debug'),
    path = require('path'),
    favicon = require('serve-favicon'),
    logger = require('morgan'),
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    express = require('express'),
    app = express(),
    http = require('http').Server(app),
    request = require('request'),
    fs = require("fs");

app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(favicon(__dirname + '/public/favicon.ico'));
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}
app.get('/combine', function (req, res) {
    function callback() {
        res.json(result);
    }
    if (req.query.father && req.query.mother) {
        var waiting = 1,
            father = req.query.father,
            mother = req.query.mother;
        if (votes[father + " and " + mother]) {
            res.json({ statusCode: 200, data: votes[father + " and " + mother] });
        } else {
            //https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&pithumbsize=500&titles=Jennifer+Lawrence
            request({ method: 'GET', url: uri.href }, function (err, res, body) {
                if (err)
                    console.log("Get request failed: " + err);
                if (res.statusCode === 200) {
                    var article = unfluff(body, 'en');
                    if (article) {
                        var title = article.softTitle, words = article.text.split(" ");
                    }
                } else { console.log("GET request failed, error code: " + res.statusCode); }
                if (--waiting === 0) callback();
            });
        }
    } else res.json({ statusCode: 400, data:"Bad Request: URI Parameter missing"});
});
app.get('/', function (req, res) { res.sendFile(__dirname + '/public/index.html'); });
app.get('*', function (req, res) { res.sendFile(__dirname + '/public/error.html'); });
app.set('port', process.env.PORT || listenOnPort);
http.listen(app.get('port'));