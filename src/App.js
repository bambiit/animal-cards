import React from 'react';
import Header from './components/Header';
import AnimalCardList from './components/AnimalCardList';
import Footer from './components/Footer';
import './App.css';

/**
 * create main app component of the application
 * @return {JSX} main component of the application
 */
function App() {
  return (
    <div>
      <Header />
      <AnimalCardList />
      <Footer />
    </div >
  );
}

export default App;
