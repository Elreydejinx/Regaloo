const mongoose = require('mongoose');

const giftSchema = new mongoose.Schema({
    name: {type: String, reuired: true},
    price: {type: Number, required: true},
    description: {type: String, required: true}
});

module.exports = mongoose.model('Gift', giftSchema);