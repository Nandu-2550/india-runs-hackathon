# India Runs by Redrob AI Hackathon (Track 1 – Data & AI Challenge)

## Problem Statement
The objective of this challenge is to rank and select the top 100 candidates from a dataset of 100,000 profiles for a Senior AI Engineer position at Redrob AI. The goal is to accurately evaluate candidates based on their technical skills, career trajectory, behavioral signals, and overall fit for the company's budget and location preferences, while successfully identifying and filtering out synthetic (honeypot) profiles.

## Scoring Approach
The scoring system assigns a final score (normalized to 0-1) to each candidate using 8 weighted components:
1. **Skill Match Score (20%)**: Evaluates proficiency and experience in must-have (e.g., embeddings, RAG, Pinecone, LLMs) and nice-to-have AI/ML skills, with bonuses for long-duration experience and endorsements.
2. **Career History Score (25%)**: Searches for specific AI-related keywords across career descriptions, evaluates title relevance, prefers product company experience over purely consulting backgrounds, and rewards optimal years of experience (5-9 years).
3. **Behavioral & Platform Signals Score (20%)**: Measures candidate activity (days since active, open to work), recruiter responsiveness, notice period, and GitHub/profile completeness to ensure high engagement probability.
4. **Education Score (10%)**: Favors relevant fields of study (CS, AI/ML), top-tier institutions, and advanced degrees.
5. **Certifications Score (5%)**: Awards points for high-value certifications (AWS, GCP, DeepLearning.AI, HuggingFace).
6. **Location & Availability Score (10%)**: Strongly prefers candidates currently in India or willing to relocate.
7. **Salary Fit Score (5%)**: Evaluates the overlap between the candidate's expected salary range and the company's budget (25-55 LPA).
8. **Profile Trust Score (5%)**: Factors in verified contact information, connected LinkedIn accounts, and overall network size.

## Honeypot Detection Strategy
Honeypots were meticulously eliminated by checking for unrealistic scenarios, such as claiming "expert" proficiency with 0 months of experience, having over 15 years of experience but less than 5 years combined job duration, single roles lasting over 16 years, contradictory low assessment scores despite "expert" claims, or mathematically impossible engagement statistics (e.g., offer acceptance > 100%).

## Key Insights
A strong candidate for this role is one who not only has the requisite modern AI stack skills (RAG, LLMs, Vector DBs) but has applied them in product-centric environments with tangible outcomes. Timely availability and strong behavioral signals further distinguish the truly viable hires from passive profiles.

## Tech Stack
- **Python**: Core logic execution
- **Pandas**: Final data framing and CSV generation
- **Tqdm**: Progress visualization for streaming 100k lines
