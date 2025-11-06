from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerar relações (mock, sempre funciona)
@app.route('/generate', methods=['POST'])
def generate():
    text = request.json.get('text', '').strip()
    if not text:
        return jsonify({"entities": [], "relations": []})

    # Simples parser local baseado em palavras-chave
    entities = set()
    relations = []

    # "is ... of" ou "owns a" ou "lives in" ou "member of"
    words = text.split()
    if "is" in words and "'s" in text:
        parts = text.split(" is ")
        subject = parts[0].strip()
        rest = parts[1].split("'s")
        obj = rest[0].strip()
        rel = rest[1].strip()
        entities.update([subject, obj])
        relations.append({"subject": subject, "relation": rel, "object": obj})
    elif "owns a" in text:
        parts = text.split(" owns a ")
        entities.update([parts[0].strip(), parts[1].strip()])
        relations.append({"subject": parts[0].strip(), "relation": "owns", "object": parts[1].strip()})
    elif "lives in" in text:
        parts = text.split(" lives in ")
        entities.update([parts[0].strip(), parts[1].strip()])
        relations.append({"subject": parts[0].strip(), "relation": "lives_in", "object": parts[1].strip()})
    elif "member of" in text:
        parts = text.split(" is member of ")
        entities.update([parts[0].strip(), parts[1].strip()])
        relations.append({"subject": parts[0].strip(), "relation": "member_of", "object": parts[1].strip()})
    else:
        # Caso padrão para teste
        entities.update(["Linda", "Josh", "Ben"])
        relations.extend([
            {"subject":"Linda","relation":"mother","object":"Josh"},
            {"subject":"Ben","relation":"brother","object":"Josh"}
        ])

    return jsonify({
        "entities": list(entities),
        "relations": relations
    })

if __name__ == "__main__":
    app.run(debug=True)
