from __future__ import annotations

from app.core.sample_data import SAMPLE_GRAPH
from app.core.schemas import RetrievalHit


class GraphService:
    """本地内存图谱服务。

    为了保证课程项目在未安装 Neo4j 的机器上也能跑通，这里先提供等价的图谱查询能力。
    """

    FIELD_ALIASES = {
        "症状": "symptoms",
        "药": "drugs",
        "药物": "drugs",
        "科室": "departments",
        "检查": "checks",
        "能吃": "do_eat",
        "推荐吃": "do_eat",
        "不能吃": "not_eat",
        "不推荐吃": "not_eat",
        "菜肴": "dishes",
        "并发症": "companions",
        "分类": "category",
        "治疗": "cureways",
    }

    def search_by_question(self, question: str) -> list[RetrievalHit]:
        """根据中文问题做模板化图谱查询。

        这里不用让模型直接写 Cypher，目的是先把课程项目做成更安全、可本地运行的版本。
        """

        disease = self._match_disease(question)
        if not disease:
            return []

        field = self._infer_field(question)
        if not field:
            return []

        values = SAMPLE_GRAPH.get(disease, {}).get(field, [])
        return [
            RetrievalHit(
                source_type="graph",
                source_id=f"graph:{disease}:{field}",
                title=f"{disease}-{field}",
                content=f"{disease}相关{field}: {'、'.join(values)}",
                score=1.0,
                metadata={"disease": disease, "field": field, "values": values},
            )
        ] if values else []

    def raw_lookup(self, disease: str, relation: str) -> dict:
        """给 MCP 工具使用的结构化查询。"""

        key = self.FIELD_ALIASES.get(relation, relation)
        values = SAMPLE_GRAPH.get(disease, {}).get(key, [])
        return {"disease": disease, "relation": key, "values": values}

    def _match_disease(self, question: str) -> str | None:
        for disease in SAMPLE_GRAPH:
            if disease in question:
                return disease
        return None

    def _infer_field(self, question: str) -> str | None:
        for keyword, field in self.FIELD_ALIASES.items():
            if keyword in question:
                return field
        return None
