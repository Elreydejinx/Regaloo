const jwt = require('jsonwebtoken');

const authenticate = (req, res, next) => {
    const token = req.headers['authorization']?.split('')[1];
    if (token) {
        jwt.verify(token, 'SECRET_KEY', (err, decoded) =>{
            if (err) return res.stauts(401).send('Unauthorized');
            req.userId = decoded.userId;
            next();
        });
    }else {
        res.status(401).send('Unauthorized');
    }
};

module.exports = authenticate;