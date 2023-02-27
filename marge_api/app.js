const express = require("express");
const fs = require("fs");
const app = express();
const port = 3000;

app.use(express.json()); // permettre la lecture des données au format JSON

// Créer une route pour les requêtes POST pour l'enregistrement de l'emargement
app.post("/marge", (req, res) => {
    const nom = req.body.nom;
    const date = req.body.date;
    const heure = req.body.heure;

    // Ajouter les données de l'emargement dans le fichier logs.json
    let logs = {};
    if (fs.existsSync("logs.json")) {
        logs = JSON.parse(fs.readFileSync("logs.json"));
    }
    if (logs[date] === undefined) {
        logs[date] = [{ nom: nom, heure: heure }];
    } else {
        logs[date].push({ nom: nom, heure: heure });
    }
    fs.writeFileSync("logs.json", JSON.stringify(logs, null, 2));

    res.send(`Emargement enregistré pour ${nom} le ${date} à ${heure}`);
});

app.listen(port, () => {
    console.log(`Serveur lancé à l'adresse http://localhost:${port}`);
});
