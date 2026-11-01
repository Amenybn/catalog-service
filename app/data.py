"""Données initiales du catalogue (chaque microservice possède ses propres données)."""


def seed_products():
    rows = [
        (1, "Ordinateur portable Pro 14\"", "Informatique", 1299.00, 8, "💻", "Processeur 8 cœurs, 16 Go de RAM, SSD 512 Go."),
        (2, "Souris sans fil ergonomique", "Informatique", 49.90, 35, "🖱️", "Capteur précis, autonomie de 70 jours."),
        (3, "Clavier mécanique RGB", "Informatique", 89.00, 4, "⌨️", "Switchs silencieux, rétroéclairage personnalisable."),
        (4, "Écran 27\" 4K", "Informatique", 379.00, 12, "🖥️", "Dalle IPS, 60 Hz, couleurs calibrées."),
        (5, "Casque à réduction de bruit", "Audio", 249.00, 15, "🎧", "Réduction de bruit active, 30 h d'autonomie."),
        (6, "Enceinte Bluetooth", "Audio", 79.90, 3, "🔊", "Son 360°, étanche IP67."),
        (7, "Écouteurs sans fil", "Audio", 129.00, 20, "🎶", "Boîtier de charge sans fil, appels clairs."),
        (8, "Machine à café expresso", "Maison", 199.00, 6, "☕", "Pression 15 bars, buse vapeur."),
        (9, "Lampe connectée", "Maison", 34.90, 40, "💡", "16 millions de couleurs, pilotable à la voix."),
        (10, "Aspirateur robot", "Maison", 299.00, 2, "🤖", "Cartographie laser, vidage automatique."),
        (11, "Montre connectée sport", "Sport", 189.00, 10, "⌚", "GPS, cardio, 50 m étanche."),
        (12, "Vélo d'appartement", "Sport", 459.00, 5, "🚲", "16 niveaux de résistance, écran LCD."),
    ]
    return [
        {
            "id": pid,
            "name": name,
            "category": category,
            "price": price,
            "stock": stock,
            "sold": 0,
            "emoji": emoji,
            "description": description,
        }
        for pid, name, category, price, stock, emoji, description in rows
    ]
