/* jshint esversion: 8 */
import mongoose from 'mongoose';

const { Schema } = mongoose;

const cars = new Schema({
  dealer_id: {
    type: Number,
    required: true
  },
  make: {
    type: String,
    required: true
  },
  model: {
    type: String,
    required: true
  },
  bodyType: {
    type: String,
    required: true
  },
  year: {
    type: Number,
    required: true
  },
  mileage: {
    type: Number,
    required: true
  }
});

export default mongoose.model('cars', cars);