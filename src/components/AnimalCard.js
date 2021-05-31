import React from 'react';
import {
  Grid, CardActionArea, CardMedia,
  CardContent, Typography,
} from '@material-ui/core';
import PropTypes from 'prop-types';
import makeStyles from '@material-ui/core/styles/makeStyles';

const useStyles = makeStyles({
  image: {
    height: '300px',
    borderRadius: '15px 15px 0 0',
  },
  card: {
    background: '#fff',
    borderRadius: 15,
  },
  cardTypo: {
    color: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
  },
  cardTypoTitle: {
    color: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
    fontWeight: 400,
  },
});

const AnimalCard = ({ xs }) => {
  const classes = useStyles();

  return (
    <Grid item xs={xs}>
      <CardActionArea className={classes.card}>
        <CardMedia className={classes.image}
          image={process.env.PUBLIC_URL + '/Tiger.jpeg'} title="Tiger">
        </CardMedia>
        <CardContent>
          <Typography className={classes.cardTypoTitle}
            gutterBottom variant="h5" component="h2">
            Tiger
          </Typography>
          <Typography className={classes.cardTypo}
            variant="body2" color="textSecondary" component="p">
            Tigers generally gain independence at
            around two years of age and attain sexual
            maturity at age three or four for females and
            four or five years for males. Juvenile mortality is high,
            however—about half of all cubs do not survive
            more than two years. Tigers have been known
            to reach up to 20 years of age in the wild.
          </Typography>
        </CardContent>
      </CardActionArea>
    </Grid>
  );
};

AnimalCard.propTypes = {
  xs: PropTypes.number.isRequired,
};

export default AnimalCard;
