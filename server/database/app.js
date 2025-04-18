
/* jshint esversion: 8 */
import express from 'express';
import mongoose from 'mongoose';
import fs from 'fs';
import cors from 'cors';
import Reviews from './review.js';
import Dealerships from './dealership.js';

const app = express();
const port = 3030;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Load initial data
const reviewsData = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealershipsData = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Database connection
mongoose.connect("mongodb://mongo_db:27017/dealershipsDB", {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log("Connected to MongoDB");
  initializeData();
})
.catch(err => {
  console.error("MongoDB connection error:", err);
});

async function initializeData() {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);
    
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);
    
    console.log("Database initialized with sample data");
  } catch (error) {
    console.error("Error initializing data:", error);
  }
}

// Routes
app.get('/', (_req, res) => {
  res.send("Welcome to the Mongoose API");
});

app.get('/fetchReviews', async (_req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

app.get('/fetchDealers', async (_req, res) => {
  try {
    const dealers = await Dealerships.find();
    res.json(dealers);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching dealers' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const dealers = await Dealerships.find({ state: req.params.state });
    res.json(dealers);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching dealers by state' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealer = await Dealerships.findOne({ id: req.params.id });
    if (!dealer) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json(dealer);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body;
    const lastReview = await Reviews.findOne().sort({ id: -1 });
    const newId = lastReview ? lastReview.id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.status(201).json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});