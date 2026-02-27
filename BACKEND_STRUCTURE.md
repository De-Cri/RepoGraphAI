# Backend Structure Proposal

```text
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
      auth.middleware.js
      validation.middleware.js
      error.middleware.js
    utils/
      db.js
      logger.js
  config/
    default.js
    production.js
  package.json
```

## Technical Notes

- AI calls live in `services/ai/` so controllers stay thin and provider-specific logic is isolated.
- The scoring engine lives in `services/scoring/scoringEngine.js` and applies rubric-based weights for clarity/completeness/accuracy.
- Exam session flow lives in `controllers/exam.controller.js` + `services/progress/progressTracker.js` for session lifecycle and metrics.
- DB logic lives in `models/` with shared connection helpers in `utils/db.js`.
- Frontend calls backend via REST API endpoints exposed by `routes/*.routes.js` (e.g. `/api/exams`, `/api/users`) using `fetch` from `frontend/js/study.js`.
