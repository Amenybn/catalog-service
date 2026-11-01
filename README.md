# QuickShop · catalog-service

Microservice **catalogue** de QuickShop (Python 3.12 + FastAPI) : produits, catégories et stock.
Service **interne** : appelé par la gateway (lecture) et par order-service (réservation de stock).

```bash
docker build -t catalog-service .
docker run -d -p 8001:8001 catalog-service
```

Documentation interactive : `http://<hote>:8001/docs`

| Méthode | Route | Rôle |
|---|---|---|
| GET | `/health`, `/info` | Supervision |
| GET | `/products?category=&q=&lowStock=` | Liste des produits |
| GET | `/products/{id}` · `/categories` | Détail, catégories |
| POST | `/products/{id}/reserve` · `/products/{id}/release` | Réserver / remettre du stock (`{"quantity": n}`) |
| PUT | `/products/{id}/stock` | Réapprovisionner (`{"stock": n}`) |

| Variable | Défaut | Rôle |
|---|---|---|
| `PORT` | `8001` | Port HTTP |
| `LOW_STOCK_THRESHOLD` | `5` | Seuil de stock bas |

Utilisateur non-root `1000:1000`, aucune écriture disque. Données en mémoire.
