const express = require('express');
const router = express.Router();
const Gift = require('../models/Gift');
const User = require('../models/User');

// total gifts sent 
router.get('/analytics/total-gifts', async (req, res) =>{
    const totalGifts = await Gift.countDocuments();
    res.json({totalGifts});
});

// total users
router.get('/analytics/total-users', async (req, res) => {
    const totalUsers = await User.countDocuments();
    res.json({totalUsers});
});

module.exports = router;