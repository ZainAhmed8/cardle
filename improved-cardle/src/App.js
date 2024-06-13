import React, { useState } from 'react';
import styled from 'styled-components';

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1b1b1b;
  color: #fff;
`;

const GuessInput = styled.input`
  padding: 10px;
  margin: 20px 0;
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
  const [guess, setGuess] = useState('');

  const handleGuessChange = (e) => {
    setGuess(e.target.value);
  };

  return (
    <AppContainer>
      <h1>Cardle</h1>
      <GuessInput 
        type="text" 
        value={guess} 
        onChange={handleGuessChange} 
        placeholder="Type a guess here..." 
      />
      <InfoContainer>
        <InfoBox bgColor="#a8d600" color="#000">
          Most Recent Year
          <br />
          2011
        </InfoBox>
        <InfoBox>
          Country
          <br />
          USA
        </InfoBox>
        <InfoBox>
          Body Type
          <br />
          Hip Hop
        </InfoBox>
        <InfoBox>
          Manufacturer
          <br />
          Solo
        </InfoBox>
        <InfoBox>
          Average MSRP
          <br />
          #53
        </InfoBox>
      </InfoContainer>
      <ButtonContainer>
        <Button color="#444" hoverColor="#666">No Match</Button>
        <Button color="#ff0" hoverColor="#ff8">Close</Button>
        <Button color="#0f0" hoverColor="#8f8">Match</Button>
      </ButtonContainer>
    </AppContainer>
  );
}

export default App;
