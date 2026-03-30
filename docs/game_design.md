# 🎮 Game Design Document (GDD) - TubeRPG

## 1. The Core Theme & Identity
- **Theme:** Classic Fantasy RPG (Dungeons, Knights, Magic).
- **The Concept:** A learning path (playlist) is an epic quest. The student is a hero fighting through dungeons to defeat monsters (knowledge gaps).

## 2. The Gamified User Journey (Step-by-Step Flow)

### Step 1: The Gates (Authentication)
- Mandatory Login/Signup to track progress, HP, and unlocked nodes.

### Step 2: The Hero's Calling (Path/Class Selection)
- The user selects a **Character Class** (Learning Path).
- *Examples:* The Dark Knight of Backend, The Warlock of DevOps.

### Step 3: The World Map & Lore (Pre-Level Screen)
- **Static World Map** with interconnected nodes (YouTube videos).
- **The Hook (AI Lore):** Pokemon-style dialog box. Gemini generates lore dynamically based on the video's transcript. 

### Step 4: The Dungeon (Video & Battle Dynamics)
- The user watches the video.
- **The Popup Battle:** The engagement loop triggers Multiple-Choice Questions based strictly on the video content.
- **Skipping Battles:** Battles *can* be skipped, but at a cost. "Fleeing" a battle costs HP or "Gold Coins" to prevent users from spamming the skip button.
- Correct answers attack the Enemy. Wrong answers damage the Player.
- **Node Clear:** Defeating the enemy unlocks the next node on the World Map.

## 3. End-Game & Rewards
- **Path Completion:** Finishing a full Path triggers a Final Boss Fight (an AI-generated exam evaluating the entire playlist).
- **Certificates:** Upon victory, the system generates a downloadable Digital Certificate.
- *Creator Integration:* Official partner creators (like Brais) can digitally sign these certificates, turning a "YouTube playlist" into a resume-worthy asset.

## 4. Business Model & Monetization (CEO Strategy)
*Why pay if YouTube is free? Because users pay for structure, validation, and dopamine (gamification).*
1. **B2C Freemium (The "Duolingo" Model):**
   - *Free Tier:* Users have a limited HP/Stamina bar. If they fail too many questions, they "die" and must wait 12 hours to recharge (or watch an Ad).
   - *Pro Tier ($5/mo):* Unlimited HP, no Ads, access to detailed AI explanations for wrong answers, and exclusive cosmetics.
2. **Creator Revenue Share (B2B2C):**
   - Creators upload "Premium Paths". Users buy the path or subscribe. We keep 30% of the revenue for providing the Gamified Platform and AI infrastructure.

## 5. Visual Identity & UI/UX (Frontend Art Style)
- **Art Direction:** 16-bit / 32-bit Pixel Art (similar to *Habitica* or *Stardew Valley*).
- *Reasoning for Solo-Dev:* Cost-effective and extremely fast to develop. Animations (like breathing) require only 2-3 frames, keeping React components lightweight. It perfectly glues with the "GameBoy Dialog" aesthetic proposed for the World Map.
- **Initial Character MVP:** The Dark Knight (representing the Backend Path).
- **Future Roster:** The DevOps Warlock, The Frontend Ranger, The Data Oracle.
- **UI Framework Concept:** React paired with a Retro/Pixel CSS library (like NES.css) or a custom Tailwind config optimized for blocky, gamified aesthetics (thick borders, pixel fonts).
