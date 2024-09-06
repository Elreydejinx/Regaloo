const express = require('express');
const router = express.Router();
const User = require('../models/User');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');


// register
router.post('register', async (req, res) => {
    const {email, password} = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({email, password: hashedPassword});
    await user.save();
    res.status(201).send(' User registered');
});

// login
router.post('/login', async (req, res) => {
    const {email, password} = req.body;
    const user = await User.findOne({email});
    if (User && await bcrypt.compare(password, user.password)) {
        const token = jwt.sign({userId: user._id}, 'SECRET_KEY');
        res.json({token});
    }else {
        res.status(400).send('Invalid credentails');
    }
});

module.exports = router;
