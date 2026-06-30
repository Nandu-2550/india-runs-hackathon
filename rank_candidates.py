import json
import pandas as pd
from tqdm import tqdm
from datetime import date

def load_and_score():
    MUST_HAVE_SKILLS = [
        "embedding", "embeddings", "vector database", "pinecone", "weaviate", 
        "milvus", "faiss", "qdrant", "elasticsearch", "rag", "retrieval", 
        "langchain", "llamaindex", "llm", "gpt", "claude", "gemini", "llama",
        "python", "ndcg", "mrr", "ranking", "semantic search"
    ]
    NICE_TO_HAVE_SKILLS = [
        "fine-tuning", "lora", "qlora", "peft", "mlflow", "weights & biases",
        "fastapi", "bentoml", "triton", "pytorch", "transformers", "huggingface",
        "kubernetes", "docker", "aws", "gcp", "azure", "prompt engineering",
        "recommendation", "nlp", "bert", "openai"
    ]
    CAREER_KEYWORDS = [
        "embedding", "vector", "retrieval", "rag", "ranking", "search",
        "llm", "fine-tun", "production", "deployed", "shipped", "at scale",
        "pipeline", "transformer", "ndcg", "mrr", "a/b test", "recommendation",
        "semantic", "pinecone", "faiss", "weaviate", "langchain", "openai",
        "real users", "latency", "throughput", "inference", "model serving"
    ]
    STRONG_TITLES = ["ai engineer", "ml engineer", "machine learning", "nlp engineer", 
                     "search engineer", "recommendation", "data scientist", "llm engineer",
                     "applied scientist", "research engineer", "ai researcher"]
    WEAK_TITLES = ["software engineer", "backend engineer", "data engineer", "full stack"]
    IRRELEVANT_TITLES = ["sales", "marketing", "hr manager", "accountant", "mechanical",
                         "civil engineer", "operations", "customer support", "graphic designer"]
    CONSULTING_FIRMS = ["tcs", "wipro", "infosys", "cognizant", "accenture", "hcl", 
                        "capgemini", "mphasis", "tech mahindra", "hexaware", "mindtree",
                        "ltimindtree", "persistent", "dunder mifflin"]
    PRODUCT_COMPANY_INDUSTRIES = ["software", "saas", "fintech", "edtech", "healthtech",
                                   "e-commerce", "ai", "machine learning", "food delivery",
                                   "technology", "internet"]
    RELEVANT_FIELDS = ["computer science", "artificial intelligence", "machine learning",
                       "data science", "information technology", "electronics", 
                       "mathematics", "statistics", "computational"]
    NEUTRAL_FIELDS = ["engineering", "physics", "information systems"]
    HIGH_VALUE_CERTS = [
        "aws certified", "gcp", "google cloud", "azure", "deeplearning.ai",
        "huggingface", "tensorflow", "pytorch", "coursera", "fast.ai",
        "databricks", "mlops", "langchain", "openai"
    ]
    MEDIUM_VALUE_CERTS = [
        "scrum", "agile", "pmp", "six sigma"
    ]

    today = date(2026, 6, 28)
    
    candidates = []
    honeypots_removed = 0
    total_processed = 0
    
    input_file = r'C:\Projects\H2S_India_Run\candidates.jsonl'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc="Processing Candidates"):
            if not line.strip(): continue
            total_processed += 1
            cand = json.loads(line)
            
            cand_id = cand.get('candidate_id', '')
            profile = cand.get('profile', {})
            career_history = cand.get('career_history', [])
            education = cand.get('education', [])
            skills = cand.get('skills', [])
            certifications = cand.get('certifications', [])
            signals = cand.get('redrob_signals', {})
            
            is_honeypot = False
            
            for s in skills:
                if s.get('proficiency') == 'expert' and s.get('duration_months', 0) == 0:
                    is_honeypot = True
                    break
            
            yoe = profile.get('years_of_experience', 0)
            sum_duration = sum(job.get('duration_months', 0) for job in career_history)
            
            if yoe > 15 and sum_duration < 60:
                is_honeypot = True
            
            for job in career_history:
                if job.get('duration_months', 0) > 200:
                    is_honeypot = True
                    break
                    
            sas = signals.get('skill_assessment_scores', {})
            if sas:
                sas_lower = {k.lower(): v for k, v in sas.items()}
                for s in skills:
                    s_name = s.get('name', '').lower()
                    if s.get('proficiency') == 'expert':
                        if s_name in sas_lower and sas_lower[s_name] < 25:
                            is_honeypot = True
                            break
                        for k, v in sas_lower.items():
                            if s_name in k or k in s_name:
                                if v < 25:
                                    is_honeypot = True
                                    break
                    if is_honeypot: break
            
            if (signals.get('recruiter_response_rate', 0) == 1.0 and 
                signals.get('avg_response_time_hours', 100) < 0.5 and 
                signals.get('applications_submitted_30d', -1) == 0):
                is_honeypot = True
                
            if signals.get('offer_acceptance_rate', 0) > 1.0:
                is_honeypot = True
                
            if (signals.get('profile_completeness_score', 0) == 100 and
                signals.get('github_activity_score', 0) == 100 and
                signals.get('interview_completion_rate', 0) == 1.0 and
                signals.get('offer_acceptance_rate', 0) == 1.0):
                is_honeypot = True
                
            if yoe < 1 and len(career_history) > 3:
                is_honeypot = True
                
            if is_honeypot:
                honeypots_removed += 1
                continue
                
            raw_skill_score = 0
            matched_must_haves = set()
            for s in skills:
                s_name = s.get('name', '').lower()
                prof = s.get('proficiency', '').lower()
                dur = s.get('duration_months', 0)
                end = s.get('endorsements', 0)
                
                is_must = any(m in s_name for m in MUST_HAVE_SKILLS)
                is_nice = any(n in s_name for n in NICE_TO_HAVE_SKILLS)
                
                if is_must:
                    matched_must_haves.add(s.get('name'))
                    if prof == 'expert': raw_skill_score += 3
                    elif prof == 'advanced': raw_skill_score += 2
                    elif prof == 'intermediate': raw_skill_score += 1.5
                    elif prof == 'beginner': raw_skill_score += 0.5
                    
                    if dur > 12: raw_skill_score += 0.5
                    if end > 20: raw_skill_score += 0.5
                elif is_nice:
                    if prof in ['expert', 'advanced']: raw_skill_score += 1
                    elif prof == 'intermediate': raw_skill_score += 0.5
            
            for k, v in sas.items():
                k_lower = k.lower()
                is_rel = any(m in k_lower for m in MUST_HAVE_SKILLS) or any(n in k_lower for n in NICE_TO_HAVE_SKILLS)
                if is_rel:
                    if v > 75: raw_skill_score += 2
                    elif v > 50: raw_skill_score += 1
                    
            skill_score = min(raw_skill_score / 30.0, 1.0)
            
            career_score_raw = 0
            
            found_keywords = set()
            for job in career_history:
                desc = job.get('description', '').lower()
                for kw in CAREER_KEYWORDS:
                    if kw in desc:
                        found_keywords.add(kw)
            career_score_raw += min(len(found_keywords), 20)
            
            cur_title = profile.get('current_title', '').lower()
            def title_score(t):
                if any(st in t for st in STRONG_TITLES): return 'strong'
                if any(wt in t for wt in WEAK_TITLES): return 'weak'
                if any(it in t for it in IRRELEVANT_TITLES): return 'irrelevant'
                return 'neutral'
            
            c_title_cat = title_score(cur_title)
            if c_title_cat == 'strong': career_score_raw += 5
            elif c_title_cat == 'weak': career_score_raw += 1
            elif c_title_cat == 'irrelevant': career_score_raw -= 3
            
            has_past_strong = False
            for job in career_history:
                if not job.get('is_current', False):
                    if title_score(job.get('title', '').lower()) == 'strong':
                        has_past_strong = True
            if has_past_strong:
                career_score_raw += 3
                
            c_ind = profile.get('current_industry', '').lower()
            c_comp = profile.get('current_company', '').lower()
            
            def is_product(ind):
                return any(pi in ind for pi in PRODUCT_COMPANY_INDUSTRIES)
            
            if is_product(c_ind):
                career_score_raw += 4
                
            has_past_product = False
            all_consulting = True
            if not career_history:
                all_consulting = False
            
            for job in career_history:
                j_ind = job.get('industry', '').lower()
                j_comp = job.get('company', '').lower()
                
                if is_product(j_ind):
                    if not job.get('is_current', False):
                        has_past_product = True
                
                is_cons = any(cf in j_comp for cf in CONSULTING_FIRMS)
                if not is_cons:
                    all_consulting = False
                    
            if has_past_product:
                career_score_raw += 2
                
            if all_consulting:
                career_score_raw -= 5
                
            if 5 <= yoe <= 9: career_score_raw += 5
            elif 4 <= yoe <= 12: career_score_raw += 3
            elif 3 <= yoe <= 15: career_score_raw += 1
            
            industries_worked = set()
            titles_ordered = []
            for job in sorted(career_history, key=lambda x: x.get('start_date', '')):
                industries_worked.add(job.get('industry', '').lower())
                titles_ordered.append(job.get('title', '').lower())
                
            if len(industries_worked) >= 2:
                career_score_raw += 1
                
            promoted = False
            has_lower = False
            for t in titles_ordered:
                cat = title_score(t)
                if cat in ['weak', 'irrelevant', 'neutral']:
                    has_lower = True
                elif cat == 'strong' and has_lower:
                    promoted = True
                    break
            if promoted:
                career_score_raw += 2
                
            career_score = max(0, min(career_score_raw / 35.0, 1.0))
            
            beh_score = 0
            
            la_str = signals.get('last_active_date')
            if la_str:
                try:
                    la_date = date.fromisoformat(la_str[:10])
                    days_since_active = (today - la_date).days
                except:
                    days_since_active = 999
            else:
                days_since_active = 999
                
            if signals.get('open_to_work_flag'): beh_score += 4
            
            if days_since_active <= 7: beh_score += 5
            elif days_since_active <= 30: beh_score += 4
            elif days_since_active <= 60: beh_score += 2
            elif days_since_active <= 90: beh_score += 1
            elif days_since_active > 180: beh_score -= 2
            
            rrr = signals.get('recruiter_response_rate', 0)
            if rrr >= 0.7: beh_score += 3
            elif rrr >= 0.4: beh_score += 2
            elif rrr >= 0.2: beh_score += 1
            
            art = signals.get('avg_response_time_hours', 100)
            if art <= 4: beh_score += 2
            elif art <= 24: beh_score += 1
            elif art > 72: beh_score -= 1
            
            npd = signals.get('notice_period_days', 999)
            if npd <= 15: beh_score += 5
            elif npd <= 30: beh_score += 4
            elif npd <= 60: beh_score += 2
            elif npd <= 90: beh_score += 1
            elif npd > 90: beh_score -= 1
            
            icr = signals.get('interview_completion_rate', 0)
            if icr >= 0.9: beh_score += 3
            elif icr >= 0.7: beh_score += 2
            elif icr >= 0.5: beh_score += 1
            
            oar = signals.get('offer_acceptance_rate', -1)
            if oar >= 0.8: beh_score += 2
            elif oar >= 0.5: beh_score += 1
            
            gh = signals.get('github_activity_score', -1)
            if gh >= 70: beh_score += 3
            elif gh >= 40: beh_score += 2
            elif gh >= 20: beh_score += 1
            
            pcs = signals.get('profile_completeness_score', 0)
            if pcs >= 90: beh_score += 2
            elif pcs >= 70: beh_score += 1
            
            sbr = signals.get('saved_by_recruiters_30d', 0)
            if sbr >= 5: beh_score += 2
            elif sbr >= 2: beh_score += 1
            
            apps = signals.get('applications_submitted_30d', 0)
            if apps >= 3: beh_score += 1
            
            if signals.get('linkedin_connected'): beh_score += 1
            if signals.get('verified_email') and signals.get('verified_phone'): beh_score += 1
            
            behavioral_score = max(0, min(beh_score / 35.0, 1.0))
            
            edu_score = 0
            for ed in education:
                fos = ed.get('field_of_study', '').lower()
                is_rel_fos = any(rf in fos for rf in RELEVANT_FIELDS)
                is_neu_fos = any(nf in fos for nf in NEUTRAL_FIELDS)
                
                tier = ed.get('tier', '').lower()
                deg = ed.get('degree', '').lower()
                
                cur_ed = 0
                if is_rel_fos: cur_ed += 4
                elif is_neu_fos: cur_ed += 2
                
                if 'tier_1' in tier: cur_ed += 5
                elif 'tier_2' in tier: cur_ed += 3
                elif 'tier_3' in tier: cur_ed += 1
                
                if 'phd' in deg or 'doctor' in deg: cur_ed += 4
                elif 'm.tech' in deg or 'm.s' in deg or 'mba' in deg or 'master' in deg: cur_ed += 3
                elif 'b.tech' in deg or 'b.e' in deg or 'b.s' in deg or 'bachelor' in deg: cur_ed += 2
                else: cur_ed += 1
                
                if cur_ed > edu_score:
                    edu_score = cur_ed
                    
            education_score = min(edu_score / 13.0, 1.0)
            
            cert_score = 0
            hv_count = 0
            mv_count = 0
            for cert in certifications:
                c_name = cert.get('name', '').lower() if isinstance(cert, dict) else str(cert).lower()
                if any(hv in c_name for hv in HIGH_VALUE_CERTS):
                    hv_count += 1
                elif any(mv in c_name for mv in MEDIUM_VALUE_CERTS):
                    mv_count += 1
            
            cert_score += min(hv_count, 3) * 3
            cert_score += min(mv_count, 2) * 1
            certification_score = min(cert_score / 11.0, 1.0)
            
            country = profile.get('country', '')
            otw = signals.get('open_to_work_flag', False)
            wtr = signals.get('willing_to_relocate', False)
            
            if country == "India" and otw: location_score = 1.0
            elif country == "India" and not otw: location_score = 0.7
            elif country != "India" and wtr: location_score = 0.4
            else: location_score = 0.1
            
            sal = signals.get('expected_salary_range_inr_lpa', {})
            c_min = sal.get('min', 0)
            c_max = sal.get('max', 999)
            BUDGET_MIN = 25
            BUDGET_MAX = 55
            
            if c_max < BUDGET_MIN:
                salary_score = 0.6
            elif c_min > BUDGET_MAX:
                salary_score = 0.2
            else:
                overlap_min = max(c_min, BUDGET_MIN)
                overlap_max = min(c_max, BUDGET_MAX)
                overlap = overlap_max - overlap_min
                cand_range = c_max - c_min
                if cand_range <= 0:
                    cand_range = 1
                if overlap > 0:
                    salary_score = min(overlap / cand_range, 1.0)
                else:
                    salary_score = 1.0
                    
            trust_raw = 0
            if signals.get('verified_email'): trust_raw += 2
            if signals.get('verified_phone'): trust_raw += 2
            if signals.get('linkedin_connected'): trust_raw += 2
            if pcs >= 85: trust_raw += 2
            elif pcs >= 70: trust_raw += 1
            if signals.get('connection_count', 0) >= 200: trust_raw += 1
            if signals.get('endorsements_received', 0) >= 30: trust_raw += 1
            trust_score = min(trust_raw / 10.0, 1.0)
            
            final_score = (
                skill_score * 0.20 +
                career_score * 0.25 +
                behavioral_score * 0.20 +
                education_score * 0.10 +
                certification_score * 0.05 +
                location_score * 0.10 +
                salary_score * 0.05 +
                trust_score * 0.05
            )
            
            tier_str = "Unknown"
            if education:
                tier_str = education[0].get('tier', 'Unknown').title().replace('_', '-')
            
            top_skills = list(matched_must_haves)[:3]
            top_skills_str = ",".join(top_skills) if top_skills else "None"
            
            cur_title_display = profile.get('current_title', 'Unknown')
            reasoning = f"{cur_title_display.title()} {yoe}yr | Skills: {top_skills_str} | {tier_str} edu | Active {days_since_active}d ago | Notice {npd}d | Score: {final_score:.3f}"
            
            candidates.append({
                'candidate_id': cand_id,
                'final_score': final_score,
                'notice_period_days': npd,
                'recruiter_response_rate': rrr,
                'last_active_date': la_str if la_str else '1970-01-01',
                'reasoning': reasoning
            })
            
    print(f"\nTotal processed: {total_processed}")
    print(f"Honeypots removed: {honeypots_removed}")
    print(f"Eligible candidates: {len(candidates)}")
    
    candidates.sort(key=lambda x: (
        round(x['final_score'], 3),
        -x['notice_period_days'],
        x['recruiter_response_rate'],
        x['last_active_date']
    ), reverse=True)
    
    top_100 = candidates[:100]
    if top_100:
        score_max = top_100[0]['final_score']
        score_min = top_100[-1]['final_score']
        print(f"Top 100 selected")
        print(f"Score range: {score_min:.3f} - {score_max:.3f}")
    
    output_df = pd.DataFrame([{
        'candidate_id': c['candidate_id'],
        'rank': i + 1,
        'score': round(c['final_score'], 3),
        'reasoning': c['reasoning']
    } for i, c in enumerate(top_100)])
    
    output_df.to_csv(r'C:\Projects\H2S_India_Run\submission.csv', index=False)
    print("submission.csv saved!")

if __name__ == '__main__':
    load_and_score()
