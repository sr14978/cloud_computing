
'use strict';

const express = require('express');

const app = express();

app.get('/', (req, res) => {
  res.send('hi');
});

app.get('*', (req, res) => {
  res.send('not available: home');
});

app.listen(process.env.PORT)

module.exports = app;
