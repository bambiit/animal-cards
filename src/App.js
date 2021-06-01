import React from 'react';
import Header from './components/Header';
import AnimalCardList from './components/AnimalCardList';
import Footer from './components/Footer';
import About from './components/About';
import Login from './components/Login';
import './App.css';
import { Route, Switch } from 'react-router-dom';

/**
 * create main app component of the application
 * @return {JSX} main component of the application
 */
function App() {
  return (
    <div>
      <Header />
      <Switch>
        <Route path="/about">
          <About />
        </Route>
        <Route path='/login'>
          <Login />
        </Route>
        <Route path="/">
          <AnimalCardList />
        </Route>
      </Switch>
      <Footer />
    </div >
  );
}

export default App;
