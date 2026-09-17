# Smart Plant Coach 🌿

## Overview

Smart Plant Coach is an AI-powered CLI application that helps users take care of their plants.

The user enters:
- Plant name
- Indoor or Outdoor
- Current weather

The application uses AI to generate a simple care plan that includes:
- Watering frequency
- Light recommendation
- Care tip

Python then saves the plant information, manages watering dates, calculates the next watering schedule, and updates the Garden Mood.

---

## User Stories

- As a user, I want to add a plant so I can save its care information.
- As a user, I want to receive an AI-generated care plan for my plant.
- As a user, I want to view all my saved plants.
- As a user, I want to see the care details for a specific plant.
- As a user, I want to mark a plant as watered so the schedule can be updated.
- As a user, I want to see the next watering date for each plant.
- As a user, I want to update a plant if its location or weather conditions change.
- As a user, I want to see the Garden Mood so I can quickly understand the overall condition of my plants.

---

## Usage

### 1. Install the required packages

Before running the project, install the required packages:

```bash
pip install -r requirements.txt
