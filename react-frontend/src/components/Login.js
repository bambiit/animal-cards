import { Button, TextField, Grid } from '@material-ui/core';
import React from 'react';

const Login = () => {
  return (
    <form autoComplete="off">
      <Grid container spacing={3} justify="center" alignItems="center" direction="column" >
        <Grid item>
          <TextField required id="username" label="Username" />
        </Grid>
        <Grid item>
          <TextField required id="password" label="Password" type="password" />
        </Grid>
        <Grid item>
          <Button type="submit" variant="contained">Login</Button>
        </Grid>
      </Grid>
    </form >
  );
};

export default Login;
