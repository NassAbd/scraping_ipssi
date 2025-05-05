import { useState } from 'react'
import axios from 'axios'

function App() {
  const [url, setUrl] = useState('')
  const [category, setCategory] = useState('')
  const [articles, setArticles] = useState([])
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleScrape = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/scrape/', { url });
      setMessage(res.data.message);
      setError('');
    } catch (err) {
      setMessage('');
      if (err.response) {
        setError(err.response.data?.detail || err.response.data?.error || 'Erreur lors du scraping');
      } else {
        setError('Erreur de réseau ou serveur non disponible');
      }
    }
  };

  const handleFetchArticles = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/articles/?category=${category}`)
      setArticles(res.data)
      setError('')
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors du chargement des articles')
    }
  }

  const handleFetchAllArticles = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/articles/all/')
      setArticles(res.data)
      setError('')
    } catch (err) {
      setError(err.response?.data?.error || 'Erreur lors du chargement des articles')
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>📰 Scraper & Afficher Articles</h1>

      <div>
        <h2>🔍 Scraper un article</h2>
        <input
          type="text"
          placeholder="URL de l'article"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: '400px', marginRight: '1rem' }}
        />
        <button onClick={handleScrape}>Scraper</button>
      </div>

      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div style={{ marginTop: '2rem' }}>
        <h2>📂 Rechercher des articles par catégorie</h2>
        <input
          type="text"
          placeholder="Catégorie ou sous-catégorie"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{ width: '300px', marginRight: '1rem' }}
        />
        <button onClick={handleFetchArticles}>Chercher</button>
        <button onClick={handleFetchAllArticles}>Tous les articles</button>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <h2>🗂 Articles trouvés</h2>
        {articles.length === 0 ? (
          <p>Aucun article.</p>
        ) : (
          articles.map((article) => (
            <div key={article._id} style={{ border: '1px solid #ccc', margin: '1rem 0', padding: '1rem' }}>
              <h3>{article.title}</h3>
              {article.thumbnail && (
                <img
                  src={article.thumbnail}
                  alt={`Thumbnail de ${article.title}`}
                  style={{ maxWidth: '30%', height: 'auto', marginBottom: '1rem' }}
                />
              )}
              <p><strong>Date:</strong> {article.date}</p>
              <p><strong>Auteur:</strong> {article.author}</p>
              <p><strong>Résumé:</strong> {article.summary}</p>
              <p><strong>Catégorie:</strong> {article.category}</p>
              <p><strong>Sous-Catégorie:</strong> {article.sub_category}</p>
              <a href={article.url} target="_blank" rel="noopener noreferrer">Voir l'article</a>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default App
