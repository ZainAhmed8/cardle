import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
// import Flag from 'react-world-flags'

const renderArrow = (direction) => {
  if (direction === 'up') {
    return '▲';
  } else if (direction === 'down') {
    return '▼';
  }
  return '';
}

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #1b1b1b;
  color: #fff;
  min-height: 100vh;
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
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 20px;
`;

const GuessContainer = styled.div`
  margin-top: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const GuessBox = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  background-color: #333;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 10px;
  width: 30%;  // Adjust this to make the box smaller
`;

const InfoBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: ${props => props.bgColor || '#333'};
  padding: 30px;  // Adjust this to make the box smaller
  border-radius: 10px;
  color: ${props => props.color || '#fff'};
  font-weight: bold;
  font-size: 1em;
  text-align: center;

  & > div {
    margin-bottom: 10px;  // Adjust this value to add space between the lines
  }
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
  const [guesses, setGuesses] = useState([]);

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
      car_of_the_day_id: '66afcf6373a71b92e6293a41' // CAR OF THE DAY, CURRENTLY 2020 Porsche Panamera
    };

    axios.get(`/api/car_details?year=${year}&make=${make}&model=${model}`).then(response => {
      const guessedCarDetails = response.data;
      axios.post('/submit_guess', guess).then(response => {
        const newGuess = {
          year,
          make,
          model,
          body_styles: guessedCarDetails.body_styles,
          country: guessedCarDetails.country,
          starting_msrp: guessedCarDetails.starting_msrp,
          comparison: response.data.comparison,
        };
        setGuesses([...guesses, newGuess]);
      }).catch(error => {
        console.error('Error submitting guess:', error);
      });
    }).catch(error => {
      console.error('Error fetching car details:', error);
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

      <ButtonContainer>
        <Button color="#a200ff" hoverColor="#da99ff" onClick={handleSubmitGuess}>
          Submit Guess
        </Button>
      </ButtonContainer>

      <GuessContainer>
        {guesses.map((guess, index) => (
          <GuessBox key={index}>
            <InfoBox bgColor={guess.comparison.year.match}>
              <div>Year</div>
              <div>
               {guess.year} {renderArrow(guess.comparison.year.direction)}
              </div>
            </InfoBox>
            <InfoBox bgColor={guess.comparison.make.match}>
              <div>Make</div><div>{guess.make}</div>
            </InfoBox>
            <InfoBox bgColor={guess.comparison.model.match}>
              <div>Model</div><div>{guess.model}</div>
            </InfoBox>
            <InfoBox bgColor={guess.comparison.body_styles.match}>
              <div>Body Styles</div> <div>{guess.body_styles}</div>
            </InfoBox>
            <InfoBox bgColor={guess.comparison.country.match}>
              <div>Country</div><div>{guess.country}</div>
            </InfoBox>
            <InfoBox bgColor={guess.comparison.starting_msrp.match}>
              <div>Starting MSRP</div><div>{guess.starting_msrp} {renderArrow(guess.comparison.starting_msrp.direction)}</div>
            </InfoBox>
          </GuessBox>
        ))}
      </GuessContainer>
    </AppContainer>
  );
}

export default App;
