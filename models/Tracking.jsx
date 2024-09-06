const mongoose = require('mongoose');

const trackingSchema = new mongoose.Schema({
    giftId: {type: mongoose.Schema.Types.ObjectId, ref: 'Gift', required: true},
    status: {type: String, required: true}, // 'sent', 'Delivered'
    updatedAt: {type: Date, default: Date.now}
});

module.exports = mongoose.model('Tracking', trackingSchema);