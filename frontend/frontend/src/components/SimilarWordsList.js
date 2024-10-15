// src/components/SimilarWordsList.js
import React from "react";

const SimilarWordsList = ({ similarWords }) => {
  if (similarWords.length === 0) {
    return <p>No similar words found.</p>;
  }

  return (
    <div>
      <h3>Similar Words</h3>
      <ul>
        {similarWords.map((word, index) => (
          <li key={index}>{word}</li>
        ))}
      </ul>
    </div>
  );
};

export default SimilarWordsList;
