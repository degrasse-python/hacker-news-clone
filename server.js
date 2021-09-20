const express = require('express');
const history = require('connect-history-api-fallback');
const path = require('path');
const serveStatic = require("serve-static");

const staticFileMiddleware = express.static(path.join(__dirname + '/dist'));

// start express server
app = express();
app.use(staticFileMiddleware);
app.get(/.*/, function(req, res) {
  res.sendfile(__dirname + "/dist/index.html");
});

/*
app.use(history({
  disableDotRule: true,
  verbose: true,
  logger: console.log.bind(console)
}));
*/


var port = process.env.PORT || 8000 ;
app.listen(port, () => {
  console.log('Server listening')
});