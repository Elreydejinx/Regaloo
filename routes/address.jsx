const express = require('express');
const router = express.Router();
const Address = require('../models/Address');

// add or update address
router.post('/address', async(req, res) => {
    const {userId, address} = req.body;
    await Address.findByIdAndUpdate({userId}, address, {upsert: true});
    res.send('Address saved');
});

// get address
router.get('/address/:userId', async(req,res) => {
    const address = await Address.findOne({userId: req.params.userId});
    res.json(address);
});


module.exports = router;