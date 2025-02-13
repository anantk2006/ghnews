import { useState, useEffect } from "react";

export interface Article {
  articleName: string;
  datePublished: string;
  url: string;
  tag: string;
}

export interface Headlines {
  [topic: string]: Article[];
}

export default function Headlines() {
  const [articles, setArticles] = useState<Headlines | null>(null);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/headlines", {
          method: "GET",
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
        const data = await res.json();
        setArticles(data);
      } catch (error) {
        console.error("Failed to fetch articles:", error);
      }
    };

    fetchArticles();
  }, []);

  if (!articles) {
    return <div>Loading...</div>; // Add a loading state
  }
  console.log(articles);
  var art_k = 0;
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-8">Latest Headlines</h1>
      <div className="space-y-8">
        {Object.entries(articles).map(([topic, articles]) => (
          <section key={++art_k}>
            <h2 className="text-2xl font-semibold capitalize mb-4">{topic}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article) => (
                <a
                  key={++art_k}
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
                >
                  <h3 className="text-xl font-medium">{article.articleName}</h3>
                </a>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}