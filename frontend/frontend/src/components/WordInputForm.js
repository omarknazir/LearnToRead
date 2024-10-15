import React, { useState } from 'react';

const WordInputForm = ({ onFindSimilar, onAddWord }) => {
    const [word, setWord] = useState('');
    const [action, setAction] = useState('find');  // New state to track action (find/add)

    const handleSubmit = (e) => {
        e.preventDefault();
        if (action === 'find') {
            onFindSimilar(word);
        } else {
            onAddWord(word);
        }
        setWord('');  // Reset the input field after submit
    };

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={word} 
                onChange={(e) => setWord(e.target.value)} 
                placeholder="Enter a word" 
                required 
            />
            <div>
                <button type="submit" onClick={() => setAction('find')}>Find Similar Words</button>
                <button type="submit" onClick={() => setAction('add')}>Add Word to Database</button>
            </div>
        </form>
    );
};

export default WordInputForm;
