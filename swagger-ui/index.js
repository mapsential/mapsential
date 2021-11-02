const express = require('express');
const app = express();
const swaggerUi = require('swagger-ui-express');

var options = {
    swaggerOptions: {
        url: 'http://127.0.0.1:8000/api-docs-plain'
    }
}

app.use('/', swaggerUi.serve, swaggerUi.setup(null, options));

app.listen(8120)