// High-fidelity fallback and demo data for WORLD TRAVELHOLIC 🌍

export const MOCK_POPULAR_DESTINATIONS = [
  {
    name: "Jaipur, Rajasthan, India",
    vibe: "Royal Forts, Palaces & Vibrant Bazaars",
    country: "India",
    countryCode: "IN",
    avgBudget: 4200,
    bestSeason: "Oct - Mar",
    image: "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop&q=80",
    tags: ["Heritage", "Culture", "Photography", "Family"]
  },
  {
    name: "Paris, France",
    vibe: "Artistic Architecture, Romantic Lights & Haute Cuisine",
    country: "France",
    countryCode: "FR",
    avgBudget: 18000,
    bestSeason: "Apr - Oct",
    image: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&auto=format&fit=crop&q=80",
    tags: ["Honeymoon", "Art", "Fine Dining", "Luxury"]
  },
  {
    name: "Tokyo, Japan",
    vibe: "Cyberpunk Skylines, Shinto Shrines & Michelin Ramen",
    country: "Japan",
    countryCode: "JP",
    avgBudget: 15000,
    bestSeason: "Mar - May, Oct - Nov",
    image: "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800&auto=format&fit=crop&q=80",
    tags: ["Culture", "Culinary", "Solo", "Adventure"]
  },
  {
    name: "Udaipur, Rajasthan, India",
    vibe: "Romantic Lakes, Palaces & Sunset Boat Cruises",
    country: "India",
    countryCode: "IN",
    avgBudget: 5200,
    bestSeason: "Sep - Mar",
    image: "https://images.unsplash.com/photo-1615836245337-f5b9b2303f10?w=800&auto=format&fit=crop&q=80",
    tags: ["Honeymoon", "Heritage", "Romantic", "Luxury"]
  },
  {
    name: "Dubai, UAE",
    vibe: "Futuristic Architecture & Desert Safaris",
    country: "UAE",
    countryCode: "AE",
    avgBudget: 16000,
    bestSeason: "Nov - Apr",
    image: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&auto=format&fit=crop&q=80",
    tags: ["Luxury", "Family", "Shopping", "Adventure"]
  },
  {
    name: "Bali, Indonesia",
    vibe: "Emerald Rice Terraces, Hindu Water Temples & Surfing",
    country: "Indonesia",
    countryCode: "ID",
    avgBudget: 7500,
    bestSeason: "Apr - Oct",
    image: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&auto=format&fit=crop&q=80",
    tags: ["Beach", "Nature", "Relaxation", "Honeymoon"]
  },
  {
    name: "Interlaken, Switzerland",
    vibe: "Alpine Glacier Peaks & Turquoise Lakes",
    country: "Switzerland",
    countryCode: "CH",
    avgBudget: 24000,
    bestSeason: "Year-round",
    image: "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?w=800&auto=format&fit=crop&q=80",
    tags: ["Mountain", "Adventure", "Scenic Trains", "Luxury"]
  },
  {
    name: "Goa, India",
    vibe: "Sun-Kissed Beaches, Portuguese Forts & Seafood",
    country: "India",
    countryCode: "IN",
    avgBudget: 4800,
    bestSeason: "Nov - Apr",
    image: "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop&q=80",
    tags: ["Beach", "Relaxation", "Nightlife", "Friends"]
  }
];

export const MOCK_GUIDES = [
  {
    id: "g1",
    name: "Mahipal Singh Rathore",
    avatarUrl: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
    city: "Jaipur",
    country: "India",
    experienceYears: 12,
    languages: ["English", "Hindi", "German"],
    hourlyRate: 850,
    currency: "INR",
    services: ["Amber Forts & Palaces", "Royal Rajput Dynasty Stories", "Textile & Gem Bazaar Walk"],
    rating: 4.98,
    reviewsCount: 142,
    verified: true,
    bio: "Certified Rajasthan tourism guide with a lineage of royal storytellers. Unlocks private areas and photo vantage points."
  },
  {
    id: "g2",
    name: "Aarav Sharma",
    avatarUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
    city: "New Delhi",
    country: "India",
    experienceYears: 8,
    languages: ["English", "Hindi", "French"],
    hourlyRate: 750,
    currency: "INR",
    services: ["Old Delhi Food Safari", "Mughal Architecture Walk", "Photography Assist"],
    rating: 4.96,
    reviewsCount: 84,
    verified: true,
    bio: "Certified Delhi Tourism guide with a master's in Medieval Indian History. Passionate about uncovering Old Delhi secrets."
  },
  {
    id: "g3",
    name: "Jean-Pierre Laurent",
    avatarUrl: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
    city: "Paris",
    country: "France",
    experienceYears: 10,
    languages: ["English", "French", "Spanish"],
    hourlyRate: 3200,
    currency: "INR",
    services: ["Louvre Masterpieces", "Montmartre Secret Walk", "Wine & Cheese Tasting"],
    rating: 4.95,
    reviewsCount: 112,
    verified: true,
    bio: "Art Historian and licensed national museum curator in Paris."
  },
  {
    id: "g4",
    name: "Kenji Sato",
    avatarUrl: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    city: "Tokyo",
    country: "Japan",
    experienceYears: 9,
    languages: ["English", "Japanese"],
    hourlyRate: 2800,
    currency: "INR",
    services: ["Asakusa & Shinto Rituals", "Akihabara Tech Safari", "Tsukiji Outer Market Food Tour"],
    rating: 4.99,
    reviewsCount: 96,
    verified: true,
    bio: "Tokyo native with deep love for Edo culture and the underground culinary scene."
  }
];

export const MOCK_EXPERIENCES = [
  {
    id: "e1",
    guideId: "g1",
    title: "Jaipur Royal Hand-Block Printing & Blue Pottery Workshop",
    category: "Craft & Workshop",
    city: "Jaipur",
    durationHours: 3.0,
    pricePerPerson: 1200,
    currency: "INR",
    rating: 4.95,
    description: "Learn 300-year-old natural dye block printing from master artisans and print your own custom silk scarf to take home.",
    imageUrl: "https://images.unsplash.com/photo-1606293926075-69a00dbfde81?w=600&auto=format&fit=crop&q=80"
  },
  {
    id: "e2",
    guideId: "g2",
    title: "Old Delhi 4-Hour Sunset Street Food & Spice Safari",
    category: "Culinary Tour",
    city: "New Delhi",
    durationHours: 4.0,
    pricePerPerson: 1499,
    currency: "INR",
    rating: 4.98,
    description: "Taste 12+ iconic delicacies including stuffed paranthas, slow-cooked kebabs, Daulat ki Chaat, and vintage Jalebis with safety-checked hygienic vendors.",
    imageUrl: "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=600&auto=format&fit=crop&q=80"
  },
  {
    id: "e3",
    guideId: "g3",
    title: "Montmartre Bohemian Artists & Pastry Stroll",
    category: "Walking Tour",
    city: "Paris",
    durationHours: 3.0,
    pricePerPerson: 4800,
    currency: "INR",
    rating: 4.94,
    description: "Walk the cobblestone paths where Picasso and Van Gogh painted, ending with warm artisanal croissants and macaron tastings.",
    imageUrl: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80"
  }
];

export const MOCK_REVIEWS = [
  {
    author: "Dr. Vikram & Priya Malhotra",
    trip: "Family Trip to Jaipur, Rajasthan",
    rating: 5,
    date: "2 weeks ago",
    comment: "The 15-agent debate engine was mind-blowing! When the Risk Agent flagged our tight commute and moved our Amber Fort climb to 08:30 AM, it saved us from the afternoon heat. Everything was realistically timed!"
  },
  {
    author: "Sarah Jenkins & Friends",
    trip: "Friends Cultural Trip to Paris, France",
    rating: 5,
    date: "Last month",
    comment: "Group conflict resolver saved us. Two of us wanted art galleries while two wanted vintage bakery trails. The itinerary balanced both seamlessly without exhausting anyone!"
  },
  {
    author: "Amitabh Sen",
    trip: "Solo Explorer in Tokyo, Japan",
    rating: 5,
    date: "3 weeks ago",
    comment: "The Live Trip Recovery mode saved my trip when my Shinkansen train was delayed by heavy rain. It rearranged the whole evening in under 3 seconds."
  }
];
