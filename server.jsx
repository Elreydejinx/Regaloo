const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const i18n = require('./i18n');
const rateLimiter = require('./middleware/rateLimiter');
const authenticate = require('./middleware/auth');

const app = express();
app.use(bodyParser.json());
app.use(i18n.init);
app.use(rateLimiter);

mongoose.connect('mongodb://localhost/regaloo', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

const config = require('./config');

mongoose.connect(config.datebase.uri, {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

// Routes
app.use('/admin', authenticate, require('./routes/admin'));
app.use('/profile', authenticate, require('./routes/profile'));
app.use('/address', authenticate, require('./routes/address'));
app.use('/tracking', authenticate, require('./routes/tracking'));
app.use('/refunds', authenticate, require('./routes/refunds'));
app.use('/analytics', authenticate, require('./routes/analytics'));
app.use('/auth', require('./routes/auth'));
app.use('/gifts', authenticate, require('./routes/gift'));

// Start server
app.listen(3000, () => {
    console.log('Server running on port 3000');
});
