import React from 'react';
import makeStyles from '@material-ui/styles/makeStyles';

const useStyles = makeStyles({
  credit: {
    color: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
    paddingTop: '50px'
  }
});

const Footer = () => {
  const classes = useStyles();

  return (
    <p className={classes.credit}>
      <i>@2021 HY, Helsinki, Finland</i>
    </p>
  );
};

export default Footer;
