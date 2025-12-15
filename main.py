from graph.graph import build_graph

if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({
        "user_query": "Explique a Revolução Francesa para um aluno do ensino médio"
    })
    print(result["final_report"])
