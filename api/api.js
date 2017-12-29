
'use strict';

const express = require('express');

const app = express();

app.get('/api/upload', (req, res) => {
  res.send('wow there, you trying to upload something. I haven\'t implemented that yet');
});

app.listen(process.env.PORT)

module.exports = app;
