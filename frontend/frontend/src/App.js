import React, { useState } from 'react';
import WordInputForm from './components/WordInputForm';
import SimilarWordsList from './components/SimilarWordsList';
import axios from 'axios';

function App() {
    const [similarWords, setSimilarWords] = useState([]);

    const findSimilarWords = (word) => {
        axios.post('http://localhost:5000/api/similar-words', { word })
            .then((response) => {
                setSimilarWords(response.data.similar_words);
            })
            .catch((error) => {
                console.error('Error fetching similar words:', error);
            });
    };

    const addWordToDatabase = (word) => {
        axios.post('http://localhost:5000/api/add-word', { word })
            .then(() => {
                alert(`Word "${word}" added successfully!`);
            })
            .catch((error) => {
                console.error('Error adding word:', error);
            });
    };

    return (
        <div className="App">
            <h1>Learn To Read</h1>
            <WordInputForm onFindSimilar={findSimilarWords} onAddWord={addWordToDatabase} />
            <SimilarWordsList similarWords={similarWords} />
        </div>
    );
}

export default App;
