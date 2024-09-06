const express = require('express');
const router = express.Router();
const Stripe = require('stripe');
const stripe = Stripe('STRIPE_SECRET_KEY');


router.post('/refund', async (req, res) => {
    const {chargeId, amount} = req.body;
    try{
        const refund = await stripe.refund.create({charge: chargeId, amount});
        res.json(refund);
    }catch (error) {
        res.status(500).send('Refund failed');
    }
});

module.exports = router;