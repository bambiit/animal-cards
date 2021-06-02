import React from 'react';
import { Grid, Button, IconButton } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ShoppingCart from '@material-ui/icons/ShoppingCart';
import { Link } from 'react-router-dom';

const useStyles = makeStyles({
  logo: {
    width: '100%'
  },
  title: {
    fontFamily: '"Indie Flower", cursive',
    fontSize: '70px',
    color: '#4b778d'
  },
  button: {
    color: '#4b778d',
    borderColor: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
    textDecoration: 'none'
  },
  link: {
    textDecoration: 'none'
  }
});

const Header = () => {
  const classes = useStyles();
  return (
    <Grid container direction="row" spacing={2}
      justify="center" alignItems="center" >
      <Grid item container direction="row" xs={6} justify="flex-start" alignItems="center">
        <Grid item xs={4}>
          <Link to="/">
            <img className={classes.logo}
              src={process.env.PUBLIC_URL + '/koala.png'} />
          </Link>
        </Grid>
        <Grid item xs={8}>
          <Link className={classes.link} to="/">
            <p className={classes.title}>Animal Cards</p>
          </Link>
        </Grid>
      </Grid>
      <Grid item container xs={6} justify="flex-end"
        alignItems="center">
        <Grid item xs={2}>
          <Link className={classes.button} to="/about">
            <Button className={classes.button}
              variant="outlined">About</Button>
          </Link>
        </Grid>
        <Grid item xs={2}>
          <Link className={classes.button} to="/login">
            <Button className={classes.button}
              variant="outlined">Login</Button>
          </Link>
        </Grid>
        <Grid item xs={2}>
          <IconButton className={classes.button}>
            <ShoppingCart />
          </IconButton>
        </Grid>
      </Grid>
    </Grid >
  );
};

export default Header;
