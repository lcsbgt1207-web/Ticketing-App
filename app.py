from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Stockage en mémoire
tickets = []
ticket_id = 1

TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>HelpDesk — Ticketing</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #0f0f1a; color: #e0e0e0; }
  
  .navbar { background: #1a1a2e; padding: 16px 32px; display: flex; align-items: center; gap: 12px; border-bottom: 2px solid #e94560; }
  .navbar h1 { font-size: 22px; color: #fff; }
  .navbar span { background: #e94560; color: white; padding: 2px 10px; border-radius: 12px; font-size: 12px; }
  
  .container { max-width: 1100px; margin: 32px auto; padding: 0 24px; }
  
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
  .stat-card { background: #1a1a2e; border-radius: 8px; padding: 20px; border-left: 4px solid #e94560; }
  .stat-card .number { font-size: 32px; font-weight: bold; color: #e94560; }
  .stat-card .label { font-size: 13px; color: #888; margin-top: 4px; }
  
  .card { background: #1a1a2e; border-radius: 8px; padding: 24px; margin-bottom: 24px; }
  .card h2 { margin-bottom: 16px; font-size: 16px; color: #e94560; text-transform: uppercase; letter-spacing: 1px; }
  
  .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .form-group { display: flex; flex-direction: column; gap: 6px; }
  .form-group.full { grid-column: 1 / -1; }
  .form-group label { font-size: 12px; color: #888; text-transform: uppercase; }
  .form-group input, .form-group select, .form-group textarea {
    background: #0f0f1a; border: 1px solid #333; border-radius: 6px;
    padding: 10px 12px; color: #e0e0e0; font-size: 14px; font-family: inherit;
  }
  .form-group textarea { height: 80px; resize: vertical; }
  .btn { background: #e94560; color: white; border: none; padding: 12px 24px;
    border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: bold;
    margin-top: 8px; transition: background 0.2s; }
  .btn:hover { background: #c73652; }
  .btn-sm { padding: 6px 14px; font-size: 12px; margin-top: 0; }
  .btn-close { background: #333; }
  .btn-close:hover { background: #555; }

  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; padding: 10px 14px; font-size: 11px; color: #888; text-transform: uppercase; border-bottom: 1px solid #333; }
  td { padding: 12px 14px; font-size: 13px; border-bottom: 1px solid #1f1f2e; vertical-align: middle; }
  tr:hover td { background: #16162a; }
  
  .badge { padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; }
  .badge-ouvert { background: #1a3a5c; color: #4da6ff; }
  .badge-en-cours { background: #3a2a00; color: #ffa500; }
  .badge-ferme { background: #1a3a1a; color: #4caf50; }
  .badge-haute { background: #3a1a1a; color: #e94560; }
  .badge-moyenne { background: #3a2a00; color: #ffa500; }
  .badge-basse { background: #1a2a1a; color: #4caf50; }
  
  .empty { text-align: center; padding: 40px; color: #555; }
</style>
</head>
<body>

<div class="navbar">
  <h1>🛡️ HelpDesk</h1>
  <span>Ticketing IT</span>
</div>

<div class="container">

  <!-- Stats -->
  <div class="stats">
    <div class="stat-card">
      <div class="number">{{ tickets|length }}</div>
      <div class="label">Total tickets</div>
    </div>
    <div class="stat-card">
      <div class="number">{{ tickets|selectattr('statut', 'equalto', 'Ouvert')|list|length }}</div>
      <div class="label">Ouverts</div>
    </div>
    <div class="stat-card">
      <div class="number">{{ tickets|selectattr('statut', 'equalto', 'En cours')|list|length }}</div>
      <div class="label">En cours</div>
    </div>
    <div class="stat-card">
      <div class="number">{{ tickets|selectattr('statut', 'equalto', 'Fermé')|list|length }}</div>
      <div class="label">Fermés</div>
    </div>
  </div>

  <!-- Formulaire -->
  <div class="card">
    <h2>Nouveau ticket</h2>
    <form method="POST" action="/create">
      <div class="form-grid">
        <div class="form-group">
          <label>Titre</label>
          <input type="text" name="titre" placeholder="Ex: Imprimante hors service" required>
        </div>
        <div class="form-group">
          <label>Demandeur</label>
          <input type="text" name="demandeur" placeholder="Nom prénom" required>
        </div>
        <div class="form-group">
          <label>Catégorie</label>
          <select name="categorie">
            <option>Matériel</option>
            <option>Réseau</option>
            <option>Logiciel</option>
            <option>Sécurité</option>
            <option>Accès / Droits</option>
            <option>Autre</option>
          </select>
        </div>
        <div class="form-group">
          <label>Priorité</label>
          <select name="priorite">
            <option>Haute</option>
            <option>Moyenne</option>
            <option>Basse</option>
          </select>
        </div>
        <div class="form-group full">
          <label>Description</label>
          <textarea name="description" placeholder="Décris le problème..."></textarea>
        </div>
      </div>
      <button class="btn" type="submit">Créer le ticket</button>
    </form>
  </div>

  <!-- Liste tickets -->
  <div class="card">
    <h2>Tickets ({{ tickets|length }})</h2>
    {% if tickets %}
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Titre</th>
          <th>Demandeur</th>
          <th>Catégorie</th>
          <th>Priorité</th>
          <th>Statut</th>
          <th>Date</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {% for t in tickets|reverse %}
        <tr>
          <td>#{{ t.id }}</td>
          <td><strong>{{ t.titre }}</strong><br><small style="color:#666">{{ t.description[:50] }}{% if t.description|length > 50 %}...{% endif %}</small></td>
          <td>{{ t.demandeur }}</td>
          <td>{{ t.categorie }}</td>
          <td><span class="badge badge-{{ t.priorite|lower }}">{{ t.priorite }}</span></td>
          <td>
            <span class="badge badge-{{ t.statut|lower|replace(' ', '-') }}">{{ t.statut }}</span>
          </td>
          <td style="font-size:11px;color:#666">{{ t.date }}</td>
          <td>
            {% if t.statut == 'Ouvert' %}
            <a href="/update/{{ t.id }}/En cours"><button class="btn btn-sm">Prendre</button></a>
            {% elif t.statut == 'En cours' %}
            <a href="/update/{{ t.id }}/Fermé"><button class="btn btn-sm btn-close">Fermer</button></a>
            {% else %}
            <span style="color:#555;font-size:11px">—</span>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <div class="empty">Aucun ticket pour l'instant.</div>
    {% endif %}
  </div>

</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, tickets=tickets)

@app.route('/create', methods=['POST'])
def create():
    global ticket_id
    ticket = {
        'id': ticket_id,
        'titre': request.form['titre'],
        'demandeur': request.form['demandeur'],
        'categorie': request.form['categorie'],
        'priorite': request.form['priorite'],
        'description': request.form.get('description', ''),
        'statut': 'Ouvert',
        'date': datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    tickets.append(ticket)
    ticket_id += 1
    return redirect(url_for('index'))

@app.route('/update/<int:tid>/<statut>')
def update(tid, statut):
    for t in tickets:
        if t['id'] == tid:
            t['statut'] = statut
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
