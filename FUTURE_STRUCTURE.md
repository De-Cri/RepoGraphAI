# OralAI Future Full-Stack Structure

```text
root/
  frontend/
    index.html
    css/
      base.css
      components.css
      pages.css
    js/
      app.js
      api.js
      simulation.js
      ui/
        navbar.js
        demo.js
        stats.js
    assets/
      images/
      icons/
      fonts/
  backend/
    src/
      server.js
      app.js
      routes/
        health.routes.js
        auth.routes.js
        exams.routes.js
        feedback.routes.js
      controllers/
        auth.controller.js
        exams.controller.js
        feedback.controller.js
      services/
        ai/
          promptBuilder.service.js
          llmClient.service.js
          feedbackOrchestrator.service.js
        scoring/
          rubricLoader.service.js
          scoreCalculator.service.js
          scoreNormalizer.service.js
        exams/
          examSession.service.js
          followUpQuestion.service.js
      models/
        user.model.js
        examSession.model.js
        response.model.js
        feedback.model.js
      middlewares/
        auth.middleware.js
        validation.middleware.js
        error.middleware.js
      utils/
        logger.js
        env.js
        db.js
    config/
      default.js
      production.js
    package.json
  database/
    schema.sql
    migrations/
      001_init.sql
      002_exam_tables.sql
  .env.example
  README.md
```

## Responsibilities

- `frontend/`: Static client app, UI behavior, and API calls to backend endpoints.
- `backend/src/services/ai/`: AI orchestration logic (prompt construction, LLM provider calls, response shaping).
- `backend/src/services/scoring/`: Scoring engine logic (rubrics, weighted evaluation, normalization).
- `backend/src/services/exams/`: Exam session flow (start session, track attempts, generate follow-up questions).
- `backend/src/models/` + `backend/src/utils/db.js`: Database access layer and query execution boundaries.
- `backend/src/controllers/` + `routes/`: HTTP boundary that validates input, invokes services, and formats API responses.
