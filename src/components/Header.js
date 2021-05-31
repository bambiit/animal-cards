import React from 'react';
import { Grid, Button, IconButton } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ShoppingCart from '@material-ui/icons/ShoppingCart';

const useStyles = makeStyles({
  logo: {
    width: '100%',
  },
  title: {
    fontFamily: '"Indie Flower", cursive',
    fontSize: '70px',
    color: '#4b778d',
  },
  button: {
    color: '#4b778d',
    borderColor: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
  },
});

const Header = () => {
  const classes = useStyles();
  return (
    <Grid container direction="row" spacing={3}
      justify="center" alignItems="center" >
      <Grid item xs={2}>
        <img className={classes.logo}
          src={process.env.PUBLIC_URL + '/koala.png'} />
      </Grid>
      <Grid item xs={4}>
        <p className={classes.title}>Animal Cards</p>
      </Grid>
      <Grid item container xs={6} justify="flex-end"
        alignItems="center">
        <Grid item xs={2}>
          <Button className={classes.button}
            variant="outlined" href="#">About</Button>
        </Grid>
        <Grid item xs={2}>
          <Button className={classes.button}
            variant="outlined" href="#">Login</Button>
        </Grid>
        <Grid item xs={2}>
          <IconButton className={classes.button}>
            <ShoppingCart />
          </IconButton>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Header;
