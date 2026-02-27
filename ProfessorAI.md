You are a senior full-stack engineer and product designer.

Generate a frontend prototype for a web application called:

"OralAI – AI Oral Exam Coach"

The design must combine:
- The bold dark hero aesthetic inspired by Redis.com
- The minimal, clean, premium feel inspired by Apple.com
- Modern AI SaaS design principles
- Strong typography hierarchy
- Large spacing
- Clean, not cluttered
- Professional startup quality

Use:
- Pure HTML
- Pure CSS
- Vanilla JavaScript
- Google Font: Inter
- No frameworks
- Fully responsive

==================================================
PROJECT STRUCTURE (MULTI-PAGE)
==================================================

Generate this folder structure:

root/
  frontend/
    index.html          (Landing page)
    study.html          (Main study app)
    css/
      styles.css
    js/
      main.js
      study.js
    assets/

All pages must share styles.css.
JavaScript must be separated logically.

==================================================
PAGE 1 — LANDING (index.html)
==================================================

Sections:

1) Navbar (fixed, glass blur)
   - Logo: OralAI
   - Links: How it Works | Features | Login
   - CTA button: "Start Studying"
   - CTA must link to study.html

2) Hero
   Large bold headline:
   "YOUR EXAM IS ABOUT TO GET EASIER"
   Subheadline:
   "Train for real oral exams with AI scoring and adaptive feedback."
   Two buttons:
      - Start Free Simulation (links to study.html)
      - Learn More (scroll)

   Dark background (#0f172a)
   Subtle gradient glow

3) How It Works (3 columns)
   - Choose Subject
   - Explain the Topic
   - Get AI Feedback

4) Features
   - Structured scoring
   - Adaptive follow-up questions
   - Progress tracking
   - Multi-level evaluation

5) Footer (minimal dark)

==================================================
PAGE 2 — STUDY PAGE (study.html)
==================================================

This is the real application interface.

Layout:

Left Sidebar:
   - Logo
   - Navigation:
       Dashboard
       New Simulation
       History
       Settings
   - Minimal vertical layout
   - Soft dark background

Main Content Area:

TOP SECTION — Simulation Setup
   - Dropdown: Level (High School / University)
   - Dropdown: Subject (Math, Physics, History, etc.)
   - Input: Topic
   - Button: "Start Simulation"

EXPOSURE SECTION
   - Large textarea
   - Character counter
   - Timer simulation (start when typing)
   - Submit button

When user clicks submit:
   - Show animated loading state
   - After 2 seconds display:

EVALUATION PANEL
   - Score card (big bold score 24/30)
   - Breakdown:
        Clarity: 8/10
        Completeness: 7/10
        Accuracy: 9/10
   - Strengths list
   - Weaknesses list
   - Follow-up questions

PROGRESS SECTION
   - Simple stat cards:
        Exams Taken
        Average Score
        Best Subject
   - Minimal Apple-style cards

Use Vanilla JS to:
   - Handle navigation tab switching (Dashboard / Simulation / History)
   - Simulate loading
   - Dynamically insert evaluation results
   - Update character counter

==================================================
DESIGN RULES
==================================================

- Primary background: #0f172a
- Light sections: #f8fafc
- Accent red inspired by Redis (#dc2626 softened)
- Rounded corners (16px+)
- Soft shadows
- Smooth hover transitions
- Clean animations
- No clutter
- Premium SaaS look

Typography:
- Very large bold hero text
- Clear section separation
- Generous padding (100px sections landing)
- 24px+ spacing rhythm

==================================================
PART 3 — FUTURE BACKEND STRUCTURE
==================================================

After generating frontend code, also generate recommended backend structure:

backend/
  src/
    server.js
    routes/
      exam.routes.js
      user.routes.js
    controllers/
      exam.controller.js
      user.controller.js
    services/
      ai/
        evaluation.service.js
        questionGenerator.service.js
      scoring/
        scoringEngine.js
      progress/
        progressTracker.js
    models/
      user.model.js
      exam.model.js
      attempt.model.js
    middlewares/
    utils/
  config/
  package.json

Explain briefly:
- Where AI calls will live
- Where scoring engine lives
- Where exam session logic lives
- Where DB logic lives
- How frontend will call backend (REST API)

==================================================
GOAL
==================================================

This must feel like:
- A real SaaS product
- Clean and modern
- Production-ready structure
- Not a school demo

Generate:
1) All frontend files
2) Folder structure
3) Short technical explanation