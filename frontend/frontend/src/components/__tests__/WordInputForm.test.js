jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: {} })),
  default: jest.fn(() => Promise.resolve({ data: {} })),
}));

import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import WordInputForm from '../WordInputForm';

test('renders input form and buttons', () => {
    render(<WordInputForm onFindSimilar={() => {}} onAddWord={() => {}} />);
    
    // Check that input and buttons are rendered
    const inputElement = screen.getByPlaceholderText(/enter a word/i);
    expect(inputElement).toBeInTheDocument();

    const findButton = screen.getByText(/find similar words/i);
    expect(findButton).toBeInTheDocument();

    const addButton = screen.getByText(/add word to database/i);
    expect(addButton).toBeInTheDocument();
});

test('submits the correct word when "Find Similar Words" is clicked', () => {
    const mockFindSimilar = jest.fn();
    render(<WordInputForm onFindSimilar={mockFindSimilar} onAddWord={() => {}} />);

    // Simulate typing a word into the input
    const inputElement = screen.getByPlaceholderText(/enter a word/i);
    fireEvent.change(inputElement, { target: { value: 'testword' } });

    // Simulate clicking the "Find Similar Words" button
    const findButton = screen.getByText(/find similar words/i);
    fireEvent.click(findButton);

    expect(mockFindSimilar).toHaveBeenCalledWith('testword');
});
