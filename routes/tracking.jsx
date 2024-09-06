const express = require('express');
const router = express.Router();
const Tracking = require('../models/Tracking');

// update gift status

router.post('/update-tracking', async (req,res) => {
    const {giftId, status} = req.body;
    const tracking = new Tracking({ giftId, status});
    await tracking.save();
    res.send('Tracking updated');
});

// gift tracking

router.get('/tracking/:giftId', async (req,res) => {
    const tracking = await Tracking.find({giftId: req.params.giftId}).sort({ updatedAt: -1});
    res.json(tracking);
});


module.exports = router;