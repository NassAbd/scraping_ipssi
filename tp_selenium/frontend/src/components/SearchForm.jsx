import React, { useState } from "react";
import axios from "axios";

function SearchForm() {
  const [results, setResults] = useState([]);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSearched(false);

    const form = e.target;
    const data = {
      query: form.query.value,
      max_results: parseInt(form.max_results.value),
      assurance: form.assurance.value,
      location: form.location.value,
    };

    try {
      const res = await axios.post("http://localhost:8000/search", data);
      setResults(res.data);
    } catch (error) {
      console.error("Erreur lors de la requête :", error);
      setResults([]);
    } finally {
      setLoading(false);
      setSearched(true);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input name="query" placeholder="Spécialité" />
        <input name="max_results" type="number" defaultValue={3} />
        <select name="assurance">
          <option value="1">Secteur 1</option>
          <option value="2">Secteur 2</option>
          <option value="nc">Non conventionné</option>
        </select>
        <input name="location" placeholder="Adresse ou code postal" />
        <button type="submit">Rechercher</button>
      </form>

      {loading ? (
        <p style={{ animation: "blink 1s infinite" }}>Chargement...</p>
      ) : searched && results.length === 0 ? (
        <p>Pas de résultat pour ces critères</p>
      ) : (
        <ul>
          {results.map((doc, i) => (
            <li key={i}>
              <strong>{doc.nom}</strong> – {doc.disponibilite} – {doc.secteur}
              <br />
              {doc.rue}, {doc.cp} {doc.ville}
            </li>
          ))}
        </ul>
      )}

      <style>{`
        @keyframes blink {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.3; }
        }
      `}</style>
    </div>
  );
}

export default SearchForm;
