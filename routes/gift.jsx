const express = require('express');
const router = express.Router();
const Gift = require('../models/Gift');

// Add a new gift
router.post('/add-gift', async (req, res) => {
    try {
        const { name, price, description } = req.body;
        if (!name || !price || !description) {
            return res.status(400).send('Name, price, and description are required');
        }
        const gift = new Gift({ name, price, description });
        await gift.save();
        res.status(201).send('Gift added successfully');
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

// Get all gifts
router.get('/gifts', async (req, res) => {
    try {
        const gifts = await Gift.find();
        res.json(gifts);
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

// Get a single gift by ID
router.get('/gift/:id', async (req, res) => {
    try {
        const gift = await Gift.findById(req.params.id);
        if (!gift) {
            return res.status(404).send('Gift not found');
        }
        res.json(gift);
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

// Update a gift by ID
router.put('/update-gift/:id', async (req, res) => {
    try {
        const { name, price, description } = req.body;
        const gift = await Gift.findByIdAndUpdate(req.params.id, { name, price, description }, { new: true });
        if (!gift) {
            return res.status(404).send('Gift not found');
        }
        res.json(gift);
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

// Delete a gift by ID
router.delete('/delete-gift/:id', async (req, res) => {
    try {
        const gift = await Gift.findByIdAndDelete(req.params.id);
        if (!gift) {
            return res.status(404).send('Gift not found');
        }
        res.send('Gift deleted successfully');
    } catch (error) {
        console.error(error);
        res.status(500).send('Server error');
    }
});

module.exports = router;
