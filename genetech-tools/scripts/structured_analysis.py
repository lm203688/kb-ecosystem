
# GeneTech 14站结构化分析模块
# 对每条实体添加结构化分析字段

import json, os, re

def analyze_entity(entity):
    """对实体进行结构化分析"""
    from shared.llm_client import call_llm
    
    title = entity.get("title", entity.get("name", ""))
    abstract = entity.get("abstract", entity.get("summary", ""))
    
    prompt = f"""分析以下科研实体，输出结构化分析：
标题: {title}
摘要: {abstract[:500]}

输出JSON:
{{
  "summary_zh": "中文摘要(100字内)",
  "keywords": ["关键词1", "关键词2"],
  "category": "分类(如gene_therapy/CRISPR/bioinformatics)",
  "innovation_level": "创新等级(高/中/低)",
  "application_areas": ["应用领域"],
  "technical_difficulty": "技术难度(1-5)",
  "commercial_potential": "商业化潜力(1-5)",
  "related_entities": ["相关实体ID"],
  "relevance_score": 0.0-1.0
}}"""
    
    try:
        result = call_llm(prompt, model="glm-4-flash", max_tokens=300)
        match = re.search(r'\{[\s\S]*\}', result)
        if match:
            analysis = json.loads(match.group())
            analysis["analyzed_at"] = "2026-07-04"
            return analysis
    except:
        pass
    return None

def batch_analyze_site(site_dir, max_entities=50):
    """批量分析一个站点的实体"""
    entity_dir = os.path.join(site_dir, "knowledge-base", "entities")
    if not os.path.exists(entity_dir):
        return 0
    
    count = 0
    for ef in os.listdir(entity_dir):
        if not ef.endswith(".json"):
            continue
        epath = os.path.join(entity_dir, ef)
        with open(epath) as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            entities = data.get("entities", data.get("data", []))
        else:
            entities = data
        
        # 只分析没有analysis字段的实体
        to_analyze = [e for e in entities if "analysis" not in e][:max_entities]
        
        for e in to_analyze:
            analysis = analyze_entity(e)
            if analysis:
                e["analysis"] = analysis
                count += 1
                if count >= max_entities:
                    break
        
        # 保存
        if isinstance(data, dict):
            data["entities"] = entities
        else:
            data = entities
        with open(epath, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        break
    
    return count
