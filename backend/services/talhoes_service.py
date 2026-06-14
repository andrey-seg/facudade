"""Serviço de gerenciamento de talhões."""

from typing import Dict, Any, List, Optional
from datetime import datetime

# Base de dados em memória para talhões
_talhoes_db: List[Dict[str, Any]] = [
    {"id": 1, "nome": "Talhão A1", "area": 32, "cultura": "soja", "status": "ok",
     "previsao_colheita": "Setembro/2026", "produtividade": 64},
    {"id": 2, "nome": "Talhão A2", "area": 28, "cultura": "soja", "status": "ok",
     "previsao_colheita": "Setembro/2026", "produtividade": 62},
    {"id": 3, "nome": "Talhão B1", "area": 25, "cultura": "milho", "status": "ok",
     "previsao_colheita": "Outubro/2026", "produtividade": 58},
    {"id": 4, "nome": "Talhão C1", "area": 20, "cultura": "cafe", "status": "ok",
     "previsao_colheita": "Agosto/2026", "produtividade": 45},
    {"id": 5, "nome": "Talhão B2", "area": 20, "cultura": "milho", "status": "atencao",
     "previsao_colheita": "Outubro/2026", "produtividade": 52},
    {"id": 6, "nome": "Talhão C2", "area": 15, "cultura": "cafe", "status": "ok",
     "previsao_colheita": "Agosto/2026", "produtividade": 48},
    {"id": 7, "nome": "Talhão D1", "area": 25, "cultura": "algodao", "status": "ok",
     "previsao_colheita": "Novembro/2026", "produtividade": 55},
    {"id": 8, "nome": "Talhão A3", "area": 30, "cultura": "soja", "status": "ok",
     "previsao_colheita": "Setembro/2026", "produtividade": 60},
    {"id": 9, "nome": "Talhão B3", "area": 20, "cultura": "milho", "status": "atencao",
     "previsao_colheita": "Outubro/2026", "produtividade": 50},
    {"id": 10, "nome": "Talhão C3", "area": 10, "cultura": "cafe", "status": "ok",
     "previsao_colheita": "Agosto/2026", "produtividade": 46},
    {"id": 11, "nome": "Talhão D2", "area": 20, "cultura": "algodao", "status": "ok",
     "previsao_colheita": "Novembro/2026", "produtividade": 53},
    {"id": 12, "nome": "Talhão A4", "area": 30, "cultura": "soja", "status": "ok",
     "previsao_colheita": "Setembro/2026", "produtividade": 63},
]


def listar_talhoes() -> List[Dict[str, Any]]:
    """Retorna todos os talhões cadastrados."""
    return _talhoes_db


def obter_talhao(talhao_id: int) -> Optional[Dict[str, Any]]:
    """Retorna um talhão específico pelo ID."""
    for talhao in _talhoes_db:
        if talhao["id"] == talhao_id:
            return talhao
    return None


def criar_talhao(dados: Dict[str, Any]) -> Dict[str, Any]:
    """Cria um novo talhão."""
    novo_id = max(t["id"] for t in _talhoes_db) + 1 if _talhoes_db else 1
    talhao = {
        "id": novo_id,
        "nome": dados["nome"],
        "area": float(dados["area"]),
        "cultura": dados.get("cultura", "soja"),
        "status": dados.get("status", "ok"),
        "previsao_colheita": dados.get("previsao_colheita", ""),
        "produtividade": float(dados.get("produtividade", 0)),
    }
    _talhoes_db.append(talhao)
    return talhao


def atualizar_talhao(talhao_id: int, dados: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Atualiza um talhão existente."""
    talhao = obter_talhao(talhao_id)
    if not talhao:
        return None

    if "nome" in dados:
        talhao["nome"] = dados["nome"]
    if "area" in dados:
        talhao["area"] = float(dados["area"])
    if "cultura" in dados:
        talhao["cultura"] = dados["cultura"]
    if "status" in dados:
        talhao["status"] = dados["status"]
    if "previsao_colheita" in dados:
        talhao["previsao_colheita"] = dados["previsao_colheita"]
    if "produtividade" in dados:
        talhao["produtividade"] = float(dados["produtividade"])

    return talhao


def excluir_talhao(talhao_id: int) -> bool:
    """Exclui um talhão pelo ID."""
    for i, t in enumerate(_talhoes_db):
        if t["id"] == talhao_id:
            _talhoes_db.pop(i)
            return True
    return False


def resumo_talhoes() -> Dict[str, Any]:
    """Retorna um resumo estatístico dos talhões."""
    total_area = sum(t["area"] for t in _talhoes_db)
    culturas: Dict[str, float] = {}
    for t in _talhoes_db:
        culturas[t["cultura"]] = culturas.get(t["cultura"], 0) + t["area"]

    return {
        "total_talhoes": len(_talhoes_db),
        "area_total": round(total_area, 2),
        "area_ocupada": round(total_area, 2),
        "percentual_ocupacao": 100.0,
        "culturas": {c: round(a, 2) for c, a in culturas.items()},
        "talhoes": _talhoes_db,
    }
