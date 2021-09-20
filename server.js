const express = require('express');
const serveStatic = require("serve-static");
const history = require('connect-history-api-fallback');
const path = require('path');
// start express server
app = express();
app.use(serveStatic(path.join(__dirname, 'dist')));

// view engine setup
app.set('views', path.join(__dirname, 'src/views'));
app.set('view engine', 'pug');

const staticFileMiddleware = express.static(__dirname);
app.use(staticFileMiddleware);
app.use(history({
  disableDotRule: true,
  verbose: true
}));
app.use(staticFileMiddleware);

const port = process.env.PORT || 80;
app.listen(port);