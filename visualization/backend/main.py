import random
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----- 数据结构 -----
class Node(BaseModel):
    id: str
    label: str
    group: str
    tag: str = ""
    expanded: bool = False
    combo: str = ""
    parent: str = ""


class Edge(BaseModel):
    source: str
    target: str
    amount: float


# ----- Mock数据 -----
MOCK_NODES = [
    Node(id=str(i), label=str(i), group="normal") for i in range(20)
]  # 增加到20个节点

MOCK_EDGES = [
    Edge(source="0", target="1", amount=1000),
    Edge(source="0", target="2", amount=1000),
    Edge(source="0", target="3", amount=1000),
    Edge(source="0", target="4", amount=1000),
    Edge(source="0", target="5", amount=1000),
    Edge(source="0", target="7", amount=1000),
    Edge(source="0", target="8", amount=1000),
    Edge(source="0", target="9", amount=1000),
    Edge(source="2", target="3", amount=1000),
    Edge(source="4", target="5", amount=1000),
    Edge(source="4", target="6", amount=1000),
    Edge(source="5", target="6", amount=1000),
    Edge(source="1", target="10", amount=1000),
    Edge(source="2", target="11", amount=1000),
    Edge(source="3", target="12", amount=1000),
    Edge(source="4", target="13", amount=1000),
    Edge(source="5", target="14", amount=1000),
    Edge(source="6", target="15", amount=1000),
    Edge(source="7", target="16", amount=1000),
    Edge(source="8", target="17", amount=1000),
    Edge(source="9", target="18", amount=1000),
    Edge(source="10", target="11", amount=1000),
    Edge(source="11", target="12", amount=1000),
    Edge(source="12", target="13", amount=1000),
    Edge(source="13", target="14", amount=1000),
    Edge(source="14", target="15", amount=1000),
    Edge(source="15", target="16", amount=1000),
    Edge(source="16", target="17", amount=1000),
    Edge(source="17", target="18", amount=1000),
    Edge(source="18", target="19", amount=1000),
    Edge(source="19", target="0", amount=1000),
]

MOCK_LABELS = {str(i): f"Node {i}" for i in range(20)}

# 新增combo组
COMBO_GROUPS = ["a", "b", "c", "d", "e", "f"]

# 为每个节点随机分配combo组
for node in MOCK_NODES:
    node.combo = random.choice(COMBO_GROUPS)

# 新增combos数组
MOCK_COMBOS = [
    {"id": "a", "data": {"label": "Combo A"}},
    {"id": "b", "data": {"label": "Combo B"}},
    {"id": "c", "data": {"label": "Combo C"}},
    {"id": "d", "data": {"label": "Combo D"}},
    {"id": "e", "data": {"label": "Combo E"}},
    {"id": "f", "data": {"label": "Combo F"}},
]


# ------ API接口 -------
@app.get("/api/graph/init")
def get_graph():
    nodes = [n.dict() for n in MOCK_NODES]
    edges = [e.dict() for e in MOCK_EDGES]
    return {"nodes": nodes, "edges": edges, "combos": MOCK_COMBOS}


@app.get("/api/address/{address}/top-tx")
def top_tx(address: str):
    # 返回5个模拟节点和边
    nodes = []
    edges = []
    # 获取父节点的combo组
    parent_node = next((node for node in MOCK_NODES if node.id == address), None)
    parent_combo = parent_node.combo if parent_node else random.choice(COMBO_GROUPS)

    # 从父节点ID中提取数字部分
    try:
        base_num = int(address.replace("0x", ""), 16)
    except ValueError:
        base_num = 0

    for i in range(5):
        # 生成2-9的随机数
        random_num = random.randint(2, 9)
        # 基于父节点ID递增生成新ID，并加入随机数
        nid = f"{random_num}{base_num + i + 1}"
        node = Node(id=nid, label=str(nid), group="normal")
        node.combo = parent_combo  # 使用与父节点相同的combo组
        node.parent = address  # 明确指定父节点
        nodes.append(node.dict())
        edges.append(
            Edge(source=address, target=nid, amount=random.randint(50, 5000)).dict()
        )
    return {"nodes": nodes, "edges": edges}


@app.get("/api/address/{address}/label")
def get_label(address: str):
    return {"label": MOCK_LABELS.get(address, "Unknown")}


@app.post("/api/address/{address}/label")
def set_label(address: str, label: str):
    MOCK_LABELS[address] = label
    return {"result": "ok"}
