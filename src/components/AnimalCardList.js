import React from 'react';
import Grid from '@material-ui/core/Grid';
import AnimalCard from './AnimalCard';

const AnimalCardList = () => {
  return (
    <Grid container direction="row" spacing={4}
      justify="center" alignItems="center">
      <AnimalCard xs={3} />
      <AnimalCard xs={3} />
      <AnimalCard xs={3} />
      <AnimalCard xs={3} />
    </Grid>
  );
};

export default AnimalCardList;
