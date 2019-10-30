import React from 'react';
import PropTypes from 'prop-types';
import { StyleSheet } from 'react-native';
import { Icon } from 'react-native-elements';


export default function RaiseReversedIconComponent(props) {
  return (
    <Icon
      reverse
      raised
      iconStyle={[styles.iconStyle, props.iconStyle]}
      type={props.type}
      name={props.name}
      color={props.color}
      size={13}
    />
  );
}

const styles = StyleSheet.create({
  iconStyle: {
    fontSize: 18,
  },
});


RaiseReversedIconComponent.propTypes = {
  type: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  color: PropTypes.string.isRequired,
  iconStyle: PropTypes.object,
};
RaiseReversedIconComponent.defaultProps = {
  iconStyle: {},
};