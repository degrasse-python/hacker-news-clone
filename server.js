const express = require('express');
const serveStatic = require("serve-static");
const history = require('connect-history-api-fallback');
const path = require('path');
const staticFileMiddleware = express.static(path.join(__dirname + '/dist'));

// start express server
app = express();
app.use(staticFileMiddleware);
// app.use(serveStatic(path.join(__dirname, 'dist')));
app.use(history({
  disableDotRule: true,
  verbose: true,
  logger: console.log.bind(console)
}));

app.get('/', function (req, res) {
  res.render(path.join(__dirname + '/dist/index.html'));
});

// view engine setup
app.set('views', path.join(__dirname, 'src/views'));
// app.set('view engine', 'pug');

// app.use(staticFileMiddleware);


const port = process.env.PORT || 80;
app.listen(port);