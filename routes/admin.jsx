const express = require('express');
const router = express.Router();
const Gift = require('../models/Gift');

// add new gift
router.post('/add-gift', async (req, res) => {
    const {name, price, description} = req.body;
    const gift = new Gift({name, price, description});
    await gift.save();
    res.status(201).send('Gift added');
});

//update gift details
router.put('/update-gift/:id', async (req, res) => {
    const {name, price, description} = req.body;
    await Gift.findByIdAndUpdate(req.params.id, {name, price, description});
    res.send('Gift updated');
});

//delete a gift
router.delete('/delete-gift/:id', async(req, res) =>{
    await Gift.findByIdAndDelete(req.params.id);
    res.send('Gift deleted');
});

module.exports = router;

