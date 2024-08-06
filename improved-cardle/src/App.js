import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1b1b1b;
  color: #fff;
`;

const Select = styled.select`
  padding: 10px;
  margin: 10px 0;
  width: 300px;
  border: none;
  border-radius: 5px;
`;

const InfoContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, auto);
  gap: 10px;
  justify-items: center;
  align-items: center;
`;

const InfoBox = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.bgColor || '#333'};
  padding: 20px;
  border-radius: 10px;
  width: 150px;
  height: 60px;
  color: ${props => props.color || '#fff'};
  font-weight: bold;
  font-size: 1em;
  text-align: center;
`;

const ButtonContainer = styled.div`
  display: flex;
  margin-top: 20px;
`;

const Button = styled.button`
  padding: 10px 20px;
  margin: 0 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: ${props => props.color || '#555'};
  color: ${props => (props.color === '#ff0' ? '#000' : '#fff')};
  &:hover {
    background-color: ${props => props.hoverColor || '#777'};
  }
`;

function App() {
  const [year, setYear] = useState('');
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [years, setYears] = useState([]);
  const [makes, setMakes] = useState([]);
  const [models, setModels] = useState([]);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [guessesLeft, setGuessesLeft] = useState(10);

  useEffect(() => {
    axios.get('/api/years').then(response => {
      setYears(response.data);
    });
  }, []);

  useEffect(() => {
    if (year) {
      axios.get(`/api/makes?year=${year}`).then(response => {
        setMakes(response.data);
        setMake('');
        setModel('');
        setModels([]);
      });
    }
  }, [year]);

  useEffect(() => {
    if (make) {
      axios.get(`/api/models?make=${make}&year=${year}`).then(response => {
        setModels(response.data);
        setModel('');
      });
    }
  }, [make, year]);

  const handleYearChange = (e) => {
    setYear(e.target.value);
  };

  const handleMakeChange = (e) => {
    setMake(e.target.value);
  };

  const handleModelChange = (e) => {
    setModel(e.target.value);
  };

  const handleSubmitGuess = () => {
    const guess = {
      year: parseInt(year, 10),
      make,
      model,
      car_of_the_day_id: 'YOUR_CAR_OF_THE_DAY_ID' // Replace this with the actual ID or fetch it dynamically
    };

    axios.post('/submit_guess', guess).then(response => {
      setComparisonResult(response.data.comparison);
      setGuessesLeft(response.data.guesses_left);
    }).catch(error => {
      console.error('Error submitting guess:', error);
    });
  };

  return (
    <AppContainer>
      <h1>Cardle</h1>
      <Select value={year} onChange={handleYearChange}>
        <option value="">Select Year</option>
        {years.map(year => (
          <option key={year} value={year}>{year}</option>
        ))}
      </Select>
      <Select value={make} onChange={handleMakeChange} disabled={!year}>
        <option value="">Select Make</option>
        {makes.map(make => (
          <option key={make} value={make}>{make}</option>
        ))}
      </Select>
      <Select value={model} onChange={handleModelChange} disabled={!make}>
        <option value="">Select Model</option>
        {models.map(model => (
          <option key={model} value={model}>{model}</option>
        ))}
      </Select>

      {comparisonResult && (
        <InfoContainer>
          {Object.keys(comparisonResult).map(key => (
            <InfoBox key={key} bgColor={comparisonResult[key].match === 'green' ? '#0f0' : '#f00'}>
              {key.charAt(0).toUpperCase() + key.slice(1)}:
              <br />
              {comparisonResult[key].match}
            </InfoBox>
          ))}
        </InfoContainer>
      )}

      <ButtonContainer>
        <Button color="#0f0" hoverColor="#8f8" onClick={handleSubmitGuess}>
          Submit Guess
        </Button>
      </ButtonContainer>

      {guessesLeft > 0 ? (
        <p>Guesses left: {guessesLeft}</p>
      ) : (
        <p>No more guesses left!</p>
      )}
    </AppContainer>
  );
}

export default App;
