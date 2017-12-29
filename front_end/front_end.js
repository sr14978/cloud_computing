
'use strict';

const express = require('express');

const app = express();

app.get('/', (req, res) => {
  res.redirect('/static/index.html')
});

app.listen(process.env.PORT)

module.exports = app;
