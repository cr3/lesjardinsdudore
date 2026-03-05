import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import styled from 'styled-components';

const API_URL = import.meta.env.VITE_API_URL || '';

interface PlantResult {
  scientific_name: string;
  common_names: string[];
}

interface PlantDetail {
  [key: string]: unknown;
}

const Plantes: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [results, setResults] = useState<PlantResult[]>([]);
  const [selected, setSelected] = useState<PlantDetail | null>(null);
  const [selectedName, setSelectedName] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.length < 1) {
      setResults([]);
      return;
    }

    const controller = new AbortController();
    const timeout = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `${API_URL}/api/plants?q=${encodeURIComponent(query)}&limit=20`,
          { signal: controller.signal },
        );
        if (res.ok) {
          setResults(await res.json());
        }
      } catch (e) {
        if (!(e instanceof DOMException && e.name === 'AbortError')) {
          console.error(e);
        }
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      clearTimeout(timeout);
      controller.abort();
    };
  }, [query]);

  const handleSelect = async (scientificName: string) => {
    setSelectedName(scientificName);
    navigate(`/plantes?q=${encodeURIComponent(query)}`, { replace: true });
    try {
      const res = await fetch(
        `${API_URL}/api/plants/${encodeURIComponent(scientificName)}`,
      );
      if (res.ok) {
        setSelected(await res.json());
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Container>
      <Title>Plantes</Title>
      <SearchInput
        type="text"
        placeholder="Rechercher une plante…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoFocus
      />
      {loading && <Status>Recherche…</Status>}
      {results.length > 0 && !selected && (
        <ResultsList>
          {results.map((plant) => (
            <ResultItem
              key={plant.scientific_name}
              onClick={() => handleSelect(plant.scientific_name)}
            >
              <ScientificName>{plant.scientific_name}</ScientificName>
              {plant.common_names.length > 0 && (
                <CommonNames>{plant.common_names.join(', ')}</CommonNames>
              )}
            </ResultItem>
          ))}
        </ResultsList>
      )}
      {selected && (
        <DetailCard>
          <DetailHeader>
            <DetailTitle>{selectedName}</DetailTitle>
            <BackButton onClick={() => setSelected(null)}>
              ← Retour aux résultats
            </BackButton>
          </DetailHeader>
          <DetailBody>
            {Object.entries(selected).map(([key, value]) => (
              <DetailRow key={key}>
                <DetailKey>{key}</DetailKey>
                <DetailValue>
                  {Array.isArray(value) ? value.join(', ') : String(value)}
                </DetailValue>
              </DetailRow>
            ))}
          </DetailBody>
        </DetailCard>
      )}
    </Container>
  );
};

export default Plantes;

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: #01bf71;
  margin-bottom: 1.5rem;
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s;

  &:focus {
    border-color: #01bf71;
  }
`;

const Status = styled.p`
  color: #888;
  margin-top: 0.5rem;
  font-size: 0.9rem;
`;

const ResultsList = styled.ul`
  list-style: none;
  margin-top: 1rem;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
`;

const ResultItem = styled.li`
  padding: 0.75rem 1rem;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background 0.15s;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: #f0fff4;
  }
`;

const ScientificName = styled.span`
  font-style: italic;
  font-weight: 500;
  display: block;
`;

const CommonNames = styled.span`
  font-size: 0.85rem;
  color: #666;
`;

const DetailCard = styled.div`
  margin-top: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
`;

const DetailHeader = styled.div`
  padding: 1rem;
  background: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const DetailTitle = styled.h2`
  font-size: 1.3rem;
  font-style: italic;
  color: #333;
  margin: 0;
`;

const BackButton = styled.button`
  background: none;
  border: none;
  color: #01bf71;
  cursor: pointer;
  font-size: 0.9rem;

  &:hover {
    text-decoration: underline;
  }
`;

const DetailBody = styled.div`
  padding: 1rem;
`;

const DetailRow = styled.div`
  display: flex;
  padding: 0.4rem 0;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }
`;

const DetailKey = styled.span`
  font-weight: 500;
  min-width: 200px;
  color: #555;
`;

const DetailValue = styled.span`
  color: #333;
`;
