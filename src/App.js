import React from 'react';
import {Grid, IconButton, Button} from '@material-ui/core';
import ShoppingCart from '@material-ui/icons/ShoppingCart';
import './App.css';

/**
 * create main app component of the application
 * @return {JSX} main component of the application
 */
function App() {
  return (
    <div>
      <Grid container direction="row" spacing={3}
        justify="center" alignItems="center" >
        <Grid item xs={2}>
          <img className="logo" src={process.env.PUBLIC_URL + '/koala.png'} />
        </Grid>
        <Grid item xs={4}>
          <p className="title">Animal Cards</p>
        </Grid>
        <Grid item container xs={6} justify="flex-end"
          alignItems="center">
          <Grid item xs={2}>
            <Button variant="outlined" href="#">About</Button>
          </Grid>
          <Grid item xs={2}>
            <Button variant="outlined" href="#">Login</Button>
          </Grid>
          <Grid item xs={2}>
            <IconButton>
              <ShoppingCart />
            </IconButton>
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;
