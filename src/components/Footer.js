import React from 'react';
import makeStyles from '@material-ui/styles/makeStyles';

const useStyles = makeStyles({
  credit: {
    color: '#4b778d',
    fontFamily: '"Tajawal", sans-serif',
  },
});

const Footer = () => {
  const classes = useStyles();

  return (
    <p className={classes.credit}>@2021 HY, Helsinki, Finland</p>
  );
};

export default Footer;
