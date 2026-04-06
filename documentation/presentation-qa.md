# Topiq Presentation Questions And Answers

## 1. What is this project?

Topiq is a smart study resource recommendation system for university students. It helps students quickly find useful video and reading materials for academic topics.

## 2. What problem does it solve?

Students usually search in many places like YouTube, blogs, and PDFs. That takes time and often gives too many poor-quality results. Topiq brings these resources into one system and ranks them.

## 3. Who are the target users?

University students, especially computer science and engineering students.

## 4. Which framework did you use?

I used Django for the backend and server-side rendering.

## 5. Which database did you use?

SQLite for local development and project demonstration.

## 6. Is this an ML project?

Yes, but it uses lightweight machine learning. The project uses TF-IDF and cosine similarity to match user queries with academic topics, then uses a weighted score to rank resources.

## 7. How does the search work?

The system cleans the query, compares it with topic names, tags, keywords, and descriptions, then finds the closest matching topic and returns its top resources.

## 8. What is TF-IDF?

TF-IDF stands for Term Frequency-Inverse Document Frequency. It gives importance to meaningful words in a query and compares them with stored topic text.

## 9. Why did you use TF-IDF?

It is fast, simple, explainable, and suitable for a university project where topic matching is based on text similarity.

## 10. How are resources ranked?

They are ranked by an `ml_score` based on rating, view count, and student feedback.

## 11. What do you mean by feedback-based improvement?

When students click helpful or not helpful, the system stores that interaction and updates the recommendation score. So better resources can move higher over time.

## 12. Did you train a neural network model?

No. This project does not train a deep learning model. It uses text matching and score-based ranking. The database is seeded with structured data, and ranking improves through feedback.

## 13. How do you train or prepare the data?

I use a Django management command called `seed_data` to populate semesters, subjects, topics, videos, and reading materials. Then the system calculates ranking scores.

## 14. Why did you choose SQLite?

SQLite is simple, lightweight, and enough for development and academic demonstration. It also reduces setup complexity.

## 15. What are the main models?

- Semester
- Subject
- Topic
- VideoResource
- ReadingResource
- StudentInteraction

## 16. What is the role of StudentInteraction?

It stores helpful, not helpful, bookmark, and view-type actions from users.

## 17. Why did you include an AI chat feature?

It gives students a quick academic explanation of a concept without leaving the platform.

## 18. Which API is used for AI chat?

Anthropic Claude API.

## 19. What happens if the API key is missing?

The AI chat returns a safe fallback message, but the main recommendation system still works.

## 20. What are the strengths of your project?

- Easy to use
- Fast topic search
- Clear academic focus
- Feedback-based ranking
- Organized subject and semester structure

## 21. What are the limitations?

- Seeded resources are demo data
- SQLite is not ideal for large production deployment
- AI chat depends on an external API key
- There is no user login system yet

## 22. What can be improved in the future?

- Real YouTube and article ingestion pipeline
- User accounts
- Personalized recommendations
- PostgreSQL deployment
- Analytics dashboard
- Better admin moderation tools

## 23. Why is this project useful academically?

It combines web development, database design, information retrieval, ranking logic, and optional AI assistance in one real educational use case.

## 24. If sir asks "where is the machine learning part?", what should I say?

The machine learning part is in topic matching and ranking. TF-IDF and cosine similarity are used to find the closest topic, and a scoring model ranks resources based on quality indicators and feedback.

## 25. If sir asks "is the project fully production ready?", what should I say?

I would say it is ready as an academic project and local demo application, but not fully production ready yet. For production, it still needs deployment hardening, real content ingestion, stronger security review, and scalable database setup.
