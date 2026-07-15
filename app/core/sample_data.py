from __future__ import annotations

# 后续如果接入 Neo4j，只需要把 graph_service 的底层实现替换掉，接口层和 Agent 都不用改。
SAMPLE_GRAPH = {
    "糖尿病": {
        "symptoms": ["多饮", "多尿", "体重下降", "视力模糊"],
        "drugs": ["二甲双胍", "格列美脲"],
        "departments": ["内分泌科"],
        "checks": ["空腹血糖", "糖化血红蛋白"],
        "do_eat": ["燕麦", "西蓝花", "黄瓜"],
        "not_eat": ["含糖饮料", "蛋糕", "油炸食品"],
        "dishes": ["清炒西蓝花", "燕麦粥"],
        "companions": ["高血压", "糖尿病肾病"],
        "category": ["代谢性疾病"],
        "cureways": ["饮食控制", "运动干预", "药物治疗"],
    },
    "高血压": {
        "symptoms": ["头晕", "头痛", "心悸"],
        "drugs": ["氨氯地平", "缬沙坦"],
        "departments": ["心血管内科"],
        "checks": ["血压监测", "心电图"],
        "do_eat": ["芹菜", "燕麦"],
        "not_eat": ["高盐腌制食品", "浓茶"],
        "dishes": ["清蒸鱼", "芹菜炒木耳"],
        "companions": ["冠心病"],
        "category": ["心血管疾病"],
        "cureways": ["生活方式管理", "药物治疗"],
    },
}

SAMPLE_USERS = [
    {"username": "cc", "email": "cc@example.com"},
    {"username": "alice", "email": "alice@example.com"},
    {"username": "bob", "email": "bob@example.com"},
]

DEFAULT_DOCS = [
    {
        "title": "糖尿病基础知识",
        "source_id": "doc-diabetes-basic",
        "content": "糖尿病是一组以慢性高血糖为特征的代谢性疾病。常见症状包括多饮、多尿、体重下降和视力模糊。管理策略通常包含饮食控制、运动干预和药物治疗。",
        "metadata": {"topic": "medical", "disease": "糖尿病"},
    },
    {
        "title": "高血压日常管理",
        "source_id": "doc-hypertension-basic",
        "content": "高血压患者需要长期监测血压，控制盐摄入，并在医生指导下使用降压药物。常见就诊科室为心血管内科。",
        "metadata": {"topic": "medical", "disease": "高血压"},
    },
    {
        "title": "验证码业务说明",
        "source_id": "doc-verification-flow",
        "content": "系统支持根据用户名查询邮箱、发送验证码并校验验证码。开发模式下不会真正发信，而是把验证码保存在本地内存中用于联调。",
        "metadata": {"topic": "system", "module": "verification"},
    },
]
