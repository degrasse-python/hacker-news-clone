const express = require('express')
const history = require('connect-history-api-fallback')
const path = require('path')
const serveStatic = require("serve-static")

//const staticFileMiddleware = express.static(path.join(__dirname + '/dist'));

// start express server
app = express()
app.use(serveStatic(path.join(__dirname, '/dist')))
app.use(history({
  disableDotRule: true,
  verbose: true,
  logger: console.log.bind(console)
}))

//app.use(staticFileMiddleware);

// view engine setup
//app.set('views', path.join(__dirname, 'src/views'))
// app.set('view engine', 'pug');

// app.use(staticFileMiddleware);

var port = process.env.PORT || 8000
app.listen(port, () => {
  console.log('Server listening')
})