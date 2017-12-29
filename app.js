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
app.get('/names', function (req, res) {
    function callback() {
        res.json(result);
    }
    if (req.query.father && req.query.mother) {
        var father = req.query.father,
            mother = req.query.mother;
        if (votes[father + " and " + mother]) {
            res.json({ statusCode: 200, data: votes[father + " and " + mother] });
        } else {
            father = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&pithumbsize=500&titles=" + father;
            mother = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&pithumbsize=500&titles=" + mother;
            var waiting = 2;
            request({ method: 'GET', url: father }, function (err, res, data) {
                if (err || res.statusCode !== 200) console.log("GET request failed, error " + res.statusCode + " + " + err); 
                else father = data.query.pages[Object.keys(data.query.pages)[0]].thumbnail.source;
                if (--waiting === 0) callback();
            });
            request({ method: 'GET', url: mother }, function (err, res, data) {
                if (err || res.statusCode !== 200) console.log("GET request failed, error " + res.statusCode + " + " + err);
                else mother = data.query.pages[Object.keys(data.query.pages)[0]].thumbnail.source;
                if (--waiting === 0) callback();
            });
        }
    } else res.json({ statusCode: 400, data: "Bad Request: URI Parameter missing" });
});
app.get('/', function (req, res) { res.sendFile(__dirname + '/public/index.html'); });
app.get('*', function (req, res) { res.sendFile(__dirname + '/public/error.html'); });
app.set('port', process.env.PORT || listenOnPort);
http.listen(app.get('port'));