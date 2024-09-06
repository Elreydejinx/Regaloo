 const express = require('express');
 const router = express.Router();
 const User = require('../models/User');

 // Get user profile
 router.get('/profile', async (req, res) => {
    const user = await User.findById(req.userId); // assuming userId is available in request
    res.json(user);
 });

 router.put('/profile', async (req, res) => {
    const {name, phoneNumber} = req.body;
    await User.findByIdAndUpdate(req.userId, {name, phoneNumber});
    res.send('Profile updated');
 });

 module.exports = router;