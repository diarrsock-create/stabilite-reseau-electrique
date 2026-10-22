"""Fonctions reutilisables du projet : chargement, variables construites, analyse des seuils."""
import numpy as np
import pandas as pd

# Les 12 variables de reglage du jeu de donnees (stab et stabf sont exclues : fuite)
BASE_COLS = ["tau1", "tau2", "tau3", "tau4",
             "p1", "p2", "p3", "p4",
             "g1", "g2", "g3", "g4"]

# Variables construites (calculees ligne par ligne : aucune fuite avant le split)
NOUVELLES_COLS = ["tau_moyen", "g_moyen", "tau_g_moyen"]


def charger_donnees(chemin):
    """Lit le CSV et ajoute la cible numerique : 1 = instable, 0 = stable."""
    df = pd.read_csv(chemin)
    df["instable"] = (df["stabf"] == "unstable").astype(int)
    return df


def ajouter_variables(df):
    """Ajoute 3 variables metier : reaction moyenne, sensibilite moyenne, leur produit moyen."""
    df = df.copy()
    taus = df[["tau1", "tau2", "tau3", "tau4"]].values
    gs = df[["g1", "g2", "g3", "g4"]].values
    df["tau_moyen"] = taus.mean(axis=1)
    df["g_moyen"] = gs.mean(axis=1)
    df["tau_g_moyen"] = (taus * gs).mean(axis=1)
    return df


def colonnes_modele():
    """Liste des variables donnees au modele."""
    return BASE_COLS + NOUVELLES_COLS


def table_seuils(y, proba, seuils, c_fn, c_sim, n_an):
    """Compare des seuils de decision : metriques et cout annuel.

    Regle de decision : si proba >= seuil, on lance la simulation complete ;
    sinon on applique le reglage directement.
    - Vrai positif / faux positif : une simulation est lancee (cout c_sim).
    - Faux negatif : un reglage instable est applique (cout c_fn).
    - Sans modele : on simule tous les reglages (cout n_an * c_sim).
    """
    y = np.asarray(y)
    proba = np.asarray(proba)
    n = len(y)
    echelle = n_an / n          # ramene les comptages de l'echantillon a une annee
    lignes = []
    for s in seuils:
        pred = (proba >= s).astype(int)
        tp = int(((pred == 1) & (y == 1)).sum())
        fp = int(((pred == 1) & (y == 0)).sum())
        fn = int(((pred == 0) & (y == 1)).sum())
        tn = int(((pred == 0) & (y == 0)).sum())
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        cout_modele = ((tp + fp) * c_sim + fn * c_fn) * echelle
        cout_sans = n_an * c_sim
        lignes.append({
            "seuil": round(float(s), 3), "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "precision": precision, "recall": recall, "f1": f1,
            "simu_evitees": (tn + fn) / n,
            "cout_avec_modele": cout_modele,
            "cout_sans_modele": cout_sans,
            "gain_annuel": cout_sans - cout_modele,
        })
    return pd.DataFrame(lignes)


def choisir_seuil(table, recall_min):
    """Seuil de cout minimal parmi ceux qui respectent le recall minimal.
    Si aucun seuil ne le respecte, renvoie le seuil de cout minimal global."""
    admissibles = table[table["recall"] >= recall_min]
    base = admissibles if len(admissibles) else table
    return float(base.loc[base["cout_avec_modele"].idxmin(), "seuil"])